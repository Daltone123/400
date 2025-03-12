from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from fastapi.middleware.wsgi import WSGIMiddleware
from dira_app.dira import app  # Import FastAPI app

urlpatterns = [
    path("fastapi/", csrf_exempt(WSGIMiddleware(app))),
    path("", views.home, name="home"),
    path("upload/", views.upload_view, name="upload"),  # ✅ FIXED
    path("predict/", views.fastapi_proxy, name="predict"),  
    path("login", views.login_view, name="login"),
    path("signup_f", views.signup_f_view, name="signup_f"),
    path("signup_a", views.signup_a_view, name="signup_a"),
]
