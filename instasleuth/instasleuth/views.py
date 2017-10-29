from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from pan_parser import parse_pan
from cloud_vision import cloud_api
import time
import json
from django.views.decorators.csrf import csrf_exempt
from .models import UserPoints, UserData
from django.core import serializers
from shutil import copyfile

#BASE = '/Users/sumit/Desktop/instamojo/instasleuth'
BASE = '/var/www/'
def handle_uploaded_file(file):
    with open(BASE + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    time.sleep(2)
    copyfile(BASE+file.name, '/var/www/instasleuth/instasleuth/static/'+file.name)




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
def cloud_extract_data(request, user_id):

    response = {}
    print request.FILES
    try:
        file = request.FILES['file']
        if not user_id:
            user_id = request.POST.get('user_id')
        usr = UserPoints(user_id=user_id)
        obj = UserPoints(user_points=0, user_name=usr.user_name)
        obj.save()
    except KeyError as e:
        return HttpResponse("The parameter "+ str(e) + " is missing", status=400)
    
    
    try:
        extension = file.name.split('.')[-1]#won't work correctly if file name has no '.'
        print type(file), "fileeee"
        handle_uploaded_file(file)
        text = cloud_api(BASE + file.name)
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
            if len(chunked_data[6]) != 10:
                if len(chunked_data[5]) == 10 and chunked_data[5][5:9].isdigit():
                    response['user_pan'] = chunked_data[5]
                elif len(chunked_data[7]) == 10 and chunked_data[7][5:9].isdigit():
                    response['user_pan'] = chunked_data[7]
                elif len(chunked_data[4]) == 10 and chunked_data[4][5:9].isdigit():
                    response['user_pan'] = chunked_data[4]

        response['full_extracted_text'] = text
        try:
            obj = UserData(user_id_fk = UserPoints(user_id=user_id),
            user_name = response['user_name'],
            user_pan = response['user_pan'],
            user_dob = response['user_dob'],
            user_image_url = 'http://34.227.56.111/static/' + file.name)
            obj.save()            
        except Exception as e: 
            print e       
            return HttpResponse(repr(e))       
    except Exception as e:
        print(e)
        response['status'] = "error"
        response['message'] = "No data"
        # response['message'] = "Token string has been expired"
        return JsonResponse(response, status=500)
    return JsonResponse({'user_id': user_id}, status=200)


@csrf_exempt
def user_points(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        user_points = request.POST.get('user_points')
        obj = UserPoints(user_name=user_name, user_points=user_points)
        obj.save()
        new_obj = UserPoints.objects.get(user_name=user_name)

        return JsonResponse({'user_id': new_obj.user_id})
    elif request.method == "GET":
        print request.body
        user_input = request.GET.get('user_name')
        if user_input == None:
            objs = UserPoints.objects.all()
            de_objs = [{'user_id':o.user_id, 'user_name':o.user_name, 'user_points': o.user_points} for o in objs]
            print de_objs
            return JsonResponse({'all_data':de_objs})
        print user_input
        obj = UserPoints.objects.get(user_name=user_input)
        response = {}
        response['user_name'] = obj.user_name
        response['user_id'] = obj.user_id
        response['user_points'] = obj.user_points
        return JsonResponse(response)

@csrf_exempt
def user_data(request, user_id):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_pan = request.POST.get('user_pan')
        user_dob = request.POST.get('user_dob')
        print user_id, user_name, user_pan, user_dob
        try:
            print UserData.objects.all()
            obj = UserData(user_id_fk = UserPoints(user_id=user_id),
            user_name = user_name,
            user_pan = user_pan,
            user_dob = user_dob)
            obj.save()            
        except Exception as e: 
            print e       
            return HttpResponse(repr(e))
        return HttpResponse("Data saved succesfully")
    
    elif request.method == "GET":
        if not user_id:
            user_input = request.GET.get('user_id')
        else:
            print "direct"
            user_input = user_id
        print type(user_input),"this"
        try:    
            obj = UserData.objects.filter(user_id_fk=user_input).order_by('-user_correction_timestamp').first()
            response = {}
            print obj, "objj"
            response['image_name'] = obj.user_name
            response['image_id'] = obj.user_id_fk.user_id
            response['image_pan'] = obj.user_pan
            response['image_dob'] = obj.user_dob
            response['image_url'] = obj.user_image_url
            response['update_time'] = obj.user_correction_timestamp
            return JsonResponse(response)
        except Exception as e:
            return HttpResponse("User not found")

@csrf_exempt
def edit_data(request, user_id):
    if request.method == "POST":
        if not user_id:
            user_id = request.POST.get('user_id')
        request_data = json.loads(request.body)
        user_name = request_data.get('image_name')
        user_pan = request_data.get('image_pan')
        user_dob = request_data.get('image_dob')
        print user_id, user_name, user_pan, user_dob
        
        try:
            print UserData.objects.all()
            #     obj = UserData(user_id_fk = UserPoints(user_id=user_id),
            #     user_name = user_name,
            #     user_pan = user_pan,
            #     user_dob = user_dob)
            #     obj.save()            
            # except Exception as e: 
            obj = UserData(user_id_fk = UserPoints(user_id=user_id))
            obj.user_name = user_name
            obj.user_pan = user_pan
            obj.user_dob = user_dob
            obj.save()
        except Exception as e: 
            print e      
            return HttpResponse(repr(e))
        return HttpResponse("Data saved succesfully")
