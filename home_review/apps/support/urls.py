from django.urls import path
from .views import SupportView, SpecificSupport, UserSupport

urlpatterns = [
    path("",
         SupportView.as_view(),
         name="Support"
         ),

    path("specific/<support_id>",
         SpecificSupport.as_view(),
         name="Specific Support"
         ),

    path("users/<user_id>",
         UserSupport.as_view(),
         name="User Support"
         ),
]
