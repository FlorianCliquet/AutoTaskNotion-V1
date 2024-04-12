import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = './../ConfigShit/AutoTaskNotion-V1/.env'
try:
    load_dotenv(dotenv_path)
except Exception as e:
    print(f"Error loading .env file: {e}")
notion_api_key = os.getenv('NOTION_API')
notion_projet_id = os.getenv('PROJET_ID')
notion_task_id = os.getenv('TASK_ID')

headers = {
    'Authorization': "Bearer " + str(notion_api_key),   
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28',
}

def get_tasks_pages(DATABASE_ID):
    pages = get_pages(DATABASE_ID)
    tasks = [] 
    week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for page in pages:
        props = page['properties']
        title = props.get("Task Name", {}).get("title", [{}])[0].get("plain_text", "No Title")
        type = props.get("Labels", {}).get("multi_select",[{}])[0].get("name", "No Type")
        day = props.get("Day", {}).get("select", {}).get("name", "No Date")
        duration = props.get("Duration (hours)", {}).get("number", "No Time")
        priorité = props.get("Priority", {}).get("select", {}).get("name", "No Status")
        if day == "Everyday":  
            for days in week:
                tasks.append({"title": title, "type": type, "duration": duration, "priority": priorité, "day": days})
        else:
            tasks.append({"title": title, "type": type, "duration": duration, "priority": priorité, "day": day})

    tasks.sort(key=lambda x: (week.index(x["day"]), int(x["priority"])), reverse=False)
    return tasks

def get_pages(DATABASE_ID):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size": 100}
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    with open('./src/db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    results = data.get('results', [])  
    return results

def get_projet_pages(DATABASE_ID):
    pages = get_pages(DATABASE_ID)
    projects = []  
    for page in pages:
        props = page['properties']
        title = props.get("Project Name", {}).get("title", [{}])[0].get("plain_text", "No Title")
        priority = props.get("Priority", {}).get("select", {}).get("name", "No Priority")
        since = props.get("Date", {}).get("date", {}).get("start", "No Date")
        projects.append({"title": title, "priority": priority, "since": since})  

    return projects