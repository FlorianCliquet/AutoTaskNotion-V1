from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
import random

def insert_projects_into_calendar(service, calendar_id, array_available_periods, projects,total_iterations=0):
    print("Inserting projects into calendar..." , total_iterations)
    if total_iterations > 1000:
        return
    for period in array_available_periods:
        total_iterations += 1

        if len(projects) == 0:
            break
        start_time = datetime.fromisoformat(period['start_time'])
        end_time = datetime.fromisoformat(period['end_time'])
        if start_time <= start_time.replace(hour=8):
            start_time = start_time.replace(hour=8,minute=0)
        if start_time >= start_time.replace(hour=22):
            continue
        if end_time >= end_time.replace(hour=22):
            end_time = end_time.replace(hour=22,minute=0)
        duration = end_time - start_time

        if duration > timedelta(hours=1):
            if duration >= timedelta(minutes=180):
                event_start_time = start_time
                event_end_time = start_time + timedelta(minutes=180)
            else:
                event_start_time = start_time
                event_end_time = end_time
            weights = [1 / (int(project['priority']) + 1) for project in projects]
            chosen_project = random.choices(projects, weights=weights, k=1)[0]
            event = {
                'summary': chosen_project['title'],
                'start': {'dateTime': event_start_time.isoformat(), 'timeZone': 'Europe/Paris'},
                'end': {'dateTime': event_end_time.isoformat() , 'timeZone': 'Europe/Paris'},
                'description': f'Duration: {duration} hours, Priority: {chosen_project["priority"]}, Since: {chosen_project["since"]}'
            }

            try:
                service.events().insert(calendarId=calendar_id, body=event).execute()
                day = event_start_time.strftime("%A").lower()
                print(f'Task "{chosen_project["title"]}" scheduled for {day} from {event_start_time.time()} to {event_end_time.time()}')
                if end_time == event_end_time or start_time == event_end_time + timedelta(minutes=15):
                    array_available_periods.remove(period)
                else :
                    event_end_time = event_end_time + timedelta(minutes=15)
                    period['start_time'] = event_end_time.isoformat() 
            except HttpError as error:
                print(f"An HTTP error occurred: {error}")
                print(f"Error details: {error.content}")
        else:
            continue

    duration_restante = [f for f in array_available_periods if (datetime.fromisoformat(f['end_time']) - datetime.fromisoformat(f['start_time'])).total_seconds() > 3600]
    if duration_restante:
        insert_projects_into_calendar(service, calendar_id, duration_restante, projects,total_iterations)