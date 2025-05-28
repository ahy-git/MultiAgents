from crewai.flow.flow import Flow, start, listen, and_
from pydantic import BaseModel

class State(BaseModel):
    info: str = ''
    tema: str = 'IA na saude'
    etapa_concluida: int =0
    validacao: str =''

class FlowAnd(Flow[State]):
    @start()
    def etapa1(self):
        self.state.info = f'{self.state.tema}'
        self.state.info += '\nEtapa 1'
        self.state.etapa_concluida += 1
    
    @listen(etapa1)
    def validar_dados1(self):
        self.state.validacao += 'Validacao 1 concluida. \n'
    
    @listen(etapa1)
    def validar_dados2(self):
        self.state.validacao += 'Validacao 2 concluida. \n'
    
    @listen(and_(validar_dados1,validar_dados2))
    def consolida_dados(self):
        self.state.info += '\nTodas validacoes ok'
        self.state.etapa_concluida =+ 1
    
    @listen(consolida_dados)
    def etapa_final(self):
        self.state.info += 'Gerado no final'
        self.state.etapa_concluida += 1
        return self.state
    
processo = FlowAnd()

states = processo.kickoff()

print(f'{states.info}')