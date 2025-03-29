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
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.models import User
from .models import Diagnosis, Treatment, Resource, Farmer, Agrovet, Product
from collections import Counter
import json


FASTAPI_URL = "http://127.0.0.1:8000/upload"  # ✅ Update with the correct FastAPI URL

def home(request):
    user = request.user
    return render(request, "index.html", {"user": user})    

def get_farmer_data(user):
    """Fetches farmer-related data including name, location, diagnosis history, and farm status."""
    try:
        farmer = Farmer.objects.get(user=user)
        farmer_data = {
            "name": f"{farmer.first_name} {farmer.last_name}",
            "location": farmer.farm_location if farmer.farm_location else "N/A",
        }

        # Get last 10 diagnosis history
        activity_history = Diagnosis.objects.filter(user=user).order_by('-date')[:10]
        farmer_data["activity_history"] = [
            {
                "date": diagnosis.date.strftime("%Y-%m-%d %H:%M:%S"),
                "diagnosis": diagnosis.disease_detected,
                "recommendation": diagnosis.recommendation,
            }
            for diagnosis in activity_history
        ]

        farmer_diagnosis = Diagnosis.objects.filter(user=user)
        farmer_data["farm_status"] = determine_farm_status(farmer_diagnosis)
        farmer_data["total_diagnoses"] = farmer_diagnosis.count()

        return farmer_data
    except Farmer.DoesNotExist:
        return {"error": "Farmer not found"}
    except Exception as e:
        return {"error": str(e)}

def get_agrovet_data(user):
    """Fetches agrovet-related data including name, location, and available products."""
    try:
        agrovet = Agrovet.objects.get(user=user)
        agrovet_data = {
            "name": f"{agrovet.first_name} {agrovet.last_name}",
            "location": agrovet.agrovet_location if agrovet.agrovet_location else "N/A",
        }

        products = agrovet.products.all()
        agrovet_data["products"] = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "stock_quantity": product.stock_quantity,
                "low_stock": product.is_low_stock(),
            }
            for product in products
        ]

        return agrovet_data
    except Agrovet.DoesNotExist:
        return {"error": "Agrovet not found", "products": []}
    except Exception as e:
        return {"error": str(e)}

def determine_farm_status(diagnoses):
    """Determines farm health status based on diagnosis records."""
    disease_counts = Counter(diagnosis.disease_detected for diagnosis in diagnoses)
    total_diagnoses = sum(disease_counts.values())

    if total_diagnoses == 0:
        return "No Data Available"

    healthy_count = disease_counts.get("Healthy", 0)
    early_blight_count = disease_counts.get("Early Blight", 0)
    late_blight_count = disease_counts.get("Late Blight", 0)
    diseased_count = early_blight_count + late_blight_count

    if healthy_count > diseased_count:
        return "Healthy"
    elif early_blight_count > late_blight_count and early_blight_count >= 0.3 * total_diagnoses:
        return "Early Blight Detected"
    elif late_blight_count > early_blight_count and late_blight_count >= 0.3 * total_diagnoses:
        return "Late Blight Detected"
    elif diseased_count >= 0.5 * total_diagnoses:
        return "Poor Health"
    else:
        return "Uncertain"

@login_required(login_url='/login')
def dashboard_view(request):
    """Handles dashboard view for both farmers and agrovets."""
    user = request.user
    is_farmer = auth.is_farmer(user)
    is_agrovet = auth.is_agrovet(user)

    user_data = {}

    if is_farmer:
        user_data = get_farmer_data(user)
        template = "farmer_dashboard.html"
    elif is_agrovet:
        user_data = get_agrovet_data(user)
        template = "agrovet_dashboard.html"
    else:
        return HttpResponse("Something went wrong!")

    return render(request, template, {"user": user_data})


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


# Report View
def download_report(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    # Check if user is a farmer or an agrovet
    if auth.is_farmer(request.user):
        user_data = get_farmer_data(request.user)
        user_type = "Farmer"
    elif auth.is_agrovet(request.user):
        user_data = get_agrovet_data(request.user)
        user_type = "Agrovet"
    else:
        return HttpResponse("User type not recognized", status=400)

    resources = Resource.objects.filter(user=request.user) | Resource.objects.filter(is_global=True)

    # Create context with user data
    context = {
        "user": request.user,
        "user_type": user_type,
        "farm_status": user_data.get("farm_status", "Unknown"),
        "total_diagnoses": user_data.get("total_diagnoses", 0),
        "successful_treatments": user_data.get("successful_treatments", 0),
        "activity_history": user_data.get("activity_history", []),
        "resources": resources,
        "products": user_data.get("products", []),  # Only applies for agrovets
    }

    # Create PDF response
    template_path = "farmer_report_template.html" if user_type == "Farmer" else "agrovet_report_template.html"
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="farm_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response




@csrf_exempt
def products_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            agrovet = Agrovet.objects.get(user=request.user)

            product = Product.objects.create(
                agrovet=agrovet,
                name=data.get("name"),
                description=data.get("description"),
                price=data.get("price"),
                stock_quantity=data.get("stock_quantity"),
            )

            return JsonResponse({"message": "Product added successfully!", "product_id": product.id}, status=201)

        except Agrovet.DoesNotExist:
            return JsonResponse({"error": "Agrovet not found for this user"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)