from rest_framework import serializers
from chatapp import models


class ChatRoomSerializer(serializers.ModelSerializer):
    members = serializers.StringRelatedField(many=True,read_only = True)
    class Meta:
        model = models.ChatRoom
        fields = [
                'id',
                'name',
                'room_type',
                'members',
                'created_at',
                'is_active'
            ]
        
class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source = 'sender.username',  read_only = True)
    class Meta:
        model = models.Message
        fields = [
            'id',
            'chatroom',
            'sender',
            'content',
            'sender_username',
            'message_type',
            'timestamp',
            'is_read',
            'is_edited',
            'is_deleted',
            'attachment',
        ]
        read_only_fields = ['timestamp','is_read','is_edited','deleted']
     

       
class UserStatusSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = models.UserStatus
        fields = [
            'id',
            'username',
            'is_online',
            'is_typing',
            'last_seen'
        ]

        def create(self,validated_data):
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)
        def update(self,instance,validated_data):
            validated_data['user'] = self.context['request'].user
            return super().update(instance,validated_data)


class BlockedUserSerializer(serializers.ModelSerializer):
    blocker_username = serializers.CharField(source = 'blocker.username',read_only = True)
    blocked_username = serializers.CharField(source = 'blocked.username', read_only = True)
    blocker = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = models.BlockedUser
        fields = [
            'blocker',
            'blocker_username',
            'blocked',
            'blocked_username',
            'blocked_at'
        ]

class TypingIndicatorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source= 'user.username', read_only = True)
    chatroom_username = serializers.CharField(source = 'chatroom.name', read_only = True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # client doesn't send this
 
    class Meta:
        model = models.TypingIndicator
        fields= [
            'id',
            'chatroom_username',
            'chatroom',
            'user',
            'username',
            'is_typing',
            'updated_at',
        ]
        read_only = ['username','chatroom_username','updated_at','user']
class MessageReactionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source= 'user.username', read_only = True)
    message_id = serializers.IntegerField(source = 'message.id', read_only = True)
    class Meta:
        model = models.MessageReaction
        fields = [
            'id', 
            'message', 
            'message_id', 
            'user', 
            'username', 
            'reaction', 
            'reacted_at'
        ]
        read_only_fields = ['id', 'username', 'message_id', 'user', 'reacted_at']

class ChatRoomSettingSerializer(serializers.ModelSerializer):
    chatroom_name =  serializers.CharField(source = 'chatroom.user', read_only =True)
    class Meta:
        model = models.ChatRoomSettings
        fields = [
            'id',
            'chatroom',
            'chatroom_name',
            'mute_notifications',
            'dark_mode',
            'pin_chat',
            'custom_nickname'
        ]
        read_only_fields = ['id','chatroom_name']

class ArchivedChatSerializer(serializers.ModelSerializer):
    chatroom_name = serializers.CharField(source='chatroom.name', read_only=True)
    archived_by_username = serializers.CharField(source='archived_by.username', read_only=True)

    class Meta:
        model = models.ArchivedChat
        fields = [
            'id',
            'chatroom',
            'chatroom_name',
            'archived_by',
            'archived_by_username',
            'archieved_at',
            'is_unarchieved',
            'un_archievd_at'
        ]
        read_only_fields = ['id', 'chatroom_name', 'archived_by', 'archived_by_username', 'archieved_at']
        
class DeletedMessageSerializer(serializers.ModelSerializer):
    message_id = serializers.CharField(source= 'message.id', read_only = True)
    deleted_by_username = serializers.CharField(source = 'deleted_by.username', read_only = True)
    class Meta:
        model = models.DeletedMessage
        fields = [
            'id',
            'message',
            'message_id',
            'deleted_by',
            'deleted_by_username',
            'deleted_at',
            'is_permanent',
            'permanent_deletion_at'
        ]

        read_only_fields = ['id','message_id','deleted_by_username','deleted_at','deleted_by',]

         
