from requests import get, post, delete

print(get('http://127.0.0.1:5000/api2/jobs').json())
print(
    post('http://127.0.0.1:5000/api2/jobs', json={'job': "doing",
                                                  "work_size": 1,
                                                  'collaborators': "1",
                                                  "start_date": "2000-01-01 00:00:00",
                                                  "end_date": "2024-01-01 00:00:00",
                                                  "is_finished": False,
                                                  'team_leader': 1}).json())
print(
    post('http://127.0.0.1:5000/api2/jobs', json={'job': "doing1",
                                                  "work_size": 1,
                                                  'collaborators': "1",
                                                  "start_date": "2000-01-01 00:00:00",
                                                  "end_date": "2022-01-01 00:00:00",
                                                  "is_finished": False,
                                                  'team_leader': 1}).json())
print(delete('http://127.0.0.1:5000/api2/jobs/2').json())
print(delete('http://127.0.0.1:5000/api2/jobs/3').json())
