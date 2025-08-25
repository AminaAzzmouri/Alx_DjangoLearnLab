from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'actor_username',
            'verb', 'is_read', 'timestamp',
            'target_content_type', 'target_object_id',
        ]
        read_only_fields = [
            'id', 'recipient', 'actor', 'actor_username',
            'timestamp', 'target_content_type', 'target_object_id',
        ]
