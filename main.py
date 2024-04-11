from datetime import datetime as dt, timedelta
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from collections import defaultdict
from src.calculate_free_slot import calculate_available_periods
from src.fetch_notion import get_tasks_pages
from src.implement_task_into_calendar import insert_tasks_into_calendar
from src.implement_project_into_notion import insert_projects_into_calendar
from src.fetch_notion import get_projet_pages
import os
import pytz
paris_timezone = pytz.timezone('Europe/Paris')
load_dotenv()
notion_api_key = os.getenv('NOTION_API')
notion_projet_id = os.getenv('PROJET_ID')
notion_task_id = os.getenv('TASK_ID')

SCOPES = ["https://www.googleapis.com/auth/calendar"]

headers = {
    'Authorization': "Bearer " + notion_api_key,
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}
def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_busy_periods(calendar_service, calendar_id, start_time, end_time):
    busy_periods = []
    events_by_day = defaultdict(list)
    try:
        event_result = calendar_service.events().list(
            calendarId=calendar_id,
            timeMin=start_time,
            timeMax=end_time,
            timeZone='Europe/Paris',
            maxResults=1000,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        for event in event_result.get('items', []):
            start_date = event['start'].get('date') or event['start'].get('dateTime').split('T')[0]
            events_by_day[start_date].append(event)

        sorted_events_by_day = sorted(events_by_day.items())

        for date, events in sorted_events_by_day:
            for event in events:
                start_time = event['start'].get('dateTime').split('T')[0] + 'T' + event['start'].get('dateTime').split('T')[1][:8]
                end_time = event['end'].get('dateTime').split('T')[0] + 'T' + event['end'].get('dateTime').split('T')[1][:8]
                busy_periods.append({
                    'date': date,
                    'summary': event['summary'],
                    'start_time': start_time,
                    'end_time': end_time
                })
            print()
    except HttpError as error:
        print(f"An HTTP error occurred: {error}")
        print(f"Error details: {error.content}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return busy_periods



def main():
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    
    now = dt.now(pytz.utc).astimezone(paris_timezone).isoformat() 
    end_time = (dt.now(pytz.utc) + timedelta(days=15)).astimezone(paris_timezone).isoformat() 
    
    busy_periods_primary = get_busy_periods(service, "primary", now, end_time)
    busy_periods_imported = get_busy_periods(service, "f41aqv7cglva98cfr3m5k2sviovu26cc@import.calendar.google.com", now, end_time)
    
    busy_periods = busy_periods_primary + busy_periods_imported
    sorted_busy_periods = sorted(busy_periods, key=lambda x: (x['date'], x['start_time']))
    
    available_periods = calculate_available_periods(sorted_busy_periods,service, "primary")
    notion_data = get_tasks_pages(notion_task_id)
    insert_tasks_into_calendar(service, "primary", available_periods, notion_data)
    print("Tasks have been scheduled successfully!")
    projects_data = get_projet_pages(notion_projet_id)
    insert_projects_into_calendar(service, "primary", available_periods, projects_data)
    print("Projects have been scheduled successfully!")
if __name__ == "__main__":
    main()