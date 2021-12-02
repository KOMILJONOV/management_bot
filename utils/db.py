import requests
from sqlite3 import *
# from constants import *
host = "http://192.168.0.188:8000"


def request_authorization(user_id: str, name_surname: str, description: str, number, user_name: str):
    res = requests.get(f'{host}/create_request/', json={
        "name": str(name_surname),
        "phone": str(number),
        "chat_id": str(user_id),
        "desc": str(description),
        "username": str(user_name)
    })
    if res.status_code == 200:
        return res.json()
    else:
        return None


def check_request_status(user_id: int):
    res = requests.get(f'{host}/check_user/', json={
        "chat_id": user_id
    }).json()
    return res


# check_user(2343434)

def get_request_types() -> list:
    res = requests.get(f'{host}/get_request_types/').json()
    return res['data']


def get_admins_list(user_id: int):
    res = requests.get(f'{host}/admin_list/', json={
        "chat_id": user_id
    })
    return res.json()['data']


def accept_request_admin(user_id: int, req: int) -> bool:
    res = requests.get(f'{host}/update_status/', json={
        "admin": user_id,
        "rq": req,
        "status": 1
    })
    return res.json()


def deny_request_admin(user_id: int, req: int) -> bool:
    res = requests.get(f'{host}/update_status/', json={
        "admin": user_id,
        "rq": req,
        "status": 2
    })
    return res.json()


class Messages_db:
    def __init__(self):
        self.db:Connection = connect('req_messages.db', check_same_thread=False)
        self.cur:Cursor = self.db.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS "messages" (
	        "id"	INTEGER NOT NULL UNIQUE,
	        "req"	INTEGER NOT NULL,
	        "msg_id"	INTEGER NOT NULL,
	        "chat_id"	INTEGER NOT NULL,
	        PRIMARY KEY("id" AUTOINCREMENT)
            );

            """)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS "requests" (
	        "id"	INTEGER NOT NULL UNIQUE,
	        "req_id"	INTEGER NOT NULL,
	        PRIMARY KEY("id" AUTOINCREMENT));""")
        self.db.commit()

    

    def exec(self, sql:str, *args):
        res = self.cur.execute(sql, *args)
        res = res.fetchall()
        return res
    

    def create_request(self, req_id:int):
        self.exec(f"INSERT INTO requests(req_id) VALUES ({req_id})")
        res = self.exec(f"select * from  requests where req_id = {req_id}")
        return res
    
    def get_request(self, req_id:int):
        res = self.exec(f"select * from  requests where id = {req_id}")
        return res
    
    def create_message(self, req_id:int, message_id:int, chat_id:int):
        req = self.get_request(req_id)
        if len(req) == 0:
            raise Exception("Request not found")
        self.exec(f"INSERT INTO messages(req, msg_id, chat_id) VALUES ({req_id}, {message_id}, {chat_id})")
        res = self.exec(f"select * from  requests where req_id = {message_id}")
        return res
    
    def get_messages(self, req_id:int):
        res = self.cur.execute(f"SELECT * FROM messages WHERE req={req_id}")
        return res.fetchall()










mesg_db = Messages_db()