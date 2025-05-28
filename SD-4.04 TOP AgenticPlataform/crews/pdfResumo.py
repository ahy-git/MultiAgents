import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import PDFSearchTool
from .tools.doclingtool import PdfReaderTool
from dotenv import load_dotenv

load_dotenv()

class CrewPDFResumo:

    def __init__(self, pdf_path):
        self.pdf_tool=PDFSearchTool(pdf_path)  
        self.llm = "gemini/gemini-2.0-flash-lite"  # Configuração do modelo LLM
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Definindo o agente resumidor
        resumidor = Agent(
            role="Especialista em Análise de Documento",
            goal="Analisar profundamente documentos PDF e criar resumos estruturados com base em seus índices e conteúdo.",
            backstory="Você é um analista textual treinado para interpretar documentos densos e organizá-los em relatórios úteis e acessíveis.",
            verbose=True,
            memory=True,
            tools=[self.pdf_tool]  # Associando a tool de leitura de PDF ao agente
        )

        # Tarefa de resumo
        resumo_tarefa = Task(
            description='''

        "Sua tarefa é realizar uma leitura analítica e estruturada de um documento PDF. Utilize a ferramenta PDFSearchTool "
        "para realizar buscas segmentadas com precisão. Siga obrigatoriamente os passos abaixo:\n\n"
        "### ETAPA 1 - IDENTIFICAR O ÍNDICE (SUMÁRIO)\n"
        "- Localize o sumário ou índice do documento usando termos como \"sumário\", \"índice\", \"conteúdo\" ou títulos numerados.\n"
        "- Extraia todos os títulos e subtítulos com suas numerações. Exemplo:\n\n"
        "    1. Introdução\n"
        "    2. Objetivos\n"
        "    3. Metodologia\n"
        "    4. Resultados\n"
        "    5. Conclusão\n\n"
        "Caso não exista um sumário explícito, deduza a estrutura com base nos títulos numerados no texto (ex: '1.', '1.1', '2.3').\n\n"
        "### ETAPA 2 - RESUMO DE CADA SEÇÃO\n"
        "- Para **cada item do índice**, faça uma busca precisa usando PDFSearchTool para encontrar a seção correspondente.\n"
        "- Resuma cada seção seguindo este modelo:\n\n"
        "**{Número e título da seção}**\n"
        "- Objetivo principal da seção:\n"
        "- Tópicos tratados:\n"
        "- Informações relevantes (ex: dados, gráficos, citações):\n"
        "- Conclusão ou ponto central:\n\n"
        "- Sempre cite ao menos 1 trecho textual original da seção, colocando entre aspas.\n\n"
        "### ETAPA 3 - RESUMO GERAL\n"
        "Ao final, escreva um resumo geral do documento com:\n"
        "- Objetivo do documento\n"
        "- Conclusões principais\n"
        "- Limitações ou recomendações finais\n\n"
        "### IMPORTANTE\n"
        "- **Nunca invente conteúdo**. Use apenas o que for extraído via busca com a ferramenta.\n"
        "- Responda no formato **estruturado em Markdown**.\n"
        "- Nunca misture seções. Cada seção deve estar claramente separada por título.\n"
        "- Mantenha linguagem objetiva, clara e técnica."
            
            ''',
            expected_output='''
        "Um relatório estruturado em Markdown com:\n"
        "1. Lista completa do sumário\n"
        "2. Um resumo por item do índice, com subtópicos obrigatórios\n"
        "3. Um resumo geral ao final\n"
        "4. Trechos textuais reais citados\n\n"
        "Formato:\n"
        "# Sumário\n"
        "- 1. Introdução\n"
        "- 2. Objetivos\n"
        "- ...\n\n"
        "## 1. Introdução\n"
        "- Objetivo: ...\n"
        "- Tópicos tratados: ...\n"
        "- Citação: \"...\"\n"
        "- Conclusão: ...\n\n"
        "# Resumo Geral\n"
        "- Objetivo: ...\n"
        "- Conclusões: ...\n"
        "- Recomendações: ..." 
        
        ''',
            agent=resumidor
        )

        # Criando o Crew
        return Crew(
            agents=[resumidor],
            tasks=[resumo_tarefa],
            process=Process.sequential
        )

    def kickoff(self):
        # Executa o Crew com o caminho do PDF como entrada
        resposta = self.crew.kickoff()
        return resposta.raw
