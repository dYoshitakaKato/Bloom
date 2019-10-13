import requests
import re
from reservation import Reservation
import datetime
import os
import pytz


def fetch_login() -> requests.Session:
    api = "https://bloom-tss.jp:6417/Common/CmM0000/Login"

    session = requests.session()
    response = session.post(
        api,
        {
            "UserId": os.environ['USERID'],
            "RememberUserId": "true",
            "Password": os.environ['PASSWORD'],
            "RememberPassword": "true",
        },
    )
    return session


def fetch_reservations_tokyo(session: requests.Session, office_number: str,
                             condition: str = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime(
                                 "%Y/%m/%d")) -> list:
    api = "https://bloom-tss.jp:6417/Office/OfM0004/Init?UnitCode=100"

    response = session.get(api)
    pattern = 'insertLabelTime[\s\S]*?\);'
    result = re.findall(pattern, response.text)
    reservations = list()
    for r in result:
        reservation = Reservation(r)
        if office_number == reservation.officeNumber and re.search(condition, reservation.date, flags=0):
            reservations.append(reservation)
        pass
    return reservations


def create_message(room_name: str, reservations: list) -> str:
    message = room_name
    for res in reservations:
        message += res.title + "\n" + res.date + " " + res.startTime + " - " + res.endTime + "\n"
    return message
