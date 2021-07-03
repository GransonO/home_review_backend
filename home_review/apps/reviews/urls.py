from django.urls import path
from .views import ReviewsView, PlaceSpecificReviews, UserReviews

urlpatterns = [
    path("",
         ReviewsView.as_view(),
         name="Reviews"
         ),

    path("specific/<place_id>",
         PlaceSpecificReviews.as_view(),
         name="Place Specific Reviews"
         ),

    path("users/<user_id>",
         UserReviews.as_view(),
         name="User Reviews"
         ),
]
