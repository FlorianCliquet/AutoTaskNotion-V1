from datetime import datetime as dt, timedelta
from googleapiclient.errors import HttpError

def calculate_available_periods(busy_periods, service, calendar_id):
    available_periods = []
    launch_scheduled_days = set() 

    for i, busy_period in enumerate(busy_periods):
        start_time = dt.fromisoformat(busy_period['start_time'])
        end_time = dt.fromisoformat(busy_period['end_time'])
        date = dt.strptime(busy_period['date'], '%Y-%m-%d').date()

        if start_time.weekday() == 4: 
            if end_time.hour > 17 or (end_time.hour == 17 and end_time.minute > 0):
                end_time = end_time.replace(hour=17, minute=0, second=0, microsecond=0)

        if i == 0:
            if start_time.time() > dt.min.time():
                available_periods.append({
                    'date': date.isoformat(),
                    'start_time': dt.combine(date, dt.min.time()).isoformat(),
                    'end_time': start_time.isoformat()
                })

        if i > 0:
            previous_end_time = dt.fromisoformat(busy_periods[i - 1]['end_time'])
            if start_time > previous_end_time:
                if previous_end_time.date() != date:
                    available_periods.append({
                        'date': previous_end_time.date().isoformat(),
                        'start_time': previous_end_time.isoformat(),
                        'end_time': dt.combine(previous_end_time.date(), dt.max.time()).isoformat()
                    })
                    available_periods.append({
                        'date': date.isoformat(),
                        'start_time': dt.combine(date, dt.min.time()).isoformat(),
                        'end_time': start_time.isoformat()
                    })
                else:
                    available_periods.append({
                        'date': date.isoformat(),
                        'start_time': previous_end_time.isoformat(),
                        'end_time': start_time.isoformat()
                    })

        if i == len(busy_periods) - 1:
            if end_time.time() < dt.max.time():
                available_periods.append({
                    'date': date.isoformat(),
                    'start_time': end_time.isoformat(),
                    'end_time': dt.combine(date, dt.max.time()).isoformat()
                })
    last_period = get_last_period_per_day(available_periods)
    schedule_diner_backhome_tasks(available_periods,last_period,service,calendar_id)
    for period in available_periods:
        date = dt.fromisoformat(period['date']).date()
        if date.weekday() == 4:
            period_start = dt.fromisoformat(period['start_time'])
            period_end = dt.fromisoformat(period['end_time'])
            now = dt.now()
            five_pm = now.replace(hour=17, minute=0, second=0, microsecond=0).time()
            if period_start.time() >= five_pm or period_end.time() >= five_pm:
                available_periods.remove(period)
        if date not in launch_scheduled_days:
            period_start = dt.fromisoformat(period['start_time'])
            period_end = dt.fromisoformat(period['start_time']) + timedelta(minutes=45)
            now = dt.now()
            eleven_am = now.replace(hour=11, minute=0, second=0, microsecond=0).time()
            two_pm = now.replace(hour=14, minute=0, second=0, microsecond=0).time()
            if period_end.time() < dt.fromisoformat(period['end_time']).time():
                if period_start.time() >= eleven_am and period_end.time() <= two_pm: 
                    if (period_end - period_start).total_seconds() >= 2700: 
                        schedule_lunch_task(service, calendar_id, period_start, period_end)
                        period['start_time'] = period_end.isoformat()
                        launch_scheduled_days.add(date)

    return available_periods

def schedule_lunch_task(service, calendar_id, start_time, end_time):
    event = {
        'summary': 'Lunch',
        'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Europe/Paris'},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Europe/Paris'},
    }

    try:
        service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f'Launch task scheduled from {start_time.time()} to {end_time.time()}')
    except HttpError as error:
        print(f'An error occurred: {error}')

def get_last_period_per_day(available_period):
    scheduled_days = dict()
    for period in available_period:
        date = dt.fromisoformat(period['date']).date()
        if date.weekday() != 4:
            period_start_time = dt.fromisoformat(period['start_time']).time()
            if date not in scheduled_days or scheduled_days[date] < period_start_time:
                scheduled_days[date] = period_start_time
    return scheduled_days

def schedule_diner_backhome_tasks(array_available,last_period, service, calendar_id):
    now = dt.now()
    task_added = {}
    five_pm = now.replace(hour=17, minute=0, second=0, microsecond=0).time()
    seven_quarter_pm = now.replace(hour=19, minute=15, second=0, microsecond=0).time()
    five_quarter_pm = now.replace(hour=17, minute=15, second=0, microsecond=0).time()
    seven_half_pm = now.replace(hour=19, minute=30, second=0, microsecond=0).time()
    for period in last_period:
        chill = False
        for array in array_available:
                array_date = dt.fromisoformat(array['date']).date()
                array_start_time = dt.fromisoformat(array['start_time']).time()
                if array_date == period and array_start_time == last_period[period] and array_date not in task_added:
                    task_added[array_date] = True
                    placeholder_date = period
                    period_time = last_period[period]
                    if period_time > five_pm:
                        start_time = dt.combine(placeholder_date, seven_quarter_pm)
                        end_time = start_time + timedelta(hours=1, minutes=15)
                    else:
                        chill = True
                        start_time_chill = dt.combine(placeholder_date, five_quarter_pm)
                        end_time_chill = start_time_chill + timedelta(hours=2)
                        start_time = dt.combine(placeholder_date, seven_half_pm)
                        end_time = start_time + timedelta(hours=1)
                    event_diner = {
                                'summary': 'Diner',
                                'start': {'dateTime': start_time.isoformat(), 'timeZone': 'Europe/Paris'},
                                'end': {'dateTime': end_time.isoformat(), 'timeZone': 'Europe/Paris'},
                            }
                    if chill:
                        event_chill = {
                                    'summary': 'Chill',
                                    'start': {'dateTime': start_time_chill.isoformat(), 'timeZone': 'Europe/Paris'},
                                    'end': {'dateTime': end_time_chill.isoformat(), 'timeZone': 'Europe/Paris'},
                                }
                            
                    try:
                                service.events().insert(calendarId=calendar_id, body=event_diner).execute()
                                tmp = array['end_time']
                                date = (dt.fromisoformat(event_diner['end']['dateTime']).date()).isoformat()
                                if chill:
                                    service.events().insert(calendarId=calendar_id, body=event_chill).execute()
                                    print(f'Chill task scheduled from {start_time_chill.time()} to {end_time_chill.time()}')
                                    array['end_time'] = start_time_chill.isoformat()
                                    array_available.append({
                                            'date': date,
                                            'start_time': end_time_chill.isoformat(),
                                            'end_time': start_time.isoformat()
                                        })
                                    array_available.append({
                                                'date': date,
                                                'start_time': end_time.isoformat(),
                                                'end_time': tmp
                                            })
                                else:
                                    array['end_time'] = start_time.isoformat()
                                    array_available.append({
                                                    'date': date,
                                                    'start_time': end_time.isoformat(),
                                                    'end_time': tmp
                                        })
                                print(f'Diner task scheduled from {start_time.time()} to {end_time.time()}')
                    except HttpError as error:
                                print(f'An error occurred: {error}')