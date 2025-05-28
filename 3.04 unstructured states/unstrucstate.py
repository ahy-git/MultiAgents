from crewai.flow.flow import Flow, listen, start

class MyUnstructuredStateFlow(Flow):
    
    @start()
    def initial_stage(self):
        # info eh um estado qualquer criado para amazenar informacao durante o fluxo
        
        self.state['info'] = 'Vamos falar sobre:' + self.state['tema']
        
        self.state['info'] += '\nInformacao gerada pela Primeira Crew'
        
        self.state['etapas_concluidas'] = 1
        
    @listen("initial_stage")
    def intermediate_stage(self):
        self.state['info'] += '\nGerada pela segunda Crew'
        self.state['etapas_concluidas'] += 1

    
    
    @listen("intermediate_stage")
    def final_stage(self):
        self.state['info'] += '\nUltima Crew'
        self.state['etapas_concluidas'] += 1
        print(f'{self.state['info']}')
        return self.state
    
processo = MyUnstructuredStateFlow()

state = processo.kickoff(inputs={'tema' : 'IA na Saude'})

print(f'Estado final: {state['info']}')

processo.plot()