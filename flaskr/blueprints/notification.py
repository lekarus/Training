from enum import Enum

from database import db
from database.models import NotifUser, Roles, SubUser, User
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import abort, reqparse, Resource
from flask_sqlalchemy.session import Session
from serializers.notifications import NotificationSerializer
from utils import create_blueprint_with_api, ORMBaseClass

notification, api = create_blueprint_with_api("notification")


class NotificationEnum(Enum):
    to_all = "to_all"
    direct = "direct"
    subscription = "subscription"


class NotificationResource(Resource):
    @jwt_required()
    def get(self):
        notifications = NotifUser.query.filter_by(to_id=97).all()
        return NotificationSerializer(many=True).dump(notifications)

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=NotificationEnum, location='json', required=True)
        parser.add_argument('to_user', type=int, location='json')
        parser.add_argument('subscription_id', type=int, location='json')
        parser.add_argument('notif_header', type=str, location='json', required=True)
        parser.add_argument('notif_body', type=str, location='json', required=True)
        args = parser.parse_args()
        from_user = User.query.filter_by(id=get_jwt_identity()).first()
        if args["type"] == NotificationEnum.to_all:
            self._send_notif_to_all(from_user, args)
        if args["type"] == NotificationEnum.direct:
            self._send_notif_direct(from_user, args)
        if args["type"] == NotificationEnum.subscription:
            self._send_notif_subscription(from_user, args)
        return 200

    @staticmethod
    def _send_notif_to_all(from_user, args):
        from services.tasks import send_notification
        if from_user.role != Roles.admin:
            abort(403, description="Have no access. Only Admins!")
        send_notification.delay(from_user, User.query.all(), args["notif_header"], args["notif_body"])

    @staticmethod
    def _send_notif_direct(from_user, args):
        from services.tasks import send_notification
        if not args["to_user"]:
            abort(400, description="direct message must contain [to_user] param")
        to_user = ORMBaseClass(table=User).make_select_query(id=args["to_user"]).first()
        dict_user = {"id": to_user.id, "email": to_user.email}
        send_notification.delay(from_user.id, from_user.email, dict_user, args["notif_header"], args["notif_body"])

    @staticmethod
    def _send_notif_subscription(from_user, args):
        from services.tasks import send_notification
        if from_user.role != Roles.trainer:
            abort(403, description="Have no access. Only Trainers!")
        if not args["subscription_id"]:
            abort(400, description="subscription message must contain [subscription_id] param")
        with Session(db) as session:
            sub_users = ORMBaseClass(table=SubUser).make_select_query(subscription_id=args["subscription_id"])
            users = session.query(User).filter(User.id.in_([user.user_id for user in sub_users])).all()
            dict_users = [{"id": user.id, "email": user.email} for user in users]

        send_notification.delay(from_user.id, from_user.email, dict_users, args["notif_header"], args["notif_body"])


class NotificationResourceRetrieve(Resource):
    @jwt_required()
    def get(self, instance_id):
        instance = ORMBaseClass(table=NotifUser).make_select_query(id=instance_id, to_id=get_jwt_identity())
        if not instance:
            abort(400, description="Bad Request. You don`t have access to this notification")
        instance = ORMBaseClass(table=NotifUser).make_update_query(instance[0], {"is_read": True})
        return NotificationSerializer().dump(instance)


class GetUnReadNotifications(Resource):
    @jwt_required()
    def get(self):
        instances = ORMBaseClass(table=NotifUser).make_select_query(to_id=get_jwt_identity(), is_read=False)
        return NotificationSerializer(many=True).dump(instances)


api.add_resource(NotificationResource, "/notification")
api.add_resource(NotificationResourceRetrieve, "/notification/<int:instance_id>")

api.add_resource(GetUnReadNotifications, "/unread_notifications")
