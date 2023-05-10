from django.urls import path
from . import views
from .models import *
from .forms import *

urlpatterns = [
    path('', views.index, name="index"),
    path('signup/', views.UserSignupView.as_view(), name="user_create"),
    path('login/',views.LoginView.as_view(template_name="home/login.html", authentication_form=UserLoginForm)),
    path('logout/', views.logout_user, name="logout"),
    path('audio_upload/', views.audio_upload, name='audio_upload'),
    path('notes/<int:prodid>/', views.note_individual, name="individual_note" ),
    path('notes_edit/<int:prodid>/', views.note_editor, name="edit_note" ),
    path('notes_new/', views.note_new, name="note_new" ),
    path('supporting_doc/<int:note_id>/', views.add_doc, name="add_doc" ),
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path('groups/new/', views.GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group-update'),
    path('delete/note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('delete/audio/<int:audio_id>/', views.delete_audio, name='delete_audio'),
    path('delete/supporting-doc/<int:sup_id>/', views.delete_supporting_doc, name='delete_supporting_doc'),
]


