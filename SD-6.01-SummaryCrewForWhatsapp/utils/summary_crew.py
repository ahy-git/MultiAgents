from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM

class SummaryCrew:
    """
    Classe para organizar um agente, tarefa e execução de resumos de mensagens do WhatsApp.
    """

    def __init__(self):
        load_dotenv()
        # self.llm = "gemini/gemini-2.0-flash-lite"
        # self.llm = LLM(model="ollama/deepseek-r1:14b", base_url="http://localhost:11434", max_tokens=2048, num_ctx=12000)
        # self.llm = LLM(model="ollama/deepseek-r1:8b", base_url="http://localhost:11434",
        #                max_tokens=131072, num_ctx=12000, timeout=1200)
        # self.llm = LLM(model="gemini/gemini-2.0-flash-lite")
        self.llm = MyLLM.geminiflash20
        self.create_crew()

    def create_crew(self):
        # Configurar o agente
        self.agent = Agent(
            role="Assistente de Resumos",
            goal="Criar resumos organizados e objetivos de mensagens de WhatsApp.",
            backstory=(
                "Você é um assistente de IA especializado em analisar e organizar informações "
                "extraídas de mensagens de WhatsApp, garantindo clareza e objetividade."
            ),
            verbose=True,
            memory=False,  # Não precisa de memória para esta tarefa simples
            llm=self.llm
        )

        # Configurar a tarefa
        self.task = Task(
            description=r"""
Você é um assistente de IA especializado 
em criar resumos organizados e objetivos 
de mensagens em grupos de WhatsApp. 
Seu objetivo é apresentar as informações 
de forma clara e segmentada, 
usando o templete delimitado por <template>. 
Para alimentar o resumo use as mensagens
de WhatsApp delimitadas por <msgs>. 

Importante:
- Ignore mensagens que são resumos anteriores.
- Retire os placeholders < > do texto. 
- Deve haver somente um tópico da lista abaixo no resumo:
    - Resumo do Grupo
    - Tópico Principal
    - Dúvidas, Erros e suas Soluções
    - Resumo geral do período
    - Links do Dia
    - Conclusão
- Quando não houver informações sobre um tópico simplesmente não coloque o tópico.
<template>
*Resumo do Grupo📝 - <Data ou Período>*

*<Tópico Principal> <Emoji relacionado> - <Horário>*

- *Participantes:* <Nomes dos usuários envolvidos>  
- *Resumo:* <Descrição do tópico discutido, incluindo detalhes importantes e ações relevantes>  

*Dúvidas, Erros e suas Soluções ❓ - <Horário>*

- *Solicitado por:* <Nome do participante que levantou a dúvida ou relatou o erro>  
- *Respondido por:* <Nome(s) dos participantes que ofereceram soluções ou respostas>
- *Resumo:* <Descrição do problema ou dúvida e as soluções ou respostas apresentadas.> 

*Resumo geral do período 📊:*
- <Resumo curto e objetivo sobre o tom geral das interações ou assuntos discutidos no período.>

*Links do Dia🔗:*
- <Caso sejam compartilhados links importantes, liste-os aqui com data e contexto.>

*Conclusão 🔚:*
- <Conclua destacando o ambiente do grupo ou a produtividade das interações.>
</template>

Mensagens do grupo para análise:

<msgs>
{msgs}
</msgs>



            """,
            expected_output=(
                "Um resumo segmentado de acordo com o template fornecido, contendo apenas informações "
                "relevantes extraídas das mensagens fornecidas."
            ),
            agent=self.agent,
        )

        # Configurar o crew
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,  # Processa as tarefas em sequência
        )

    def kickoff(self, inputs):
        """
        Executa o processo de resumo de mensagens.

        Args:
            msgs (str): Mensagens de WhatsApp para processar.

        Returns:
            str: O resumo gerado no formato esperado.
        """
        result = self.crew.kickoff(inputs=inputs).raw
        return result
