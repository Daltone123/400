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


FASTAPI_URL = "http://127.0.0.1:7000/upload"  # ✅ Update with the correct FastAPI URL

def home(request):
    return render(request, "index.html")

def login_view(request):
    return render(request, "login.html") 

def signup_f_view(request):
    return render(request, "signup_f.html") 

def signup_a_view(request):
    return render(request, "signup_a.html") 

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
