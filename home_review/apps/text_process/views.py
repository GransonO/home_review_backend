from leoprofanity import LeoProfanity
from rest_framework import views, status
from rest_framework.response import Response


class Processing(views.APIView):
    """ Processing  """

    @staticmethod
    def get(request):
        passed_data = request.data
        print("The passedData is ----------------------------: {}".format(passed_data))
        return Response({"GET"}, status.HTTP_200_OK)

    @staticmethod
    def post(request):
        fil = LeoProfanity()
        passed_data = request.data

        body = passed_data['body']
        is_profane = fil.check(body)

        print("The passedData is ----------------------------: {}".format(passed_data))
        return Response({"isProfane": is_profane}, status.HTTP_200_OK)
