from django.urls import path
from .views import SocialView

urlpatterns = [
    path("register",
         SocialView.as_view(),
         name="Social Auth Register"
         ),
]
