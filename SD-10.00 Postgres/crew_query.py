from MyLLM import MyLLM
from crewai import Agent, Task, Process, Crew
from crewai_tools import FileReadTool


class SQLQueryCrew:
    
    def __init__(self):
        
        self.llm=MyLLM.Ollama_qwen3_14b
        self.llm2=MyLLM.mistral_small
        self.schema_tool = FileReadTool()
        self.crew = None
        
        self.create_crew()
        
    def create_crew(self):
        self.sql_agent = Agent(
            role="Especialista em SQL",
            goal="Gerar consultas SQL precisas e otimizadas para diferentes bancos de dados.",
            backstory=(
                "Você é um renomado especialista em SQL, com conhecimento avançado em diversas bases de dados, incluindo Postgres, MySQL e SQL Server. "
                "Sua missão é interpretar descrições textuais e transformá-las em consultas SQL eficientes, sempre considerando a estrutura do banco de dados."
            ),
            tools=[self.schema_tool],
            verbose=True,
            memory=True,
            llm=self.llm        
        )
        
        self.task = Task(
            description=(
                r"""/no_think A partir do meu gerenciador {database_type}, 
                no banco de dados '{database_name}',
                e do esquema fornecido no campo 'yaml_content' 
                gere uma consulta SQL otimizada para 
                atender ao seguinte pedido: 
                
                {user_request}. 
                
                Certifique-se de usar as tabelas e colunas 
                corretas conforme a estrutura do YAML. 
                Antes de gerar a query, você deve **usar a ferramenta de leitura (Schema_Tool)** 
                para acessar o conteúdo do arquivo YAML em {yaml_path}. 
                Use essa informação como base obrigatória para decidir as tabelas 
                e colunas da consulta.
                O valor inserido em `json_output` é {json_output}.
                     --- Início do YAML ---
                        {yaml_content}
                     --- Fim do YAML ---
                IMPORTANTE:
                - **Formato de Retorno:**  
                  Se `json_output` for **True**, a consulta deve retornar os dados em formato JSON, 
                  usando as funções apropriadas para cada banco de dados:  
                    - **Postgres:** `row_to_json()` ou `json_agg()`  
                    - **MySQL:** `JSON_OBJECT()` ou `JSON_ARRAYAGG()`  
                    - **SQL Server:** `FOR JSON AUTO`  
                    - **Oracle:** `JSON_OBJECT()`  
                  Caso contrário, a consulta deve ser otimizada para um **retorno tabular tradicional**.

                - **Otimização:**  
                  - Sempre utilize **índices disponíveis** para melhorar a performance.  
                  - Se houver junções (`JOINs`), prefira **chaves indexadas** para evitar scans desnecessários.  
                  - Ordene os resultados de maneira lógica se necessário (`ORDER BY`).  
                  
                - **Considerações Específicas:**  
                  - Evite selecionar colunas desnecessárias (`SELECT *` não é recomendado).  
                  - Se a consulta precisar de filtros (`WHERE`), utilize os campos de indexação do banco de dados para maior eficiência.  
                  - Para valores nulos, utilize funções adequadas como `COALESCE()` para garantir legibilidade no resultado.  
                  
                """
            ),
            expected_output="Uma consulta SQL válida e otimizada para o banco de dados especificado.",
            agent=self.sql_agent   
        )
        
        self.clean_agent = Agent(
            role="Validador SQL",
            goal="Extrair apenas a instrução SQL limpa e executável de um texto gerado por LLM",
            backstory=(
                "Você é um assistente preciso que valida e corrige saídas de modelos LLM. "
                "Sua principal responsabilidade é garantir que a consulta SQL esteja corretamente isolada, "
                "sem explicações ou comentários adicionais. Se houver múltiplos blocos SQL, mantenha apenas o mais relevante."
            ),
            verbose=True,
            memory=True,
            llm=self.llm2
        )

        self.cleanup_task = Task(
            description=(
            """
            Extraia **apenas** a consulta SQL final, de forma limpa, sem explicações, comentários ou formatação extra.
            Revise a consulta SQL a fim de estar em coerencia ao pedido:
            {user_request}
            Regras:
            - O resultado deve conter **apenas o SQL**, pronto para ser executado.
            - Remova aspas de markdown como ```sql ou blocos ```.
            - Remova quebras de linha desnecessárias.
            - Não adicione explicações ou qualquer texto fora da query.
            - Se houver mais de uma query, mantenha **somente a principal** relacionada ao pedido original.
            """
            ),
            expected_output="Uma string contendo apenas a instrução SQL limpa e pronta para execução.",
            agent=self.clean_agent,
            context=[self.task]
            
        )
        
        self.crew = Crew(
            agents=[self.sql_agent, self.clean_agent],
            tasks=[self.task,self.cleanup_task],
            process=Process.sequential  # A execução será sequencial
        )
    
    def load_yaml_as_string(self, yaml_path: str) -> str:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return f.read()
        
    def kickoff(self,inputs):
        """
        Executa o processo de geração de consultas SQL.

        Args:
            inputs (dict): Dicionário contendo os parâmetros de entrada:
                - database_type (str): Tipo do banco de dados (Postgres, MySQL, etc.).
                - database_name (str): Nome do banco de dados.
                - yaml_path (str): Caminho do arquivo YAML contendo a estrutura do banco.
                - user_request (str): Pedido textual para gerar a consulta SQL.
                - json_output (bool): Define se a consulta deve retornar um JSON ou um formato tabular.

        Returns:
            str: A consulta SQL gerada no formato esperado.
        """
        yaml_raw = self.load_yaml_as_string(inputs["yaml_path"])
        inputs["yaml_content"] = yaml_raw        
        
        result = self.crew.kickoff(inputs=inputs).raw
        result = result.replace("sql","")  # Remover as crases triplas para evitar problemas com formatação de código
        result = result.replace("```", "")  # Remover as crases triplas para evitar problemas com formatação de código
        
        return result