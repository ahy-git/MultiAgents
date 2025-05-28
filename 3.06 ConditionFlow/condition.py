from crewai.flow.flow import Flow, start, listen, or_
from pydantic import BaseModel

class State(BaseModel):
    tema: str ="IA na saude"
    info: str =''
    etapa_concluida: int = 0
    log: str= ''
    
class MyFlowOR(Flow[State]):
    @start()
    def etapa_inicial(self):
        self.state.info = f'Tema: {self.state.tema}'
        self.state.info += '\nEtapa Inicial'
        self.state.etapa_concluida += 1
    
    @listen(etapa_inicial)
    def etapa2(self):
        self.state.info += '\nEtapa2'
        self.state.etapa_concluida +=1
    
    @listen(etapa2)
    def etapa3(self):
        self.state.info +='\nEtapa 3'
        self.state.etapa_concluida +=1
    
    @listen(or_(etapa_inicial,etapa2, etapa3))
    def reg_log(self):
        etapa_atual = self.state.etapa_concluida
        self.state.log += f'Etapa {etapa_atual} concluida. State: {self.state.info}\n'
        return self.state
    
processo = MyFlowOR()
state = processo.kickoff()

# print(f'State: {state.info}')

print(f'Log: {state.log}')