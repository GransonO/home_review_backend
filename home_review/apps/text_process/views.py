# import bugsnag
import spacy
from profanity_filter import ProfanityFilter
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

        nlp = spacy.load('en')
        profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse Spacy Language (optional)
        nlp.add_pipe(profanity_filter.spacy_component, last=True)

        passed_data = request.data
        body = passed_data['body']

        doc = nlp(body)
        is_profane = doc._.is_profane

        print("The passedData is ----------------------------: {}".format(passed_data))
        return Response({"isProfane": is_profane}, status.HTTP_200_OK)
