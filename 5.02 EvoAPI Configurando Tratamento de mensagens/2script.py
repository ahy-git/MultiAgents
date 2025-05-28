from utils.sendWhatsapp import SendWhatsapp

mensagem = SendWhatsapp()

response = mensagem.textMessage('5511984617987',"teste funcao")

print(response)