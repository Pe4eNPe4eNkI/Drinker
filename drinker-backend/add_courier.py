import random

from data import db_session
from data.db_session import Session
from data.models import *
from const import FILENAME_DB


def add_courier(id, login, password, name, middlename, surname, phone):
    with db_session.create_session() as session:
        session: Session

        if session.query(Account).filter(Account.login == login_).first():
            print("bad id")
            return False
        acc: Account = Account(id=id, login=login, password=password)
        crr: Courier = Courier(account_id=id)
        acc_info: AccountInfo = AccountInfo(account_id=id, name=name, surname=surname, middlename=middlename, phone=phone)
        session.add_all([acc, crr, acc_info])
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
    phone_: int = int(input("phone number: "))
    add_courier(id_, login_, password_, name_, middlename_, surname_, phone_)
