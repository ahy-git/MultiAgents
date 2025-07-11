import time
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel
from crew_facade import FacadeCrew
from crew_talking import TalkingCrew
from crew_sales_report import SalesReportCrew

class State(BaseModel):
    tipo_msg: bool = False
    text: str = ""
    language: str = ""
    
class FluxoAudio(Flow[State]):
    
    @start()
    def start(self):
        start_time = time.time()
        
        avaliador = FacadeCrew()
        self.state.tipo_msg = avaliador.kickoff(self.state.text)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"Runtime: {execution_time:.4f} s")
        
    @router(start)
    def roteamento(self):
        return str(self.state.tipo_msg).lower()
    
    @listen("vendas")
    def salesReport(self):

        sales = SalesReportCrew()
        resposta = sales.kickoff(self.state.text)
        
        return resposta
    
    @listen("trivialidades")
    def smallTalk(self):
        conversador = TalkingCrew()
        resposta = conversador.kickoff(self.state.text)
        
        return resposta
    

# consulta = "Analisando entre homens e mulheres, me diga quanto cada genero vendeu. Se nao houver coluna genero, identifique e analise nome por nome e crie essa nova coluna"
# fluxo = FluxoAudio()
# resposta = fluxo.kickoff(inputs={'text':consulta})
# print(resposta) 