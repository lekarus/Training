from serializers import ma


class NotificationSerializer(ma.Schema):

    class Meta:
        fields = ("id", "from_id", "notif_header", "notif_body", "is_read")
