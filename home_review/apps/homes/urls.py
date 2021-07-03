from django.urls import path
from .views import HomesView, SpecificHome, UserHomes

urlpatterns = [
    path("",
         HomesView.as_view(),
         name="Homes"
         ),

    path("specific/<home_id>",
         SpecificHome.as_view(),
         name="Specific Home"
         ),

    path("users/<user_id>",
         UserHomes.as_view(),
         name="User Homes"
         ),
]
