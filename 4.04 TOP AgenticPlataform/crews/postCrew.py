import os
from crewai import Agent, Task, Crew, Process
from .tools.searxngtool_v2 import searxng_search
from .tools.remotescraper import RemoteScraperTool
from dotenv import load_dotenv

load_dotenv()

class crewPost:
    def __init__(self):
        self.search_tool = searxng_search
        self.scrape_tool = RemoteScraperTool()
        self.llm = 'gemini/gemini-2.0-flash-lite'
        self.crew = self._criarCrew()
    
    def _criarCrew(self):
        # agents
        pesquisador = Agent(
            role = 'Pesquisador',
            goal = 'Encontrar informacoes relevantes sobre {topic}',
            verbose=True,
            memory=True,
            backstory = """
            Você é um pesquisador especializado em
            descobrir informações úteis e relevantes
            para escrever sobre {topic}.
            """,
            tools = [self.search_tool,self.scrape_tool]
        )
        
        escritor = Agent(
            role = 'Escritor',
            goal = 'Criar uma postagem convincente sobre {topic}',
            verbose=True,
            memory=True,
            backstory="""
            Vc eh um redator experiente que transforma 
            informacoes em conteudos interessantes e informativos
            """            
        )
        
        revisor = Agent(
            role = 'Revisor',
            goal = 'Revisar e melhorar a postagem sobre {topic}',
            verbose=True,
            memory = True,
            backstory = """
            Você é um revisor detalhista ,
            especializado em ajustar o tom ,
            a clareza e a gramática de textos .
            """   
        )
        pesquisa_tarefa = Task(
            description = """
            Busque sites com informacoes sobre {topic} usando a search_tool
            Para cada site encontrado, obtenha informacoes 
            detalhadas usando a ferramenta de scrapear scrape_tool - envie a url.
            Foque em identificar pontos importantes e um resumo geral.
            """,
            expected_output = 'Um resumo detalhado sobre {topic}',
            tools = [self.search_tool, self.scrape_tool],
            agent=pesquisador            
        )
        
        escrita_tarefa = Task(
            description = """
            Escreva uma postagem com base no conteudo pesquisado.
            A postagem deve ser clara, interessante e envolvent.
            """,
            expected_output="Uma postagem completa sobre {topic} com 3 paragrafos",
            agent=escritor,
            context=[pesquisa_tarefa]
        )
        
        revisao_tarefa = Task(
            description="""
            Reveja a postagem criada, ajustando a clareza e corrigindo possiveis erros
            """,
            expected_output="Uma postagem revisada e otimizada",
            agent = revisor,
            context=[escrita_tarefa]
            
        )
        
        return Crew(
            agents=[pesquisador,escritor,revisor],
            tasks = [pesquisa_tarefa,escrita_tarefa,revisao_tarefa],
            process=Process.sequential
        )
        
    def kickoff(self,inputs):
        resposta = self.crew.kickoff(inputs=inputs)
        return resposta.raw