from django.contrib.auth  import login, logout, authenticate
from django.contrib.auth.models import User, Group
from . import models

def is_agrovet(user):
  return user.groups.filter(name="agrovet").exists()

def is_farmer(user):
  return user.groups.filter(name="farmer").exists()

def create_group(group_name):
  try:
    group, _ = Group.objects.get_or_create(name=group_name)
    return True, group
  except Exception as e:
    return False, {
      "message": f"Error: {e}",
      "status": 500
    }

def add_user_to_group(user, group_name):
  try:
    is_success, group = create_group(group_name)
    if not is_success:
      return False, group
    
    group.user_set.add(user)
    print("User added to group")
    return True, None
  except Exception as e:
    print(f"Error: {e}")
    return False, {
      "message": f"Error: {e}",
      "status": 500
    }

def login_fn(request, email=None, password=None):

  if not(email and password):
    return False, {
      "message":"Email, password required",
      "status": 401
    }
  try:
    user = authenticate( request,username=email, password=password)

    if user is None:
      return False, {
        "message": "Incorrect credentials",
        "status": 401
      }

    login(request, user)

    return True, {
      "message": "Login successfully",
      "status": 200,
      "redirect_url": ""
    }
  except Exception as e:
    return False, {
      "message": f"Error: {e}",
      "status": 500
    }

    
  
def create_user(user_data={}):
  try:
    if len(user_data) == 0:
      print("Missing data")
      return False, {
        "message":"Missing data",
        "status": 400
      }
    username = user_data.get("email", None)
    first_name = user_data.get("first_name", None)
    last_name = user_data.get("last_name", None)
    password = user_data.get("password", None)
    group_name = user_data.get("group_name", None)

    user = User.objects.create_user(
      username=username,
      email=username,
      first_name=first_name,
      last_name=last_name,
      password=password
    )
    
    _ = add_user_to_group(user, group_name)

    print("User created successfully")

    return True, user

  except Exception as e:
    print(f"Error account: {e}")
    return False, {
      "message": f"Error: {e}",
      "status": 500
    }

def register_farmer(farmer_data={}):
  if len(farmer_data) == 0:
    return False, {
      "message": "Missing data",
      "status": 400
    }

  try:
    first_name = farmer_data.get("first_name", None)
    last_name = farmer_data.get("last_name", None)
    email = farmer_data.get("email", None)
    phone_number = farmer_data.get("phone_number", None)
    location = farmer_data.get("location", None)
    farm_size = farmer_data.get("farm_size", None)
    type_of_crops = farmer_data.get("type_of_crops", None)
    password = farmer_data.get("password", None)


    is_sucess, response = create_user(user_data=farmer_data)

    if not is_sucess:
      return response

    user = response

    new_farmer = models.Farmer.objects.create(
      first_name=first_name,
      last_name=last_name,
      user=user,
      email=email,
      phone_number=phone_number,
      farm_location=location,
      farm_size=farm_size,
      type_of_crops=type_of_crops
    )

    new_farmer.save()

    return True, {
      "message": "Farmer registered successfully",
      "status": 200
    }

  except Exception as e:
    print(f"Error: {e}")
    return False, {
      "message": f"Error: {e}",
      "status": 500
    }

def register_agrovet(data={}):
  if len(data) == 0:
    print("Missing data. Agrovet data required")
    return False, {
      "message": "Missing data",
      "status": 400
    }

  try:
    first_name = data.get("first_name", None)
    last_name = data.get("last_name", None)
    email = data.get("email", None)
    phone_number = data.get("phone_number", None)
    location = data.get("location", None)
    agrovet_name = data.get("agrovet_name", None)
    business_licence_number = data.get("business_licence_number", None)
    password = data.get("password", None)

    is_sucess, response = create_user(user_data=data)

    if not is_sucess:
      print(f"Response account: {response}")
      return response

    user = response

    new_agrovet = models.Agrovet.objects.create(
      first_name=first_name,
      last_name=last_name,
      user=user,
      email=email,
      phone_number=phone_number,
      agrovet_location=location,
      agrovet_name=agrovet_name,
      business_licence_number=business_licence_number
    )

    new_agrovet.save()

    return True, {
      "message": "Agrovet registered successfully",
      "status": 200
    }

  except Exception as e:
    print(f"Error aggrovet: {e}")
    return False, {
      "message": f"Error: {e}",
      "status": 500
    }
