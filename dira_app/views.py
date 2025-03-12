from django.shortcuts import render
from django.http import JsonResponse
from .model_loader import MODEL, CLASS_NAMES  # ✅ Import model from model_loader.py
import numpy as np
import os
import requests
from tensorflow.keras.preprocessing import image
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import auth


FASTAPI_URL = "http://127.0.0.1:7000/upload"  # ✅ Update with the correct FastAPI URL

def home(request):
    user = request.user
    return render(request, "index.html", {"user": user})    

def login_view(request):

    if request.method == "GET":
        return render(request, "login.html") 

    elif request.method != "POST":
        return JsonResponse({
            "message": "Method not allowed",
            "status": 400
        }, status=400)

    try:

        email = request.POST.get("email", None)
        password = request.POST.get("password", None)

        if not(email and password):
            return JsonResponse({
                "message": "Email and password required.",
                "status": 400
            }, status =400)

        _, response = auth.login_fn(request=request, email=email, password=password)

        return JsonResponse(response, status=response["status"])

    except Exception as e:
        return JsonResponse({
            "message": f"Error: {e}",
            "status": 500
        }, status=500)



def signup_f_view(request):
    if request.method == "GET":
        return render(request, "signup_f.html")

    elif request.method != "POST":
        return JsonResponse({
            "message": "Method not allowed",
            "status": 400
        }, status=400)
    
    try:
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        phone_number = request.POST.get("phone_number", None)
        farm_location = request.POST.get("farm_location", None)
        farm_size = request.POST.get("farm_size", None)
        type_of_crops = request.POST.get("type_of_crops", None)

        if not(first_name and last_name and email and phone_number and farm_size and type_of_crops and password):
            return JsonResponse({
                "message": "All fields are required",
                "status": 400
            }, status=400)

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "farm_location": farm_location,
            "password": password,
            "farm_size": farm_size,
            "type_of_crops": type_of_crops,
            "group_name": "farmer"
        }

        _, response = auth.register_farmer(farmer_data=user_data)

        return JsonResponse(response, status=response["status"])

    except Exception as e:
        return JsonResponse({
            "message": f"Error: {e}",
            "status": 500
        }, status=500)

def signup_a_view(request):

    if request.method == "GET":
        return render(request, "signup_a.html")

    if request.method != "POST":
        return JsonResponse({
            "message": "Method not allowed",
            "status": 400
        }, status=400)

    try:
        print("Request: ", request.POST)
        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)
        email = request.POST.get("email", None)
        phone_number = request.POST.get("phone_number", None)
        agrovet_name = request.POST.get("agrovet_name", None)
        agrovet_location = request.POST.get("agrovet_location", None)
        business_licence_number = request.POST.get("business_licence_number", None)
        password = request.POST.get("password", None)
        if not(first_name and last_name and email and phone_number and agrovet_name  and business_licence_number and password):
            return JsonResponse({
                "message": "All fields are required",
                "status": 400
            }, status=400)

        print(f"password {password}")
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "agrovet_name": agrovet_name,
            "agrovet_location": agrovet_location,
            "business_licence_number": business_licence_number,
            "group_name": "agrovet"
        }

        _, server_response = auth.register_agrovet(data=user_data)

        print(f"Response server: {server_response}")

        return JsonResponse(server_response, safe=False)
    except Exception as e:
        print(f"Error view: {e}")
        return JsonResponse({
            "message": f"Error: {e}",
            "status": 500
        }, status=500)
@csrf_exempt
def upload_view(request):
    return render(request, "upload.html") 

@csrf_exempt
def fastapi_proxy(request):
    """
    Forwards requests to the FastAPI server.
    """
    if request.method == "GET":
        return JsonResponse({"message": "Upload page is accessible"}, status=200)

    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        try:
            response = requests.post(FASTAPI_URL, files={"file": (file.name, file.read())})
            return JsonResponse(response.json(), safe=False)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Failed to connect to FastAPI: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)  # 405: Method Not Allowed

@csrf_exempt
def predict_view(request):
    if request.method == "POST":
        file = request.FILES.get("file")  # ✅ Get the uploaded file
        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        try:
            # Save the uploaded image temporarily
            img_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(img_path, "wb") as f:
                f.write(file.read())

            # Load and preprocess the image
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0) / 255.0

            # Model prediction
            prediction = MODEL.predict(img_array)
            result = CLASS_NAMES[np.argmax(prediction)]

            # Cleanup temporary image
            os.remove(img_path)

            return JsonResponse({"prediction": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)  # ✅ Catch exceptions

    return JsonResponse({"error": "Invalid request method"}, status=405)  # ✅ Return proper status code
