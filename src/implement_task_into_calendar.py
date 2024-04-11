from datetime import datetime, timedelta
from googleapiclient.errors import HttpError
import re

def insert_tasks_into_calendar(service, calendar_id, array_available_periods, tasks):
    for task in tasks:
            lastimplentday = ''
            for period in array_available_periods:
                if lastimplentday != period['date']:
                    start_time = datetime.fromisoformat(period['start_time'])
                    end_time = datetime.fromisoformat(period['end_time'])
                    day = start_time.strftime("%A").lower()
                    if task['day'].lower() == day:
                        time_match = re.match(r'OverLimit (\d+:\d+\s*(?:[ap]m)?)', task['type'])
                        if time_match:
                            task_start_time = datetime.strptime(time_match.group(1), '%I:%M%p')
                            task_start_time = task_start_time.replace(year=start_time.year, month=start_time.month, day=start_time.day)
                            if task_start_time < start_time:
                                task_start_time += timedelta(days=1)
                        else:
                            task_start_time = start_time
                            task_start_time = task_start_time.replace(year=start_time.year, month=start_time.month, day=start_time.day)
                            if task_start_time < start_time.replace(hour=8,minute=0):
                                continue
                            if task_start_time > start_time.replace(hour=22,minute=0):
                                continue
                            if task_start_time + timedelta(hours=task['duration']) > end_time.replace(hour=22,minute=0):
                                continue
                        if task_start_time >= start_time and task_start_time + timedelta(hours=task['duration']) <= end_time:
                            event_start_time = task_start_time
                            event_end_time = task_start_time + timedelta(hours=task['duration'])
                        else:
                            continue
                        event = {
                            'summary': task['title'],
                            'start': {'dateTime': event_start_time.isoformat(), 'timeZone': 'Europe/Paris'},
                            'end': {'dateTime': event_end_time.isoformat(), 'timeZone': 'Europe/Paris'},
                            'description': f'Type: {task["type"]}, Duration: {task["duration"]} hours, Priority: {task["priority"]}'
                        }

                        try:
                            service.events().insert(calendarId=calendar_id, body=event).execute()
                            print(f'Task "{task["title"]}" scheduled for {day} from {event_start_time.time()} to {event_end_time.time()}')
                            if end_time == event_end_time or start_time == event_end_time + timedelta(minutes=15):
                                array_available_periods.remove(period)
                            else:
                                event_end_time = event_end_time + timedelta(minutes=15)
                                period['start_time'] = event_end_time.isoformat()
                            lastimplentday = period['date']
                        except HttpError as error:
                            print(f"An HTTP error occurred: {error}")
                            print(f"Error details: {error.content}")