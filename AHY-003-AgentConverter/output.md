# Agent: Especialista em Conversão para CrewAI
## Final Answer:
<crewMusicGenerator>
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM  # Assuming MyLLM has a relevant LLM for music generation
from ModelsLabTool import ModelsLabTool  # Tool for interacting with ModelsLab API
import os

class MusicGeneratorCrew:
    def __init__(self):
        self.llm = MyLLM.Ollama_qwen3_14b  # Assume MyLLM is set up appropriately
        self.crew = self._setup_crew()

    def _setup_crew(self):
        music_tool = ModelsLabTool()  # Initialize your tool here

        agent = Agent(
            role="Música Geração Agente",
            goal="Gerar música com base em um prompt dado.",
            backstory="Você ajuda os usuários a criar músicas originais de diferentes gêneros.",
            tools=[music_tool],
            llm=self.llm,
            verbose=True
        )

        task = Task(
            description='''Gere uma peça musical de 30 segundos com base no prompt fornecido.
            O prompt deve descrever o estilo, os instrumentos, o humor e a estrutura desejados.''',      
            expected_output='''Um arquivo de áudio (mp3) da música gerada.',
            'A música deve ser de alta qualidade e atender aos requisitos do prompt dado.''',
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
    crew = MusicGeneratorCrew()
    result = crew.kickoff()
    print(result)

</crewMusicGenerator>

<toolModelsLab>
from crewai.tools import BaseTool
import requests
from uuid import uuid4
import os

class ModelsLabTool(BaseTool):
    name: str = "ModelsLab Music Generation Tool"
    description: str = "Gera música com a API ModelsLab utilizando um prompt."

    def _run(self, prompt):
        # Make a request to the ModelsLab API to generate music based on the prompt
        url = "https://api.modelslab.com/generate/music"
        headers = {
            "Authorization": f"Bearer {os.getenv('MODELS_LAB_API_KEY')}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt
        }
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            music_url = response.json().get("data").get("url")  # Adjust based on the actual API response structure.
            return {"audio": [{"url": music_url}]}
        else:
            return {"error": "Failed to generate music."}

</toolModelsLab>

.env
# .env file content suggestion
MODELS_LAB_API_KEY="your_models_lab_api_key_here"


[TaskOutput(description='Use a ferramenta para ler todos os arquivos de código e exemplos de output.\n1. Analise como a LLM é usada no código.\n2. Converta a estrutura para o padrão CrewAI.\n3. Siga o modelo <sample> e <sampletool>. Cada tool deve ser separada em arquivo próprio usando BaseTool.\n4. Envolva cada arquivo gerado entre tags <nome.py> e </nome.py>. Os arquivos crew devem se iniciar com crew, e.g. <crewSample> e os arquivos tool devem iniciar com tool e.g <toolSample>\n5. Nunca gere o arquivo MyLLM.py (ele já existe).\n6. Se houver necessidade de secrets, gere um conteúdo sugerido para o arquivo .env.\n\n<crewSample>\nfrom crewai import Agent, Task, Crew, Process\nfrom MyLLM import MyLLM\nfrom GmailReader import GmailReaderTool\nimport re\n\nclass EmailTriageCrew:\n    def __init__(self):\n        self.llm = MyLLM.Ollama_qwen3_14b\n        self.crew = self._setup_crew()\n\n    def _setup_crew(self):\n        reader_tool = GmailReaderTool()\n\n        agent = Agent(\n            role="Analista de Caixa de Entrada",\n            goal="Ler e classificar os e-mails recebidos como importantes ou não.",\n            backstory="Você ajuda seu usuário a manter o foco apenas nos e-mails essenciais.",\n            tools=[reader_tool],\n            llm=self.llm,\n            verbose=True\n        )\n\n        task = Task(\n            description\'\'\'Use a ferramenta para ler os e-mails e \n            classifique os que exigem atenção urgente. Retorne um resumo com título,\n            remetente e por que é importante. Ignore se o email e\' spam ou propaganda.\n            Foque e analise um email real, realmente direcionado a mim ou fatura, boleto, comunicado, ou direcionado. \n            Leia todo o conteudo e faca essa analise critica\'\'\',\n            expected_output=\'\'\'\n            Lista dos e-mails importantes com título e justificativa.\n            Escreva um breve resumo e as acoes a serem tomadas.\n            \'\'\',\n            agent=agent\n        )\n\n        return Crew(\n            agents=[agent],\n            tasks=[task],\n           
 process=Process.sequential\n        )\n\n    def kickoff(self):\n        return self.crew.kickoff()\n    \n    \nif __name__ == "__main__":\n    crew = EmailTriageCrew()\n    result = crew.kickoff()\n    result = re.sub(r"", "", result, flags=re.DOTALL).strip()\n    print(result)\n\n</crewSample>\n\n\n<toolSample># gmail_reader_tool.py\nfrom crewai.tools import BaseTool\nfrom google.oauth2.credentials import Credentials\nfrom google_auth_oauthlib.flow import InstalledAppFlow\nfrom googleapiclient.discovery import build\nfrom google.auth.transport.requests import Request\nimport os\n\nclass GmailReaderTool(BaseTool):\n    name: str  =  "Gmail Inbox Tool"\n    description: str = "Lê e-mails recentes do usuário e retorna os mais importantes."\n\n    def _get_service(self):\n        SCOPES = [\'https://www.googleapis.com/auth/gmail.readonly\']\n        creds = None\n        token_path = \'token.json\'\n\n        if os.path.exists(token_path):\n            creds = Credentials.from_authorized_user_file(token_path, SCOPES)\n\n        if not creds or not creds.valid:\n            if creds and creds.expired and creds.refresh_token:\n            
    creds.refresh(Request())\n            else:\n                flow = InstalledAppFlow.from_client_secrets_file(\'clientSecret.json\', SCOPES)\n                creds = flow.run_local_server(port=0)\n         
   with open(token_path, \'w\') as token:\n                token.write(creds.to_json())\n\n        return build(\'gmail\', \'v1\', credentials=creds)\n\n    def _list_messages(self, service, query=\'is:unread\', max_results=50):\n        results = service.users().messages().list(userId=\'me\', q=query, maxResults=max_results).execute()\n        return results.get(\'messages\', [])\n    \n    def _parse_message(self, msg_data):\n        snippet = msg_data.get("snippet", "")\n        headers = msg_data.get(\'payload\', {}).get(\'headers\', [])\n        subject = next((h[\'value\'] for h in headers if h[\'name\'] == \'Subject\'), \'Sem assunto\')\n        sender = next((h[\'value\'] for h in headers if h[\'name\'] == \'From\'), \'Remetente desconhecido\')\n        date = next((h[\'value\'] for h in headers if h[\'name\'] == \'Date\'), \'Data desconhecida\')\n\n        return {\n            "remetente": sender,\n            "assunto": subject,\n            "resumo": snippet,\n            "data": date\n        }\n\n    def _get_message_content(self, service, msg_id):\n        msg_data = service.users().messages().get(userId=\'me\', id=msg_id, format=\'full\').execute()\n        parsed = self._parse_message(msg_data)\n        return f"De: {parsed[\'remetente\']}\nAssunto: {parsed[\'assunto\']}\nResumo: {parsed[\'resumo\']}"\n\n\n    def _run(self, query="is:unread newer_than:3d"):\n        service = self._get_service()\n        messages = self._list_messages(service, query)\n        if not messages:\n            return "Nenhum e-mail encontrado."\n\n        structured_emails = []\n        for msg in messages:\n            msg_data = service.users().messages().get(userId=\'me\', id=msg[\'id\'], format=\'full\').execute()\n            structured_emails.append(self._parse_message(msg_data))\n\n        return structured_emails\n\n\n\n# TESTE LOCAL INDEPENDENTE\nif __name__ == "__main__":\n    print("Executando leitura de e-mails...")\n    tool = GmailReaderTool()\n    resultado = tool._run()\n    print(resultado)\n</toolSample>\n', name=None, expected_output='Blocos de código como <nome_arquivo.py>...codigo...</nome_arquivo.py>.\nInclua arquivos separados para tools e arquivos da crew. Código limpo e funcional.', summary='Use a ferramenta para ler todos os arquivos de código...', raw='<crewMusicGenerator>\nfrom crewai import Agent, Task, Crew, Process\nfrom MyLLM import MyLLM  # Assuming MyLLM has a relevant LLM for music generation\nfrom ModelsLabTool import ModelsLabTool  # Tool for interacting with ModelsLab API\nimport os\n\nclass MusicGeneratorCrew:\n    def __init__(self):\n        self.llm = MyLLM.Ollama_qwen3_14b  # Assume MyLLM is set up appropriately\n        self.crew = self._setup_crew()\n\n    def _setup_crew(self):\n        music_tool = ModelsLabTool()  # Initialize your tool here\n\n        agent = Agent(\n            role="Música Geração Agente",\n            goal="Gerar música com base em um prompt dado.",\n            backstory="Você ajuda os usuários a criar músicas originais de diferentes gêneros.",\n            tools=[music_tool],\n            llm=self.llm,\n            verbose=True\n        )\n\n        task = Task(\n            description=\'\'\'Gere uma peça musical de 30 segundos com base no prompt fornecido. \n            O prompt deve descrever o estilo, os instrumentos, o humor e a estrutura desejados.\'\'\',\n            expected_output=\'\'\'Um arquivo de áudio (mp3) da música gerada.\',\n            \'A música deve ser de alta qualidade e atender aos requisitos do prompt dado.\'\'\',\n            agent=agent\n        )\n\n        return Crew(\n            agents=[agent],\n            tasks=[task],\n            process=Process.sequential\n        )\n\n    def kickoff(self):\n        return self.crew.kickoff()\n\nif __name__ == "__main__":\n    crew = MusicGeneratorCrew()\n    result = crew.kickoff()\n    print(result)\n\n</crewMusicGenerator>\n\n<toolModelsLab>\nfrom crewai.tools import BaseTool\nimport requests\nfrom uuid import uuid4\nimport os\n\nclass ModelsLabTool(BaseTool):\n    name: str = "ModelsLab Music Generation Tool"\n    description: str = "Gera música com a API ModelsLab utilizando um prompt."\n\n    def _run(self, prompt):\n        # Make a request to the ModelsLab API to generate music based on the prompt\n        url = "https://api.modelslab.com/generate/music"\n        headers = {\n            "Authorization": f"Bearer {os.getenv(\'MODELS_LAB_API_KEY\')}",\n            "Content-Type": "application/json"\n        }\n        data = {\n            "prompt": prompt\n        }\n        response = requests.post(url, headers=headers, json=data)\n        \n        if response.status_code == 200:\n          
  music_url = response.json().get("data").get("url")  # Adjust based on the actual API response structure.\n            return {"audio": [{"url": music_url}]}\n        else:\n            return {"error": "Failed to generate music."}\n\n</toolModelsLab>\n\n.env\n# .env file content suggestion\nMODELS_LAB_API_KEY="your_models_lab_api_key_here"', pydantic=None, json_dict=None, agent='Especialista em Conversão para CrewAI', output_format=<OutputFormat.RAW: 'raw'>)]