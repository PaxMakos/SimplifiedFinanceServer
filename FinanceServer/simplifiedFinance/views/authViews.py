from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ..models import Permissions, Project


@require_http_methods(["POST"])
@csrf_exempt
def loginToApp(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        sessionKey = request.session.session_key
        return JsonResponse({"status": "success", "sessionKey": sessionKey})
    else:
        return JsonResponse({"status": "error", "message": "Invalid credentials"})


@require_http_methods(["POST"])
@csrf_exempt
def logoutFromApp(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def registerUser(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    try:
        if User.objects.filter(username=username).exists():
            raise ValidationError("User already exists")

        if len(password) < 8:
            raise ValidationError("Password is too short")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return JsonResponse({"status": "success"})
    except ValidationError as e:
        return JsonResponse({"status": "validationError", "message": e.message})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def sessionInfo(request):
    if request.user.is_authenticated:
        sessionKey = request.session.session_key
        return JsonResponse({"status": "success", "sessionKey": sessionKey})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["GET"])
@csrf_exempt
def getPermissions(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            permissions = Project.objects.all()
            return JsonResponse({"status": "success", "permissions": [p.name for p in permissions]})
        else:
            permissions = Permissions.objects.filter(user=request.user)
            return JsonResponse({"status": "success", "permissions": [p.project.name for p in permissions]})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def givePermissions(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = User.objects.get(username=request.POST.get("user"))
            project = Project.objects.get(name=request.POST.get("project"))

            if Permissions.objects.filter(user=user, project=project).exists():
                return JsonResponse({"status": "error", "message": "Permissions already granted"})
            else:
                Permissions.objects.create(user=user, project=project)
                return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["DELETE"])
@csrf_exempt
def removePermissions(request, user, project):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = User.objects.get(username=user)
            project = Project.objects.get(name=project)

            if Permissions.objects.filter(user=user, project=project).exists():
                Permissions.objects.filter(user=user, project=project).delete()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "Permissions not granted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})