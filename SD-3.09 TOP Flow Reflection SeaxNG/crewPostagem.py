import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from searxngtool_v2 import searxng_search

load_dotenv()

class CrewPostagem:
    def __init__(self):
        self.search_tool = searxng_search
        self.llm = 'gemini/gemini-2.0-flash-lite'
        self.crew = self._criarcrew()
    def _criarcrew(self):
        pesquisador = Agent(
            role = 'Pesquisador',
            goal="""
            Encontrar informacoes relevantes sobre {topic}.
            Se ja existir um text anterior em <text> e critica em <critic>
            use essas informacoes para guiar a pesquisa, buscando
            dados que melhores o conteudo de <text>
            Caso contrario, incie do zero, com as informacoes mais relevantes e 
            impactantes sobre {topic}.
            <text>
            {ideia}
            </text>
            <critic>
            {critica}
            </critic>
            """,
            verbose=True,
            memory=True,
            backstory="""
            Você é um pesquisador especializado em buscar informações 
            objetivas e diretas . 
            Quando houver contexto prévio , você foca em enriquecer
            e melhorar o conte údo com base nas críticas . 
            Se não houver contexto , você inicia do zero ,
            identificando os principais pontos sobre {topic}.
            """,
            llm=self.llm,
            tools = [self.search_tool]             
        )
        
        escritor = Agent (
            role ='Escritor',
            goal = """
            Criar um texto envolvente sobre {topic}.
            Se já existir um texto anterior , melhore-o com base na
            crítica .
            Caso contrário , inicie do zero criando um texto curto ,
            direto e otimizado para leitura em 1 minuto 
            """,
            backstory="""
            Você é um redator focado em criar textos curtos e
            impactantes, perfeitos para o formato de Shorts .
            Sua habilidade está em aprimorar conteúdos existentes
            ou começar do zero quando necessário.
            """,
            verbose=True,
            llm=self.llm,
            memory=True
            
        )
        
        revisor = Agent(
            role = 'Revisor',
            goal = """ 
            Revisar e otimizar o texto curto sobre {topic} para garantir 
            clareza, concisao e impacto
            """,
            backstory="""
            Você é um revisor especializado em ajustar textos
            curtos , garantindo que eles sejam diretos , impactantes e 
            perfeitos para formatos rápidos como Shorts.
            """,
            verbose= True,
            memory = True,
            llm=self.llm
        )
        
        pesquisa_tarefa = Task(
            description="""
            Pesquise informações relevantes sobre o tópico "{topic}".
            Se já houver um texto anterior em <text> e críticas
            recebidas em <critic>, use essas informações
            para guiar sua pesquisa e buscar dados que complementem
            ou melhorem o conteúdo. Caso contrário ,
            inicie do zero e encontre os principais pontos sobre o 
            tópico.
            Seu objetivo é fornecer informações concisas e
            impactantes para criação ou aprimoramento do texto .
            <text>
            {ideia}
            </text>
            <critic>
            {critica}
            </critic>
            """,
            expected_output="""
            Um resumo curto e direto sobre {topic}, contendo
            informacoes relevantes e, se necessario, enderecando as criticas
            """,
            tools=[self.search_tool],
            agent = pesquisador
        )
        
        escrita_tarefa = Task(
            description = """
            Com base nas informações pesquisadas , você escreverá
            um texto curto sobre "{topic}". 
            Se já houver algum conteúdo em <text> é
            um texto que você já escreveu anteriormente e que recebeu um
            feedback meu <critic>. 
            Por isso , melhore o texto com base no feedback. Caso
            contrário (<text> = vazio ),
            inicie do zero e encontre os principais pontos sobre o 
            tópico.
            Seu objetivo é fornecer informações concisas e
            impactantes para criação ou aprimoramento do texto.
            Otimize o texto para leitura em 1 minuto. O texto deve
            ser claro, envolvente e direto , com no máximo 200 palavras.
            <text>
            {ideia}
            </text>
            <critic>
            {critica}
            </critic>
            """,
            expected_output="""Um texto curto de ate 200 palavras criado ou 
            aprimorado com base nas criticas e no contexto""",
            agent = escritor,
            context=[pesquisa_tarefa]   
        )
        
        revisao_tarefa = Task (
            description ='Revisar o texto do contexto',
            expected_output = 'texto do contexto revisado',
            agent = revisor,
            context=[escrita_tarefa]
            
        )
        
        return Crew(
            agents=[pesquisador,escritor,revisor],
            tasks=[pesquisa_tarefa,escrita_tarefa,revisao_tarefa],
            process=Process.sequential
        )
    
    def kickoff(self,inputs):
        """
        Executa o Crew com os parâ metros fornecidos .
        inputs :
            - topic : str , o tó pico principal da postagem .
            - ideia : str , o texto anterior ou ponto de partida ( opcional ).
            - critica : str , a ú ltima crí tica feita ao texto ( opcional ).
        Returns :
            - Um texto curto , criado ou aprimorado , otimizado para leitura
            em 1 minuto .
        """
        resposta = self.crew.kickoff(inputs=inputs)
        return resposta.raw
    
    