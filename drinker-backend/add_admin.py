import random

from data import db_session
from data.db_session import Session
from data.models import *
from const import FILENAME_DB
from random import randrange


def add_admin(id, login, password, name, middlename, surname, phone):
    with db_session.create_session() as session:
        session: Session

        if session.query(Account).filter(Account.login == login_).first():
            print("bad id")
            return False
        acc: Account = Account(id=id, login=login, password=password)
        adm: Admin = Admin(account_id=id)
        acc_info: AccountInfo = AccountInfo(account_id=id, name=name, surname=surname, middlename=middlename, phone=phone)
        session.add_all([acc, adm, acc_info])
        session.commit()
        print(f"id: {id_}")
        return True


if __name__ == "__main__":
    db_session.global_init(FILENAME_DB)

    id_: int = random.randint(0, 1000_000_000_000_000)
    login_: str = input("login: ")
    password_: str = input("password: ")
    name_: str = input("name: ")
    middlename_: str = input("middlename: ")
    surname_: str = input("surname: ")
    phone_: int = input("phone number: ")
    add_admin(id_, login_, password_, name_, middlename_, surname_, phone_)
