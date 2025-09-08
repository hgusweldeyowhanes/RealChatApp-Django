from django.urls import path
from chatapp import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('', views.CreateRoom, name='create-room'),
    path('login/', views.UserLoginView.as_view(), name='login-user'),  
    path('logout/', views.UserLogoutView.as_view(),name='logout-user'),
    path('room/<str:room_name>/', views.Message_room_View, name='room'),
    path("token/",TokenObtainPairView.as_view(),),
    path("token/refrash",TokenRefreshView.as_view(),),
    path("chatrooms/",views.ChatRoom_listView, name= "chatroom_list"),
    path("chatrooms/<int:pk>/",views.ChatRoomDetailView.as_view(), name = "chatroom_detail"),
    path("chatrooms/<int:chatroom_id>/messages/", views.MessageView.as_view(), name="message-list-create"),
    path("messages/<int:pk>/",views.MessageDetailView.as_view(), name="message-detail"),
    path('user-status/',views.UserStatusView.as_view()),
    path('user-status/<int:pk>/',views.UserStatusUpdateDeleteView.as_view(),),
    path('blocked-user/',views.BlockedUserView.as_view()),
    path('blocked-user/<int:pk>/',views.BlockedUserDetailView.as_view()),
    path('typing-indicator/', views.TypingIndicatorListView.as_view()),
    path('message-reaction/',views.MessageReactionView.as_view()),
    path('chatroom-settings/<int:chatroom_id>/',views.ChatRoomSettingView.as_view()),
    path('archived-chat/',views.ArchievedChatView.as_view()),
    path('deleted-message/',views.DeletedMessageView.as_view(),)
]
