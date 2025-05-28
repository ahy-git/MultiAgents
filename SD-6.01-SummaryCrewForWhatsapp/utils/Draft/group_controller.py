import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"...")))

#group_manager.py
import os
from dotenv import load_dotenv
from datetime import datetime
from evolutionapi import EvolutionClient
from group import Group
import pandas as pd
from receiveWhatsapp import MessageWhatsapp
from task_scheduler import TaskScheduled

load_dotenv()

class Group_controller:
    def __init__(self):
        """Inicializa o gerenciador de groups para a EvoAPI"""
        self.base_url = os.getenv("EVO_API_URL", "http://localhost:8081")
        self.api_token = os.getenv("EVO_API_TOKEN")
        self.instance_id = os.getenv("EVO_INSTANCE_NAME")
        self.instance_token = os.getenv("EVO_INSTANCE_TOKEN")
        
        paths_this = os.path.dirname(__file__)
        
        self.csv_file = os.path.join(paths_this,"group_summary.csv")
        
        if not all ([self.base_url, self.api_token, self.instance_id, self.instance_token]):
            raise ValueError(
                "Variaveis url, token, instance id e instance token nao foram configuradas"
            )
            
        self.client = EvolutionClient(base_url=self.base_url,api_token=self.api_token)
        self.groups = []
        
    def load_summary_info(self):
        """
        Carrega ou cria DataFrame com informacoes de resumo dos grupos
        """
        try:
            return pd.read_csv(self.csv_file)
        except:
            #se nao existir o arquivo, cria o DF vazio
            return pd.DataFrame(columns=["group_id","dias","horario",
                                         "enabled","is_links","is_names"])
    
    def load_data_by_group(self, group_id):
        try:
            df = self.load_summary_info()
            resumo = df[df["group_id"] == group_id]
            
            if not resumo.empty:
                resumo = resumo.iloc[0].to_dict()
            else:
                resumo = False
        except Exception as e:
            resumo = False
        
        return resumo
    
    def fetch_groups(self):
        """
        Busca todos os groups da instance, atualiza lista interna e carrega dados de resumo.
        """
        
        summary_data = self.load_summary_info()
        
        groups_data = self.client.group.fetch_all_groups(
            instance_id = self.instance_id,
            instance_token = self.instance_token,
            get_participants = False
        )
        
        #atualiza lista de groups
        self.groups = []
        
        for group in groups_data:
            group_id = group["id"]
            
            #dados de resumo se existir no csv
            resumo = summary_data[summary_data["group_id"] == group_id]
            
            if not resumo.empty:
                resumo = resumo.iloc[0].to_dict()
                horario = resumo.get("horario","22:00")
                enabled = resumo.get("enabled",False)
                is_links = resumo.get("is_links",False)
                is_names = resumo.get("is_names",False)
            else:
                horario = "22:00"
                enabled: False
                is_links = False
                is_names = False
                
            self.groups.append(
                Group(
                    group_id= group_id,
                    name = group["subject"],
                    subject_owner=group["subjectOwner"],
                    subject_time=group["subjectTime"],
                    picture_url=group.get("pictureUrl",None),
                    size=group["size"],
                    creation = group["creation"],
                    owner=group["owner"],
                    restrict = group["restrict"],
                    announce = group["announce"],
                    is_community=group["isCommunity"],
                    is_community_announce=group["isCommunityAnnounce"],
                    horario=horario,
                    enabled=enabled,
                    is_links=is_links,
                    is_names=is_names,
                )
                
            )
            return self.groups
        
    def update_summary(self,
                       group_id,horario,enabled,is_links,is_names,script):
        """Atualiza ou adicionar config de resumos aos csv"""
        
        try:
            df = self.load_summary_info()
            
            if group_id in df["group_id"].values:
                df.loc[df["group_id"] == group_id, ["horario","enabled","is_links","is_names"]] = [horario,enabled,is_links,is_names]
            else:
                nova_linha = {
                    "group_id": group_id,
                    "horario" : horario,
                    "enabled" : enabled,
                    "is_links" : is_links,
                    "is_names" : is_names
                }
                df = pd.concat([df,pd.DataFrame([nova_linha])],ignore_index=True)
            task_name = f"ResumoGrupo_{group_id}"
            try:
                TaskScheduled.delete_task(task_name)
            except Exception as e:
                pass

            if enabled:
                python_script = os.path.join(script)
                
                TaskScheduled.create_task(
                    task_name,
                    python_script,
                    schedule_type='Daily',
                    time=horario
                )
                
            TaskScheduled.list_tasks()
        
            df.to_csv(self.csv_file, index=False)
        
            return True
        except Exception as e:
            print(f'Erro ao salvar config: {e}')
            return False
        
    def get_groups(self):
        """Retorna lista de groups"""
        return self.groups
    
    def find_group_by_id(self,group_id):
        
        if not self.groups:
            self.groups = self.fetch_groups()
        
        for group in self.groups:
            if group.group_id == group_id:
                return group
            return None
    
    def filter_groups_by_owner(self,owner):
        return [group for group in self.groups if group.owner== owner]
    
    def get_message(self, group_id, start_date, end_date):
        
        def to_iso8601(date_str):
            dt = datetime.strptime(date_str,"%Y-%m-%d %H:%M:%S")
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        timestamp_start = to_iso8601(start_date)
        timestamp_end = to_iso8601(end_date)
        
        group_messages = self.client.chat.get_messages(
            instance_id = self.instance_id,
            remote_jid=group_id,
            instace_token=self.instance_token,
            timestamp_start = timestamp_start,
            timestamp_end = timestamp_end,
            page =1,
            offset=1000
        )
        
        msgs = MessageWhatsapp.get_text(group_messages)
        
        data_obj = datetime.strptime(timestamp_start,"%Y-%m-%dT%H:%M:%SZ")
        
        timestamp_limite = int(data_obj.timestamp())
        
        msg_filtradas = []
        for msg in msgs:
            if msg.message_timestamp >= timestamp_limite:
                msg_filtradas.append(msg)
        
        return msg_filtradas
        
    
    