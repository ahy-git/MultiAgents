from crewai import Agent, Task, Crew, Process
from MyLLM import MyLLM

class FacadeCrew:
    def __init__(self):
        self.agent = None
        self.task= None
        self.crew=None
        self.llm = MyLLM.geminiflash20
        
        self._setup_crew()
        
    def _setup_crew(self):
        self.agent = Agent(
            role="Classificador de Text",
            goal=( "Classificar um texto em duas categorias: "
            "'Vendas' ou 'trivialidades'"),
            backstory=(
                                "Você é um especialista em análise de linguagem, capaz de interpretar textos "
            "e classificá-los de acordo com o contexto: vendas ou trivialidades. A palavra deve estar em minúsculas."
            ),
            memory=False,
            verbose=True,
            llm=self.llm
        )
        
        self.task = Task(
            description=(
            r"""Determine se o texto delimitado por <texto> ele fala sobre: 
            'vendas' (assuntos relacionados a produtos, clientes, etc.), 
            
            'trivialidades' (qualquer outro tema). 
            Forneça uma classificação com somente uma palavra: 'vendas' ou 'trivialidades. A palavra deve estar em minúsculas.'.
            <texto>
                {text}
            </texto>
            """
        ),
        expected_output=(
                "Retorne somente uma das categorias: 'vendas' ou 'trivialidades'. Nao retorna aspas '"
            ),
        agent=self.agent
        )
        
        self.crew = Crew(
            agents=[self.agent],
            tasks = [self.task],
            process = Process.sequential
        )
    
    def kickoff(self,text):
        result = self.crew.kickoff(inputs={"text": text})
        return result.raw