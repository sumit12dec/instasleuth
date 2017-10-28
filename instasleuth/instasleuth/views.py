from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from pan_parser import parse_pan
from cloud_vision import cloud_api
import time
from django.views.decorators.csrf import csrf_exempt

#BASE = '/Users/sumit/Desktop/instamojo/instasleuth'
BASE = '/var/www/'
def handle_uploaded_file(file):
    with open(BASE + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    time.sleep(5)


@csrf_exempt
def get_pan_data(request):
    # USER_IMAGES_BUCKET = settings.S3_USER_IMAGES_BUCKET
    # PROPERTY_IMAGES_BUCKET = settings.S3_PROPERTY_IMAGES_BUCKET
    # AWS_KEY = settings.S3_AWS_KEY
    # AWS_SECRET = settings.S3_AWS_SECRET
    response = {}
    print request.FILES
    try:
        file = request.FILES['file']
    except KeyError as e:
        return HttpResponse("The parameter "+ str(e) + " is missing", status=400)
    
    
    try:
        extension = file.name.split('.')[-1]#won't work correctly if file name has no '.'
        print type(file), "fileeee"
        handle_uploaded_file(file)
        user_name, fathers_name, dob, pan_card_no = parse_pan(BASE+file.name)
        response['user_name'] = user_name
        response['fathers_name'] = fathers_name
        response['dob'] = dob
        response['pan_card_no'] = pan_card_no
        return JsonResponse(response, status=200)
    except Exception as e:
        print(e)
        response['status'] = "error"
        response['message'] = "No data"
        # response['message'] = "Token string has been expired"
        return JsonResponse(response, status=500)

@csrf_exempt
def cloud_extract_data(request):

    response = {}
    print request.FILES
    try:
        file = request.FILES['file']
    except KeyError as e:
        return HttpResponse("The parameter "+ str(e) + " is missing", status=400)
    
    
    try:
        extension = file.name.split('.')[-1]#won't work correctly if file name has no '.'
        print type(file), "fileeee"
        handle_uploaded_file(file)
        text = cloud_api(BASE+file.name)
        if "INCOME TAX DEPARTMENT" not in text[0]:
            response['status'] = "Invalid Image"
            return JsonResponse(response)
        else:
            chunked_data = text[0].split("\n")
            if len(chunked_data[0])>21:
                chunked_data.insert(0, 'FORCE_REORDER')
            response['user_name'] = chunked_data[2]
            response['user_dob'] = chunked_data[4]
            response['user_pan'] = chunked_data[6]
        response['full_extracted_text'] = text
        return JsonResponse(response, status=200)
    except Exception as e:
        print(e)
        response['status'] = "error"
        response['message'] = "No data"
        # response['message'] = "Token string has been expired"
        return JsonResponse(response, status=500)