from crewai.flow.flow import Flow, listen, start

class SimpleFlow(Flow):
    @start()
    def saudacao(self):
        # aqui pode ser uma crew inteira
        print('Iniciando Flow')
        msg = "Hello World"
        print(msg)
        
        return msg

    @listen(saudacao)
    def get_number(self, mensagem):
        #aqui uma segunda crew espera saida ca primeira
        
        print (f'mensagem para o user: {mensagem}')
        
        #solicita 2 numeros para o usuario
        
        num1 = int(input('Digite o primeiro numero:'))
        num2 = int(input('Digite o segundo numero:'))
        
        print(f'Numeros recebidos: {num1} e {num2}')
        
        return num1, num2
    
    @listen(get_number)
    def calc_sum(self, numeros):
        #aqui uma terceira crew que termina o processo
        num1 = numeros[0]
        num2 = numeros[1]
        soma = num1 + num2 
        print(f'resultado da soma eh {soma}')
        return soma

fluxo =SimpleFlow()

results = fluxo.kickoff()

print (f'Resultado final: {results}')