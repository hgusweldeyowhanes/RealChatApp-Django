# 💬 Secure Real-Time Chat Application
A comprehensive, real-time chat application built with Django, featuring end-to-end encryption, multimedia support, and advanced messaging capabilities.

## 🚀 Features
### 🔒 Security & Privacy
End-to-End Encryption using Fernet symmetric encryption

User Blocking System with privacy controls

Message Deletion with soft/hard delete options

Secure File Attachments with encrypted storage

## 💬 Messaging Capabilities
Real-time Chat with WebSocket support

Multiple Message Types: Text, Images, Voice, Video, Documents

Message Threading with reply functionality

Read Receipts and delivery status

Message Editing with edit history

Emoji Reactions with custom emoji support

## 👥 User Management
Online/Offline Status with last seen tracking

Typing Indicators in real-time

User Status updates

Chat Room Management with member controls

## 🏗️ Chat Rooms & Groups
Private Chats (1-on-1 conversations)

Group Chats with multiple participants

Chat Room Settings with customization

Archived Chats with unarchive capability


## 🛠️ Technology Stack
Backend
Django 4.0+ - Web framework

Django Channels - WebSocket support

PostgreSQL - Database (recommended)

Redis - Channel layers & caching

Security
Fernet Encryption - Message encryption

Django Auth - User authentication

File Validation - Secure file uploads

Frontend (Suggested)
WebSocket Client - Real-time communication

Bootstrap 5 - UI framework

JavaScript - Dynamic interactions

## 📁 Database Models
### Core Models
#### ChatRoom
Private and group chat rooms

#### Member management

Room type classification

#### Message
Encrypted message content

Multiple file type support

Threading and replies

Read receipts and reactions


### Advanced Features
#### MessageReaction
Emoji reactions system

Custom reaction types

User reaction tracking

#### BlockedUser
User blocking system

Privacy controls

Block management

#### ChatRoomSettings
Per-chat customization

Notification controls


## 🔧 Installation & Setup

1. Prerequisites
```bash
python >= 3.8
postgresql >= 12
redis >= 6.0
```
2. Install Dependencies
```bash
pip install django channels daphne cryptography pillow
pip install channels-redis redis psycopg2-binary
```


# Channels Configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
4. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```
5. Run Development Server
```bash
# Run with Daphne for WebSocket support
daphne chat_app.asgi:application
```

## 🔐 Security Implementation
#### Message Encryption
```bash
# All messages are encrypted before storage
def encrypt_content(self, value):
    f = Fernet(settings.ENCRYPTION_KEY)
    return f.encrypt(value.encode()).decode()

def decrypt_content(self):
    f = Fernet(settings.ENCRYPTION_KEY)
    return f.decrypt(self.content.encode()).decode()
```
