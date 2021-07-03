# Create your views here.
# Create your views here.
import bugsnag
import uuid

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import views,  status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Homes
from .serializers import HomeSerializer


class HomesView(views.APIView):
    """Social Auth flow"""

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """Save user Google_ID and data Social Auth DB and profiles (Registration)"""
        passed_data = request.data
        # Check if it exists
        try:
            # Save data to DB
            homes = Homes(
                home_id=uuid.uuid1(),
                user_id=passed_data["user_id"],
                description=passed_data["description"],
                administrator=passed_data["administrator"],
                bathrooms=passed_data["bathrooms"],
                bedrooms=passed_data["bedrooms"],
                place_id=passed_data["user_id"],
                place_image=passed_data["user_id"],
                address=passed_data["address"],
                name=passed_data["name"]
            )
            homes.save()
            HomesView.send_email((passed_data["email"]).lower(), passed_data["username"])

            return Response({
                "status": "success",
                "message": "Homes success",
                "code": 0
            }, status.HTTP_200_OK)

        except Exception as E:
                print("Homes error: {}".format(E))
                bugsnag.notify(
                    Exception('Homes error: {}'.format(E))
                )
                return Response({
                    "status": "failed",
                    "message": "Homes failed",
                    "code": 0
                }, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """Update support"""
        passed_data = request.data
        try:
            homes = Homes.objects.get(home_id=passed_data["home_id"])
            serializer = HomeSerializer(
                homes, data=passed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                "status": "success",
                "message": "Support success",
                "code": 0
            }, status.HTTP_200_OK)

        except Exception as E:
            print("Support error: {}".format(E))
            bugsnag.notify(
                Exception('Support error: {}'.format(E))
            )
            return Response({
                "status": "failed",
                "message": "Support failed",
                "code": 0
            }, status.HTTP_200_OK)

    @staticmethod
    def send_email(email, name):
        subject = 'Rated Homes Support'.format(name)
        message = EmailTemplates.home_email(name)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list, html_message=message)


class EmailTemplates:

    @staticmethod
    def home_email(name):
        return """
            <!DOCTYPE html>
            <html lang="en">
                <body style="text-align:center;">
                    <img alt="Image" border="0" src="https://res.cloudinary.com/dolwj4vkq/image/upload/v1586524551/homeReview/logo.png" title="Image" width="300"/>
                    </br>
                    <div style="color:#008080;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.2;padding-top:0px;padding-right:0px;padding-bottom:5px;padding-left:0px;">
                        <div style="font-size: 12px; line-height: 1.2; font-family: 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #008080; mso-line-height-alt: 14px;">
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 22px; margin: 0;"><span style="font-size: 18px;"><strong><span style="font-size: 18px;">Hello {}</span></strong></span></p>
                        </div>
                    </div>
                    <div style="color:#555555;font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
                        <div style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif; font-size: 12px; line-height: 1.2; color: #555555; mso-line-height-alt: 14px;">
                            <p style="font-size: 17px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Rated Homes Assistant</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> You submitted a request to add a suitable home to one of our many homes </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> We thank you for your support as we work to provide a desirable home finder for all our lovely customers. </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Reach out to us for any more inquiries or support issues</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            </br>
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 29px; margin: 0;"><span style="font-size: 24px;">Thank you</span></p>
                        </div>
                    </div>
                </body>
            </html>
        """.format(name)


class SpecificHome(generics.ListAPIView):
    """Fetch specific support"""
    permission_classes = [AllowAny]
    serializer_class = HomeSerializer

    def get_queryset(self):
        return Homes.objects.filter(
            home_id=self.kwargs['home_id']
            )


class UserHomes(generics.ListAPIView):
    """Fetch user specific support"""
    permission_classes = [AllowAny]
    serializer_class = HomeSerializer

    def get_queryset(self):
        return Homes.objects.filter(
            user_id=self.kwargs['user_id']
            ).order_by('createdAt')

