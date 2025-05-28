from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class State(BaseModel):
    tema: str ='Ia na Saude'
    info: str =''
    etapas_concluidas: int = 0


class MyStrcturedFlow(Flow[State]):
    
    
    @start()
    def init_stage(self):
        self.state.info = f'Vamos falar sobre: {self.state.tema}'
        self.state.info += '\nCrew 1'
        self.state.etapas_concluidas =1
    
    @listen(init_stage)
    def int_state(self):
        self.state.info += '\nCrew 2'
        self.state.etapas_concluidas += 1
        
    @listen(int_state)
    def final_state(self):
        self.state.info += '\nCrew 3'
        self.state.etapas_concluidas += 1
        return self.state

processo = MyStrcturedFlow()

state = processo.kickoff()

print(f'Estado final: {state.info}')

processo.plot()

    
    