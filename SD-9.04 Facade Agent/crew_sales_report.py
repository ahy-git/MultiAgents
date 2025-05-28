from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM
from custom_tool_vendas import QueryCSV
import os

class SalesReportCrew:
    def __init__(self):
        self.tool_file_path = os.path.join('vendas_ficticias_brasil.csv')
  
        self.crew=None
        self.llm = MyLLM.geminiflash20
        
        self._setup_crew()
        
    def _setup_crew(self):
        vendas_tool = QueryCSV(file_path=self.tool_file_path)
        
        analista_dados = Agent(
            role="Analista de dados",
            goal=( "Criar codigos em python que executam uma consulta em um determinado CSV"),
            backstory=(
            """Você é um analista de dados experiente, capaz de escrever códigos em Python 
            capazes de extrair informações solicitadas de conjuntos de dados estruturados como arquivos CSV."""
            ),
            memory=False,
            verbose=True,
            llm=self.llm
        )
        
        redator = Agent(
            role="Redator",
            goal=( "Escrever um paragrafo baseado no contexto fornecido pelo Analista de Dados e pela solicitacao {query}"),
            backstory=(
            """Você é um escritor habilidoso, capaz de transformar dados técnicos e análises 
            em textos claros e cativantes, sempre mantendo um tom formal e direcionado ao chefe."""
            ),
            memory=False,
            verbose=True,
            llm=self.llm
        )
                    
        task_csv = Task(
            description=(
            """
            Dada a solicitação delimitada por <query>, crie um código python que 
            irá ler o arquivo exatamente o código delimitado em <abertura>. Você 
            deve completar o código que começou em abertura de modo a atender
            a <query>. Chame a ferramenta QueryCSV para executar o código. Em <exemplo>
            tem um exemplo de um código que você deve gerar. Veja que o exemplo ja tem <abertura> nele. 
            
            <query>
            colunas=(Data da Venda,ID da Venda,ID do Cliente,Nome do Cliente,Produto,ID do Produto,Categoria,Preço Unitário,Quantidade,Valor Total,Meio de Pagamento,Vendedor,Região,Status da Venda)
            Com base nas colunas do CSV vendas_ficticias_brasil.csv escreva um código pandas para essa solicitação:\n\n
            {query}
            </query>
            
            <abertura>
            csv = os.path.join('vendas_ficticias_brasil.csv')
            df = pd.read_csv(csv)
            <abertura>
            
            <exemplo>
            import os
            import pandas as pd

            csv = os.path.join('vendas_ficticias_brasil.csv')
            # Carregue o arquivo CSV no DataFrame
            df = pd.read_csv(csv)
            
            # Verificar se o arquivo existe antes de tentar carregá-lo
            if not os.path.exists(csv):
                raise FileNotFoundError(f"O arquivo vendas_ficticias_brasil.csv não foi encontrado. Verifique o caminho!")


            # Agrupar os dados por 'Região' e somar o 'Valor Total' para cada grupo
            vendas_por_regiao = df.groupby('Região')['Valor Total'].sum()

            # Identificar a região com maior valor total de vendas
            regiao_mais_vendeu = vendas_por_regiao.idxmax()
            valor_total_mais_vendeu = vendas_por_regiao.max()

            resultado = f'A região que mais vendeu foi' + regiao_mais_vendeu + 'com um total de R$' + valor_total_mais_vendeu.'
            <exemplo>
            
            no código, sempre atribua o resultado da a variável "resultado" como mostra o <exemplo>
                    
            """
        ),
        expected_output=(
            "Um texto em um parágrafo sobre: {query}."
            ),
        agent=analista_dados,
        tools=[vendas_tool]
        )
        
        write_task = Task(
            description=(
                """
                Use o contexto fornecido pela pesquisa do agente 'analista_dados' para escrever um parágrafo
                que responda à solicitação em {query}. Explicar
                a resposta da maneira mais clara e informativa possível. quando for escrever algum número de valores 
                em reais, escreva por extenso. SEMPRE RESPONDA EM PT-BR
                """
            ),
            expected_output=(
                "Um parágrafo explicando a resposta à solicitação {query}."
            ),
            agent=redator,
            context=[task_csv]
        )
        
        self.crew = Crew(
            agents=[analista_dados,redator],
            tasks = [task_csv,write_task],
            process = Process.sequential
        )
    
    def kickoff(self,query):
        result = self.crew.kickoff(inputs={"query": query})
        return result.raw
        
        