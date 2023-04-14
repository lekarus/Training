from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

from app import create_app
from database import db
from database.models import NotifUser, SubUser, User
from dotenv import load_dotenv
from flask_sqlalchemy.session import Session
from utils import ORMBaseClass


load_dotenv()


flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@celery_app.task
def send_notification(sender: User | str, receivers: list, topic: str, body_text: str):
    message = MIMEMultipart("alternative")
    message["Subject"] = topic
    message["From"] = sender if type(sender) == str else sender.email
    message["To"] = str([receiver.email for receiver in receivers])
    message.attach(MIMEText(body_text, "plain"))

    from_id = None if type(sender) == str else sender.id

    if len(receivers) > 1:
        with Session(db) as session:
            notifications = [
                NotifUser(
                    from_id=from_id,
                    to_id=receiver.id,
                    is_read=False,
                )
                for receiver in receivers
            ]
            session.bulk_save_objects(notifications)
            session.commit()
    else:
        ORMBaseClass(table=NotifUser).make_create_query(
            from_id=from_id,
            to_id=receivers[0].id,
            is_read=False,
        )

    with smtplib.SMTP("smtp.pacomail.io", 2525) as server:
        server.login(os.getenv("SMTP_LOGIN"), os.getenv("SMTP_PASSWORD"))
        server.esmtp_features['auth'] = 'CRAM-MD5'
        server.sendmail(
            sender,
            [receiver.email for receiver in receivers],
            message.as_string(),
        )


@celery_app.task(name="subscription_expiration_check")
def subscription_expiration_check():
    expiring_records = ORMBaseClass(table=SubUser).make_select_query(to_date=date.today() + timedelta(1))

    with Session(db) as session:
        users = session.query(User).filter(User.id.in_([record.user_id for record in expiring_records])).all()

    topic = "you subscription is expiring"
    text = "your subscription will expire tomorrow, don't forget to renew"

    send_notification(os.getenv("SENDER_EMAIL"), users, topic, text)