from crewai.flow.flow import Flow, start, listen, router
from crewAnalyzer import crewAnalyzer
from crewPostagem import CrewPostagem
from pydantic import BaseModel


class ReflectionState(BaseModel):
    topico: str =''
    ideia: str =''
    critica: str = ''
    tentativas: int = 0
    logs: str = ""
    
class ReflectionFlow(Flow[ReflectionState]):
   
    @start()
    def inicio(self):
        self.state.ideia = ''
        self.state.critica = ''
        self.state.tentativas=0
        self.state.logs = "Start OK\n"
        return self.state
    
    @listen(inicio)
    def idealista(self):
        crew = CrewPostagem()
        ideia = crew.kickoff(inputs={
            'topic' : self.state.topico,
            'ideia' : self.state.ideia,
            'critica' : self.state.critica
        })
        self.state.ideia = ideia
        self.state.logs += "Idealista OK\n"
    

    @router(idealista)
    def analisador(self):
        crew = crewAnalyzer()
        critica = crew.kickoff(inputs={
            'topic' : self.state.topico,
            'ideia' : self.state.ideia,
            'critica' : self.state.critica,
            'objetivo' : 'Texto para shorts youtube'
        })
        self.state.critica = critica
        self.state.logs += "Analisador OK\n"
        self.state.tentativas += 1
        if self.state.tentativas > 1 or 'perfeito' in self.state.critica.lower():
            return "completed"
        else:
            return "inicio"
    
    @listen("completed")
    def sucesso(self):
        print('Reflexao feita com sucesso')
        print(f'Ideia final: {self.state.ideia}')
        print (f'Critica final: {self.state.critica}')
        return self.state
        
        

reflection = ReflectionFlow()

states = reflection.kickoff(inputs={
    'topico' : 'IA no COMEX'  
})

# print(f"Logs: {states.logs}")
print(f"Ideia: {states.ideia}")