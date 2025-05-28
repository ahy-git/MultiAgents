import os
from datetime import datetime, timedelta
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
]

CALENDAR_ID = os.getenv('CALENDAR_ID')


class GoogleCalendarToolInput(BaseModel):
    """Input schema for GoogleCalendarTool."""
    summary: str = Field(..., description="Summary of the event.")
    description: str = Field(
        ..., description="Description of the event containing: airline name, booking code and passenger names.")
    start_time: datetime = Field(..., description="Start time of the event.")


class GoogleCalendarTool(BaseTool):
    name: str = "Google Calendar Tool"
    description: str = "Tool to create Google Calendar Checkin events."
    args_schema: Type[BaseModel] = GoogleCalendarToolInput

    def authenticate(self):
        """Authenticate using service account for a personal Gmail account"""
        service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')
        try:
            creds = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=SCOPES
            )
            calendar_service = build('calendar', 'v3', credentials=creds)
        except Exception as e:
            print(f"Error during authentication: {e}")
            raise

        return calendar_service

    def _run(self, summary: str, description: str, start_time: datetime, end_time: datetime) -> str:
        calendar_service = self.authenticate()
        calendar_id = CALENDAR_ID

        checkin_event = {
            'summary': f"Checkin: {summary}",
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'reminders': {
                'useDefault': 'false',
                'overrides': [
                    {
                        'method': 'popup',
                        'minutes': 2880  # 2 days * 24 hours * 60 minutes
                    },
                ],
            },
        }

        try:
            # Create event
            created_event = calendar_service.events().insert(
                calendarId=calendar_id, body=checkin_event).execute()
            print(f"Event created:\n{created_event.get('htmlLink')}")

            return created_event
        except Exception as e:
            return f"Error creating events: {e}"


class GoogleCalendarFetchEventsInput(BaseModel):
    """Input schema for GoogleCalendarFetchEvents."""
    start_time: datetime = Field(...,
                                 description="Start time for fetching events.")
    end_time: datetime = Field(...,
                               description="End time for fetching events.")


class GoogleCalendarFetchEvents(BaseTool):
    name: str = "Google Calendar Fetch Events"
    description: str = "Tool to fetch Google Calendar events."
    args_schema: Type[BaseModel] = GoogleCalendarFetchEventsInput

    def authenticate(self):
        """Authenticate using service account for a personal Gmail account"""
        service_account_file = os.getenv('SERVICE_ACCOUNT_FILE')

        try:
            creds = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=SCOPES
            )
            return build('calendar', 'v3', credentials=creds)
        except Exception as e:
            print(f"Error during authentication: {e}")
            raise

    def _run(self, start_time: datetime, end_time: datetime) -> str:
        service = self.authenticate()
        calendar_id = CALENDAR_ID

        # Adjust search range to ±3 days
        search_start = start_time - timedelta(days=3)
        search_end = end_time + timedelta(days=3)

        try:
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=search_start.isoformat() + 'Z',
                timeMax=search_end.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])
            return events
        except Exception as e:
            return f"Error fetching events: {e}"