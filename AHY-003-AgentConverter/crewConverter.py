# code_conversion_crew.py
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM
from toolFileReader import FileReaderTool
import os
import re

def extract_and_save_code_blocks(output: str, output_folder: str = "."):
    pattern = re.compile(r"<(\w+\.py)>(.*?)</\1>", re.DOTALL)
    matches = pattern.findall(output)

    if not matches:
        print("Nenhum bloco de código encontrado.")
        return

    for filename, code in matches:
        filepath = os.path.join(output_folder, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code.strip())
        print(f"Arquivo salvo: {filepath}")


class CodeConversionCrew:
    def __init__(self, input_folder: str = "./input"):
        self.llm = MyLLM.geminiflash20
        self.folder = input_folder
        self.reader_tool = FileReaderTool(folder=input_folder)
        self.crew = self._setup_crew()

    def _setup_crew(self):
        agent = Agent(
            role="Especialista em Conversão para CrewAI",
            goal="Converter códigos baseados em LLM em agentes CrewAI reutilizáveis",
            backstory=(
                "Você é um engenheiro de software especializado em estruturar fluxos baseados em LLM "
                "como agentes CrewAI. Seu objetivo é entender o funcionamento atual do código e reestruturá-lo "
                "em agentes CrewAI bem definidos."
            ),
            tools=[self.reader_tool],
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description="""Use a ferramenta para ler todos os arquivos de código e exemplos de output.
1. Analise como a LLM é usada no código.
2. Converta a estrutura para o padrão CrewAI.
3. Siga o modelo <crewSample> e <toolSample>. Cada tool deve ser separada em arquivo próprio usando BaseTool.
4. Envolva cada arquivo gerado entre tags <nome.py> e </nome.py>. Crie o nome para os arquivos de acordo a funcionalidade deles e nomeie os placeholders entre <>. Por exemplo, se o codigo gerar musica o placeholder devera se chamar <crewMusicGenerator>. Os arquivos crew devem se iniciar com crew, e.g. <crewSample> e os arquivos tool devem iniciar com tool e.g <toolSample>
5. Nunca gere o arquivo MyLLM.py (ele já existe).
6. Se houver necessidade de secrets, gere um conteúdo sugerido para o arquivo .env. Envolva o arquivo .env entre <.env>

<crewSample>
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM
from GmailReader import GmailReaderTool
import re

class EmailTriageCrew:
    def __init__(self):
        self.llm = MyLLM.Ollama_qwen3_14b
        self.crew = self._setup_crew()

    def _setup_crew(self):
        reader_tool = GmailReaderTool()

        agent = Agent(
            role="Analista de Caixa de Entrada",
            goal="Ler e classificar os e-mails recebidos como importantes ou não.",
            backstory="Você ajuda seu usuário a manter o foco apenas nos e-mails essenciais.",
            tools=[reader_tool],
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description'''Use a ferramenta para ler os e-mails e 
            classifique os que exigem atenção urgente. Retorne um resumo com título,
            remetente e por que é importante. Ignore se o email e' spam ou propaganda.
            Foque e analise um email real, realmente direcionado a mim ou fatura, boleto, comunicado, ou direcionado. 
            Leia todo o conteudo e faca essa analise critica''',
            expected_output='''
            Lista dos e-mails importantes com título e justificativa.
            Escreva um breve resumo e as acoes a serem tomadas.
            ''',
            agent=agent
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

    def kickoff(self):
        return self.crew.kickoff()
    
    
if __name__ == "__main__":
    crew = EmailTriageCrew()
    result = crew.kickoff()
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()
    print(result)

</crewSample>


<toolSample># gmail_reader_tool.py
from crewai.tools import BaseTool
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

class GmailReaderTool(BaseTool):
    name: str  =  "Gmail Inbox Tool"
    description: str = "Lê e-mails recentes do usuário e retorna os mais importantes."

    def _get_service(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        token_path = 'token.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('clientSecret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def _list_messages(self, service, query='is:unread', max_results=50):
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        return results.get('messages', [])
    
    def _parse_message(self, msg_data):
        snippet = msg_data.get("snippet", "")
        headers = msg_data.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sem assunto')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Remetente desconhecido')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Data desconhecida')

        return {
            "remetente": sender,
            "assunto": subject,
            "resumo": snippet,
            "data": date
        }

    def _get_message_content(self, service, msg_id):
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        parsed = self._parse_message(msg_data)
        return f"De: {parsed['remetente']}\nAssunto: {parsed['assunto']}\nResumo: {parsed['resumo']}"


    def _run(self, query="is:unread newer_than:3d"):
        service = self._get_service()
        messages = self._list_messages(service, query)
        if not messages:
            return "Nenhum e-mail encontrado."

        structured_emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            structured_emails.append(self._parse_message(msg_data))

        return structured_emails



# TESTE LOCAL INDEPENDENTE
if __name__ == "__main__":
    print("Executando leitura de e-mails...")
    tool = GmailReaderTool()
    resultado = tool._run()
    print(resultado)
</toolSample>
""",
            expected_output="""Blocos de código como <.env>...variaveis env... </.env> <nome_arquivo.py>...codigo...</nome_arquivo.py>.
Inclua arquivos separados para tools e arquivos da crew. Código limpo e funcional.""",
            agent=agent
        )

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential
        )

    def kickoff(self):
        context = self.reader_tool._run()
        return self.crew.kickoff(inputs={"message": context})


if __name__ == "__main__":
    import sys
    # folder = sys.argv[1] if len(sys.argv) > 1 else "./input"
    base_dir = os.path.dirname(__file__)
    folder = os.path.abspath(os.path.join(base_dir, "../AWL-006-MusicGenerator"))
    crew = CodeConversionCrew(folder)
    result_obj = crew.kickoff()
    result = str(result_obj.raw)
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL).strip()
    print(result)
    # if result_obj.json_dict:
    #     print(f"JSON Output: {json.dumps(result_obj.json_dict, indent=2)}")
    # if result.pydantic:
    #     print(f"Pydantic Output: {result_obj.pydantic}")
    # print(f"Tasks Output: {result_obj.tasks_output}")
    # print(f"Token Usage: {result_obj.token_usage}")
    
    extract_and_save_code_blocks(result, folder)
