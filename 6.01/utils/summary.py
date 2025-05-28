import sys
import os
import time
import argparse
from datetime import datetime, timedelta
from group_controller import GroupController
from summary_crew import SummaryCrew
from sendWhatsapp import SendWhatsapp
from groups_util import GroupUtils
import requests
from dotenv import load_dotenv



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("COMEÇANDO A EXECUTAR O SCRIPT\n")
print("AGUARDE...\n")

try:
    # Define o argumento para o nome da tarefa
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_name", required=True, help="Nome da tarefa agendada")
    args = parser.parse_args()

    #group_id = '120363372879654391@g.us' 

    group_id = args.task_name.split("_")[1]

    control = GroupController()
    df = control.load_data_by_group(group_id)

    nome = control.find_group_by_id(group_id).name

    print("----------------------\n")
    print("EXECUTANDO TAREFA AGENDADA\n")
    print(f"Resumo do grupo : {nome}\n")

    if df['enabled'] == True:
        
        # Obtém a data e hora atual
        data_atual = datetime.now()

        # Calcula a data de 1 dia anterior
        data_anterior = data_atual - timedelta(days=1)

        # Formata as datas no formato desejado
        formato = "%Y-%m-%d %H:%M:%S"
        data_atual_formatada = data_atual.strftime(formato)
        data_anterior_formatada = data_anterior.strftime(formato)

        # Exibe os resultados
        print(f"Data atual: {data_atual_formatada}")
        print(f"Data de 1 dia anterior: {data_anterior_formatada}")
            
        msgs = control.get_messages(group_id, data_anterior_formatada, data_atual_formatada)
            
        cont = len(msgs)
        
        print(f"Total de mensagens: {cont}")
        
        time.sleep(20)
            
        pull_msg = f"""
            Dados sobre as mensagens do grupo
            Data Inicial: {data_anterior_formatada}
            Data Final: {data_atual_formatada}
            
            
            MENSAGENS DOS USUÁRIOS PARA O RESUMO:
            --------------------------
            
            """
            
        for msg in reversed(msgs):
                
                pull_msg = pull_msg + f"""
                Nome: *{msg.get_name()}*
                Postagem: "{msg.get_text()}"  
                data: {time.strftime("%d/%m %H:%M", time.localtime(msg.message_timestamp))}'     
                """            

        print(pull_msg)
        
        inputs = {
            "msgs": pull_msg
        }
        
        
        summary_crew = SummaryCrew()
        resposta = summary_crew.kickoff(inputs=inputs)
        respostaNothink = GroupUtils.remove_think_section(resposta)
        respostaTitulo = "*"+nome+"*" + "\n" + respostaNothink
        
        evo_send = SendWhatsapp()
        summaryGroup = "120363419901558061@g.us" # Grupo para enviar os resumos - Resumos Grupo 
        evo_send.textMessage(summaryGroup, respostaTitulo)


        log_path = os.path.dirname(__file__)
        # Nome do arquivo log será gravado
        nome_arquivo = os.path.join(log_path, "log_summary.txt")

        # Abre o arquivo no modo de escrita
        with open(nome_arquivo, "a", encoding="utf-8") as arquivo:
            # Escreve o poema no arquivo
            
            log = f"""[{data_atual}] [INFO] [GRUPO: {nome}] [GROUP_ID: {group_id}] - Mensagem: Resumo gerado e enviado com sucesso!"""
            arquivo.write(log)
            
except Exception as e:
    print(f"Erro: {e}")
    load_dotenv()
    chatID = os.getenv("TELEGRAM_CHAT_ID")
    telegramAPIToken=os.getenv("TELEGRAM_API_TOKEN")
    requests.post(f"https://api.telegram.org/bot{telegramAPIToken}/sendMessage", 
                  data={"chat_id": chatID, "text": f"Erro ao enviar processar resumo {e}"})
