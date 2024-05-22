import requests
import json

#Sensible information should be removed, this is only a test case.
BONITA_URL = "http://localhost:8080/bonita"
USERNAME = "admin"
PASSWORD = "bpm"
PROCESS_DEFINITION_ID = "your_process_definition_id"

def login(username, password):
    response = requests.post(f"{BONITA_URL}/loginservice", data={
        "username": username,
        "password": password,
        "redirect": "false"
    })
    response.raise_for_status()
    return response.cookies["JSESSIONID"]

def start_process(session_id, process_definition_id):
    headers = {"X-Bonita-API-Token": session_id}
    response = requests.post(f"{BONITA_URL}/API/bpm/process/{process_definition_id}/instantiation", headers=headers)
    response.raise_for_status()
    return response.json()["id"]

def assign_task(session_id, task_id, user_id):
    headers = {"X-Bonita-API-Token": session_id, "Content-Type": "application/json"}
    data = json.dumps({"assigned_id": user_id})
    response = requests.put(f"{BONITA_URL}/API/bpm/userTask/{task_id}", headers=headers, data=data)
    response.raise_for_status()

def get_pending_tasks(session_id, process_instance_id):
    headers = {"X-Bonita-API-Token": session_id}
    response = requests.get(f"{BONITA_URL}/API/bpm/task?c=10&p=0&f=processId={process_instance_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def assign_tasks(session_id, process_instance_id, assignments):
    pending_tasks = get_pending_tasks(session_id, process_instance_id)
    for task in pending_tasks:
        task_name = task["name"]
        if task_name in assignments:
            user_id = assignments[task_name]
            assign_task(session_id, task["id"], user_id)

user_ids = {
    "JVG": 1,
    "HYV": 2,
    "PGR": 3,
    "MFE": 4,
    "GTR": 5,
    "LPG": 6,
    "RGB": 7,
    "MDS": 8,
    "HJR": 9,
    "PTS": 10,
    "IHP": 11
}

def generate_assignments():
    assignments = []
    for i in range(20):
        assignment = {
            "T1": user_ids["JVG"],
            "T2.1": user_ids["GTR"],
            "T2.2": user_ids["MDS"],
            "T3": user_ids["PGR"],
            "T4": user_ids["MFE"]
        }
        assignments.append(assignment)
    return assignments

def main():
    session_id = login(USERNAME, PASSWORD)
    assignments_list = generate_assignments()
    
    for assignments in assignments_list:
        process_instance_id = start_process(session_id, PROCESS_DEFINITION_ID)
        assign_tasks(session_id, process_instance_id, assignments)

if __name__ == "__main__":
    main()
