from crewai.flow.flow import Flow, router, start, listen
import random
from pydantic import BaseModel

class StateSample(BaseModel):
    seletor: bool = False

class FlowRouter(Flow[StateSample]):
    
    @start()
    def metodo_1(self):
        print('Inicio Fluxo')
        booleano_aleatorio = random.choice([True,False])
        self.seletor = booleano_aleatorio

    @router(metodo_1)
    def metodo_2(self):
        if self.state.seletor:
            return 'sucesso'
        else:
            return 'falha'
    
    @listen('sucesso')
    def metodo_3(self):
        print('Metodo 3 - Seletor Sucesso')
    
    @listen('falha')
    def metodo_4(self):
        print('Metodo 4 - Seletor Falha')

fluxo = FlowRouter()

state = fluxo.kickoff()
