from django.shortcuts import render
from django.http import JsonResponse
from .model_loader import MODEL, CLASS_NAMES  # ✅ Import model from model_loader.py
import numpy as np
import os
import requests
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from PIL import Image
from io import BytesIO

FASTAPI_URL = "http://127.0.0.1:8000/upload"  # ✅ Update with the correct FastAPI URL

def home(request):
    user = request.user
    return render(request, "index.html", {"user": user})    

@login_required(login_url='/login')
def dashboard_view(request):
    user = request.user
    is_farmer = auth.is_farmer(user)
    is_agrovet = auth.is_agrovet(user)

    template = None

    if is_farmer:
        template = "farmer_dashboard.html"
    elif is_agrovet:
        template = "agrovet_dashboard.html"

    if not template:
        return HttpResponse("Something went wrong!")
    
    return render(request, template, {"user": user})
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
            # response = requests.post(url=FASTAPI_URL, files={"file": (file.name, file.read())})
            # return JsonResponse(response.json(), safe=False)
            #image = file.read()
            # Read the image file and convert it to a NumPy array
            image = Image.open(file)  # Open image using PIL
            image = image.convert("RGB")  # Ensure it's in RGB mode
            img_array = np.array(image)  # Convert to NumPy array
            img_batch = np.expand_dims(img_array, axis=0)

            predictions = MODEL.predict(img_batch)

            predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
            confidence = float(np.max(predictions[0]))

            print(f"Prediction: {predicted_class}, Confidence: {confidence:.2f}")

            return JsonResponse({
                "class": predicted_class,
                "confidence": round((confidence*100), 1)
            }, status=200) 
        except requests.RequestException as e:
            print(f"Failed to connect to FastAPI: {str(e)}")
            return JsonResponse({"error": f"Failed to connect to FastAPI: {str(e)}"}, status=500)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

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


def logout_view(request):
    logout(request)
    return redirect('home')


def agrovet_dashboard(request):
    if request.user.is_authenticated and request.user.is_agrovet:
        agrovet = request.user.agrovet_profile
        products = agrovet.products.all()
        orders = agrovet.orders.all()
        context = {
            'agrovet': agrovet,
            'products': products,
            'orders': orders
        }
        return render(request, 'agrovet_dashboard.html', context)
    else:
        return redirect('login')
