# Create your views here.
# Create your views here.
import bugsnag
import uuid

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import views,  status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Support
from .serializers import SupportSerializer


class EmailTemplates:

    @staticmethod
    def support_email(name):
        return """
            <!DOCTYPE html>
            <html lang="en">
                <body style="text-align:center;">
                    <img alt="Image" border="0" src="https://res.cloudinary.com/dolwj4vkq/image/upload/v1586524551/homeReview/logo.png" title="Image" width="300"/>
                    </br>
                    <div style="color:#008080;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.2;padding-top:0px;padding-right:0px;padding-bottom:5px;padding-left:0px;">
                        <div style="font-size: 12px; line-height: 1.2; font-family: 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #008080; mso-line-height-alt: 14px;">
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 22px; margin: 0;"><span style="font-size: 18px;"><strong><span style="font-size: 18px;">Well hello {}</span></strong></span></p>
                        </div>
                    </div>
                    <div style="color:#555555;font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
                        <div style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif; font-size: 12px; line-height: 1.2; color: #555555; mso-line-height-alt: 14px;">
                            <p style="font-size: 17px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Rated Homes support</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Yor support request has been received. you shall receive a notification once we sort your issue</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Reach out to us for any more inquiries or support issues</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            </br>
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 29px; margin: 0;"><span style="font-size: 24px;">Thank you</span></p>
                        </div>
                    </div>
                </body>
            </html>
        """.format(name)


class SupportView(views.APIView):
    """Social Auth flow"""

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """Save user Google_ID and data Social Auth DB and profiles (Registration)"""
        passed_data = request.data
        # Check if it exists
        try:
            # Save data to DB
            support = Support(
                support_id=uuid.uuid1(),
                user_id=passed_data["user_id"],
                email=passed_data["email"],
                details=passed_data["details"],
                title=passed_data["title"],
                photo=passed_data["photo"],
            )
            support.save()
            SupportView.send_email((passed_data["email"]).lower(), passed_data["username"])

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
    def put(request):
        """Update support"""
        passed_data = request.data
        try:
            support = Support.objects.get(support_id=passed_data["support_id"])
            serializer = SupportSerializer(
                support, data=passed_data, partial=True)
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
        message = EmailTemplates.support_email(name)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list, html_message=message)


class SpecificSupport(generics.ListAPIView):
    """Fetch specific support"""
    permission_classes = [AllowAny]
    serializer_class = SupportSerializer

    def get_queryset(self):
        return Support.objects.filter(
            support_id=self.kwargs['support_id']
            )


class UserSupport(generics.ListAPIView):
    """Fetch user specific support"""
    permission_classes = [AllowAny]
    serializer_class = SupportSerializer

    def get_queryset(self):
        return Support.objects.filter(
            user_id=self.kwargs['user_id']
            ).order_by('createdAt')

