import debug_toolbar
from django.urls import path, include
from . import views



urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("query/", views.query, name="query"),
    path("query_txt/", views.query_txt, name="query_txt"),
    path("history/", views.history, name="history"),    
    path("query_detailed/<int:query_name_pk>", views.query_detailed, name="query_detailed"),
    path("global_words", views.global_words, name="global_words"),
    path("global_words_personal", views.global_words_personal, name="global_words_personal"),
]
