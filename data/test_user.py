from requests import get, post, delete, put


print(get('http://127.0.0.1:5000/api/v2/users').json())
print(post('http://127.0.0.1:5000/api/v2/users', json={'nickname': 'Art', 'age': 100,
    'position': 'Fighter', 'address': 'Okhotny Ryad, 1', 'email': 'art@gmail.com', 'password': 'a'}).json())
print(post('http://127.0.0.1:5000/api/v2/users', json={'nickname': 'Art1', 'age': 99,
    'position': 'Fighter1', 'address': 'Okhotny Ryad, 2', 'email': 'art1@gmail.com', 'password': 'b'}).json())
print(delete('http://127.0.0.1:5000/api/v2/users/2').json())
print(delete('http://127.0.0.1:5000/api/v2/users/3').json())