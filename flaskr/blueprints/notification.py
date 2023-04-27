from database.models import Notification, NotificationType, Roles, User
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import abort, reqparse, Resource
from flask_restful_swagger import swagger
from serializers.notifications import NotificationSerializer
from utils import create_blueprint_with_api, ORMBaseClass

notification, api = create_blueprint_with_api("notification", "notification")


class NotificationResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=NotificationType, location='json', required=True)
        self.parser.add_argument('to_user', type=int, location='json')
        self.parser.add_argument('subscription_id', type=int, location='json')
        self.parser.add_argument('notif_header', type=str, location='json', required=True)
        self.parser.add_argument('notif_body', type=str, location='json', required=True)
        super(Resource, self).__init__()

    @swagger.operation(
        notes='Get all notification',
        responseMessages=[
            {
                "code": 200,
                "message": "[List of notifications]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
        ],
    )
    @jwt_required()
    def get(self):
        notifications = Notification.query.filter_by(to_id=get_jwt_identity()).order_by(Notification.send_at).all()
        return NotificationSerializer(many=True).dump(notifications)

    @swagger.operation(
        notes='Send notification',
        parameters=[
            {
                "name": "type",
                "description": "notification type [to_all/direct/subscription]",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "body",
            },
            {
                "name": "to_user",
                "description": "user_id, if you send direct message",
                "required": False,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "body",
            },
            {
                "name": "subscription_id",
                "description": "subscription_id, if you send subscription message",
                "required": False,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "body",
            },
            {
                "name": "notif_header",
                "description": "Topic of your notification",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "body",
            },
            {
                "name": "notif_body",
                "description": "Your message",
                "required": True,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "body",
            },
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
            {
                "code": 403,
                "message": "Have no access. Only Admins!",
            },
            {
                "code": 400,
                "message": "direct message must contain [to_user] param",
            },
            {
                "code": 403,
                "message": "Have no access. Only Trainers!",
            },
            {
                "code": 400,
                "message": "subscription message must contain [subscription_id] param",
            },
        ],
    )
    @jwt_required()
    def post(self):
        args = self.parser.parse_args()
        from_user = User.query.get(get_jwt_identity())

        if args["type"] == NotificationType.to_all:
            self._send_notif_to_all(from_user, args)
        if args["type"] == NotificationType.direct:
            self._send_notif_direct(from_user, args)
        if args["type"] == NotificationType.subscription:
            self._send_notif_subscription(from_user, args)
        return 200

    @staticmethod
    def _send_notif_to_all(from_user: User, args: dict):
        """send notification to all users in system"""

        from services.tasks import send_notification
        if from_user.role != Roles.admin:
            abort(403, description="Have no access. Only Admins!")

        users = [{"id": user.id, "email": user.email} for user in User.query.all()]
        send_notification.delay(from_user, users, args["notif_header"], args["notif_body"])

    @staticmethod
    def _send_notif_direct(from_user: User, args: dict):
        """send direct notification"""

        from services.tasks import send_notification
        if not args["to_user"]:
            abort(400, description="direct message must contain [to_user] param")

        to_user = User.query.get(args["to_user"])
        user = [{"id": to_user.id, "email": to_user.email}]
        send_notification.delay(from_user.id, from_user.email, user, args["notif_header"], args["notif_body"])

    @staticmethod
    def _send_notif_subscription(from_user: User, args: dict):
        """send notification to all subscribed users"""

        from services.tasks import send_notification
        if from_user.role != Roles.trainer:
            abort(403, description="Have no access. Only Trainers!")
        if not args["subscription_id"]:
            abort(400, description="subscription message must contain [subscription_id] param")

        subscribed = User.query.filter(User.subscriptions.any(id=args["subscription_id"])).all()
        users = [{"id": user.id, "email": user.email} for user in subscribed]
        send_notification.delay(from_user.id, from_user.email, users, args["notif_header"], args["notif_body"])


class NotificationResourceRetrieve(Resource):
    @swagger.operation(
        notes='Retrieve and read your notification',
        responseMessages=[
            {
                "code": 200,
                "message": "[Notification Object]",
            },
            {
                "code": 400,
                "message": "Bad Request. You don`t have access to this notification",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
        ],
    )
    @jwt_required()
    def get(self, instance_id):
        instance = Notification.query.filter_by(id=instance_id, to_id=get_jwt_identity()).first()
        if not instance:
            abort(400, description="Bad Request. You don`t have access to this notification")

        instance = ORMBaseClass(table=Notification).make_update_query(instance, {"is_read": True})
        return NotificationSerializer().dump(instance)


class GetUnReadNotifications(Resource):
    @swagger.operation(
        notes='Get your unread notifications',
        responseMessages=[
            {
                "code": 200,
                "message": "[List of Notifications]",
            },
            {
                "code": 401,
                "message": "Missing Authorization Header",
            },
        ],
    )
    @jwt_required()
    def get(self):
        instances = Notification.query.filter_by(to_id=get_jwt_identity(), is_read=False).order_by(Notification.send_at)
        return NotificationSerializer(many=True).dump(instances)


api.add_resource(NotificationResource, "/")
api.add_resource(NotificationResourceRetrieve, "/<int:instance_id>")

api.add_resource(GetUnReadNotifications, "/unread_notifications")
