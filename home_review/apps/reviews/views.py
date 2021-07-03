import bugsnag
import uuid

from rest_framework import views,  status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Reviews
from .serializers import ReviewSerializer


class ReviewsView(views.APIView):
    """Social Auth flow"""

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """Save user Google_ID and data Social Auth DB and profiles (Registration)"""
        passed_data = request.data
        # Check if it exists
        try:
            # Save data to DB
            review = Reviews(
                review_id=uuid.uuid1(),
                user_id=passed_data["user_id"],
                reviewer=passed_data["reviewer"],
                email=passed_data["email"],
                review_details=passed_data["review_details"],
                title=passed_data["title"],
                review_image=passed_data["review_image"],
                place_image=passed_data["place_image"],
                place_address=passed_data["place_address"],
                place_id=passed_data["place_id"],
                place_name=passed_data["place_name"],
                rating=passed_data["rating"],
                admin=passed_data["admin"],
                units=passed_data["units"],
                environment=passed_data["environment"],
                amenities=passed_data["amenities"]
            )
            review.save()

            return Response({
                "status": "success",
                "message": "Review success",
                "code": 0
            }, status.HTTP_200_OK)

        except Exception as E:
                print("Review error: {}".format(E))
                bugsnag.notify(
                    Exception('Review error: {}'.format(E))
                )
                return Response({
                    "status": "failed",
                    "message": "Review failed",
                    "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """Update support"""
        passed_data = request.data
        try:
            review = Reviews.objects.get(review_id=passed_data["review_id"])
            serializer = ReviewSerializer(
                review, data=passed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "status": "success",
                "message": "Review success",
                "code": 0
            }, status.HTTP_200_OK)

        except Exception as E:
            print("Review error: {}".format(E))
            bugsnag.notify(
                Exception('Review error: {}'.format(E))
            )
            return Response({
                "status": "failed",
                "message": "Review failed",
                "code": 0
            }, status.HTTP_200_OK)


class PlaceSpecificReviews(generics.ListAPIView):
    """Fetch specific support"""
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Reviews.objects.filter(
            place_id=self.kwargs['place_id']
            )


class UserReviews(generics.ListAPIView):
    """Fetch user specific support"""
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Reviews.objects.filter(
            user_id=self.kwargs['user_id']
            ).order_by('createdAt')
