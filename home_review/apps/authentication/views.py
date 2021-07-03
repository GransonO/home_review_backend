# Create your views here.
import bugsnag

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SocialAuth


class EmailTemplates:

    @staticmethod
    def register_email(name,):
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
                            <p style="font-size: 17px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> A home fit for you is just some clicks away .</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> You have been registered to the Rated Homes application. We are glad to have you on board</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> Reach out to us for any inquiries and support issues</p>
                            <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                            </br>
                            <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 29px; margin: 0;"><span style="font-size: 24px;">Welcome</span></p>
                        </div>
                    </div>
                </body>
            </html>
        """.format(name)

    @staticmethod
    def reset_email(code):
        return """
            <!DOCTYPE html>
            <html lang="en">
            <body style="text-align:center;">
                <img alt="Image" border="0" src="https://res.cloudinary.com/dolwj4vkq/image/upload/v1586524551/homeReview/logo.png" title="Image" width="300"/>
                <br>
                <br>
                <div style="color:#008080;font-family:'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;line-height:1.2;padding-top:0px;padding-right:0px;padding-bottom:5px;padding-left:0px;">
                    <div style="font-size: 12px; line-height: 1.2; font-family: 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif; color: #008080; mso-line-height-alt: 14px;">
                        <p style="font-size: 18px; line-height: 1.2; text-align: center; mso-line-height-alt: 22px; margin: 0;"><span style="font-size: 18px;"><strong><span style="font-size: 18px;">Did you requested to have your password changed?</span></strong></span></p>
                    </div>
                </div>
                <br>
                <div style="color:#555555;font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif;line-height:1.2;padding-top:10px;padding-right:10px;padding-bottom:10px;padding-left:10px;">
                    <div style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Geneva, Verdana, sans-serif; font-size: 12px; line-height: 1.2; color: #555555; mso-line-height-alt: 14px;">
                        <p style="font-size: 15px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;">We received a request to reset your password. If you made the request, use the code <strong>{}</strong> to complete the process</p>
                        <p style="font-size: 14px; line-height: 1.2; mso-line-height-alt: 17px; margin: 0;"> </p>
                    </div>
                </div>
            </body>
            </html>
        """.format(code)


class SocialView(views.APIView):
    """Social Auth flow"""

    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """Save user Google_ID and data Social Auth DB and profiles (Registration)"""
        passed_data = request.data
        try:
            # Save data to DB
            social_auth = SocialAuth(
                social_auth_id=passed_data["social_auth_id"],
                email=passed_data["email"],
                fullname=passed_data["fullname"],
                phone=passed_data["phone"],
                photo=passed_data["photo"],
                location=passed_data["location"],
                birthDate=passed_data["birthDate"],
                gender=passed_data["gender"]
            )
            social_auth.save()
            SocialView.send_email((passed_data["email"]).lower(), passed_data["fullname"])

            return Response({
                "status": "success",
                "message": "Registration success",
                "code": 0
            }, status.HTTP_200_OK)

        except Exception as E:
            print("Registration error: {}".format(E))
            bugsnag.notify(
                Exception('Registration error: {}'.format(E))
            )
            return Response({
                "status": "failed",
                "message": "Registration failed",
                "code": 0
            }, status.HTTP_200_OK)

    @staticmethod
    def send_email(email, name):
        subject = 'Welcome {} to Rated Homes'.format(name)
        message = EmailTemplates.register_email(name)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list, html_message=message)

