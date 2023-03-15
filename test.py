from requests import get, post, delete, put

print(get('http://127.0.0.1:5000/api/jobs').json())  # все работает
print(get('http://127.0.0.1:5000/api/jobs/1').json())  # все работает
print(get('http://127.0.0.1:5000/api/jobs/5').json())  # нет id
print(post('http://127.0.0.1:5000/api/jobs',  # не хватает - бед рекуэст
           json={'id': 1}).json())

print(post('http://127.0.0.1:5000/api/jobs', json={'id': 43,  # все работает
                                                   'job': "doing",
                                                   "work_size": 1,
                                                   'collaborators': "1, 2",
                                                   "start_date": "2000-01-01 00:00:00",
                                                   "end_date": "2024-01-01 00:00:00",
                                                   "is_finished": False,
                                                   'team_leader': 1}).json())

print(post('http://127.0.0.1:5000/api/jobs', json={'id': 44,  # нет такого тим лида - бед рекуэст
                                                   'job': "doing",
                                                   "work_size": 1,
                                                   'collaborators': "1, 2",
                                                   "start_date": "2000-01-01 00:00:00",
                                                   "end_date": "2024-01-01 00:00:00",
                                                   "is_finished": False,
                                                   'team_leader': 5}).json())

print(post('http://127.0.0.1:5000/api/jobs'))  # нет json - <Response [400]>
print(get('http://127.0.0.1:5000/api/jobs').json())  # все работает
print(delete('http://127.0.0.1:5000/api/jobs/43').json())  # все работает
print(delete('http://127.0.0.1:5000/api/jobs/9999').json())  # не работает - нет работы
print(get('http://127.0.0.1:5000/api/jobs').json())  # все работает

print(put('http://127.0.0.1:5000/api/jobs/1', json={'id': 1,  # работает, тк id совпадают
                                                    'job': "doing1",
                                                    "work_size": 2,
                                                    'collaborators': "1",
                                                    "start_date": "2022-01-01 00:00:00",
                                                    "end_date": "2023-01-01 00:00:00",
                                                    "is_finished": False,
                                                    'team_leader': 1}).json())

print(put('http://127.0.0.1:5000/api/jobs/1', json={'id': 2,  # не работает, тк id не совпадают
                                                    'job': "doing2",
                                                    "work_size": 2,
                                                    'collaborators': "1",
                                                    "start_date": "2022-01-01 00:00:00",
                                                    "end_date": "2023-01-01 00:00:00",
                                                    "is_finished": False,
                                                    'team_leader': 1}).json())

print(put('http://127.0.0.1:5000/api/jobs/1', json={  # работает
    'job': "doing3",
    "work_size": 2,
    'collaborators': "1",
    "start_date": "2022-01-01 00:00:00",
    "end_date": "2023-01-01 00:00:00",
    "is_finished": False,
    'team_leader': 1}).json())

print(put('http://127.0.0.1:5000/api/jobs/2', json={  # не работает, тк нет работы
    'job': "doing2",
    "work_size": 2,
    'collaborators': "1",
    "start_date": "2022-01-01 00:00:00",
    "end_date": "2023-01-01 00:00:00",
    "is_finished": False,
    'team_leader': 1}).json())
print(get('http://127.0.0.1:5000/api/jobs').json())  # все работает
