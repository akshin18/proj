import requests
import pytest


def test_register():
    data = {
        "username":"test2",
        "first_name":"test",
        "last_name":"test",
        "middle_name":"test",
        "birth_date":"test",
        "email":"test",
        "phone":"test",
        "address":"test",
        "position":1,
        "pwd":"test",
        "project":"test"
    }
    r = requests.post("http://127.0.0.1:5000/register",json=data)
    print(r.text)
    # assert r.json == {"status":1,"message":"Successfully registered"}
    assert r.status_code == 200

