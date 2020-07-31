# Create your views here.
import bugsnag
from rest_framework import views,  status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import MpesaEntryDB


class MpesaCallback(views.APIView):
    """
        Pick all MPESA details and save in DB
    """
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        """ Reassign Tier groups to members """
        passedData = request.data
        print("The passedData is -------------: {}".format(passedData))

        body = passedData['Body']
        # callback_body = body['stkCallback']
        # MerchantRequestID = callback_body['MerchantRequestID']
        # ResultCode = callback_body['ResultCode']
        # ResultDesc = callback_body['ResultDesc']
        # CallbackMetadata = callback_body['CallbackMetadata']
        #
        # Item = CallbackMetadata['Item']
        # Amount = Item[0]['Value']
        # MpesaReceiptNumber = Item[1]['Value']
        # TransactionDate = Item[3]['Value']
        # PhoneNumber = Item[4]['Value']
        mpesa_data = MpesaEntryDB(
            MerchantRequestID=1010,  # MerchantRequestID,
            ResultCode=1010,  # ResultCode,
            ResultDesc=1010,  # ResultDesc,
            Amount=100,  # Amount,
            MpesaReceiptNumber=1234,  # MpesaReceiptNumber,
            # TransactionDate=TransactionDate,
            Client_phone='0728376473'  # PhoneNumber
        )
        mpesa_data.save()
        return Response({"DONE"}, status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """Get the Mpesa value deposited"""
        passedData = request.data
        trans_num = passedData["MerchantRequestID"]
        try:
            result = MpesaEntryDB.objects.get(
                MerchantRequestID=trans_num)
            print("The responce is : {}".format(result))
            return Response({
                    "status": "success",
                    "code": 1,
                    "customer_phone": result.Client_phone,
                    "receipt_number": result.MpesaReceiptNumber,
                    "amount": result.Amount,
                }, status.HTTP_200_OK)

        except Exception as E:
            print("Error: {}".format(E))
            bugsnag.notify(
                Exception('Transaction Put: {}'.format(E))
            )
            return Response({
                "error": "{}".format(E),
                "status": "failed",
                "code": 0
                }, status.HTTP_200_OK)
