# gmail_reader_tool.py
from crewai.tools import BaseTool
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

class GmailReaderTool(BaseTool):
    name: str  =  "Gmail Inbox Tool"
    description: str = "Lê e-mails recentes do usuário e retorna os mais importantes."

    def _get_service(self):
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        token_path = 'token.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('clientSecret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def _list_messages(self, service, query='is:unread', max_results=50):
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        return results.get('messages', [])
    
    def _parse_message(self, msg_data):
        snippet = msg_data.get("snippet", "")
        headers = msg_data.get('payload', {}).get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'Sem assunto')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Remetente desconhecido')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Data desconhecida')

        return {
            "remetente": sender,
            "assunto": subject,
            "resumo": snippet,
            "data": date
        }

    def _get_message_content(self, service, msg_id):
        msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        parsed = self._parse_message(msg_data)
        return f"De: {parsed['remetente']}\nAssunto: {parsed['assunto']}\nResumo: {parsed['resumo']}"


    def _run(self, query="is:unread newer_than:3d"):
        service = self._get_service()
        messages = self._list_messages(service, query)
        if not messages:
            return "Nenhum e-mail encontrado."

        structured_emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
            structured_emails.append(self._parse_message(msg_data))

        return structured_emails



# TESTE LOCAL INDEPENDENTE
if __name__ == "__main__":
    print("Executando leitura de e-mails...")
    tool = GmailReaderTool()
    resultado = tool._run()
    print(resultado)
