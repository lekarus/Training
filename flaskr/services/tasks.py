import datetime
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from typing import List

from app import create_app
from database import db
from database.models import Notification, SubUser, User
from dotenv import load_dotenv
from flask_sqlalchemy.session import Session
from utils import ORMBaseClass

load_dotenv()

flask_app = create_app()
celery_app = flask_app.extensions["celery"]


@celery_app.task
def send_notification(sender_id: str, sender_email: str, recipients: List[dict], topic: str, body_text: str):
    """create record in DB and send email notifications
    :str sender_id: sender id
    :str sender_email: sender email
    :str recipients: dictionary list with recipients
    :str topic: subject of message
    :str body_text: body text of the message
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = topic
    message["From"] = sender_email
    message["To"] = str([receiver["email"] for receiver in recipients])
    message.attach(MIMEText(body_text, "plain"))

    # if we have more than 1 receiver, we have to create multiple records in DB
    if len(recipients) > 1:
        with Session(db) as session:
            notifications = [
                Notification(
                    from_id=sender_id,
                    to_id=receiver["id"],
                    is_read=False,
                    notif_header=topic,
                    notif_body=body_text,
                    send_at=datetime.datetime.now(),
                )
                for receiver in recipients
            ]
            session.bulk_save_objects(notifications)
            session.commit()
    else:
        ORMBaseClass(table=Notification).make_create_query(
            from_id=sender_id,
            to_id=recipients[0]["id"],
            is_read=False,
            send_at=datetime.datetime.now(),
        )

    # send email notification
    with smtplib.SMTP("smtp.pacomail.io", 2525) as server:
        server.login(os.getenv("SMTP_LOGIN"), os.getenv("SMTP_PASSWORD"))
        server.esmtp_features['auth'] = 'CRAM-MD5'
        server.sendmail(
            sender_email,
            [receiver["email"] for receiver in recipients],
            message.as_string(),
        )


@celery_app.task(name="subscription_expiration_check")
def subscription_expiration_check():
    """task to check up-to-date subscriptions for all users"""
    expiring_records = ORMBaseClass(table=SubUser).make_select_query(to_date=date.today() + timedelta(1))

    users = User.query.filter(User.id.in_([record.user_id for record in expiring_records])).all()
    dict_users = [{"id": user.id, "email": user.email} for user in users]

    topic = "you subscription is expiring"
    text = "your subscription will expire tomorrow, don't forget to renew"

    send_notification(os.getenv("SENDER_EMAIL"), dict_users, topic, text)
