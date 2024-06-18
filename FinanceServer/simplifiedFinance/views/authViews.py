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
    # log in to the app
    try:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            sessionKey = request.session.session_key
            return JsonResponse({"status": "success", "sessionKey": sessionKey})
        else:
            return JsonResponse({"status": "error", "message": "Invalid credentials"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def logoutFromApp(request):
    # log out from the app
    try:
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({"status": "success", "message": f"User {request.user.username} logged out"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def registerUser(request):
    # register a new user
    try:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username is None or password is None:
            raise ValidationError("Missing required fields")

        if User.objects.filter(username=username).exists():
            raise ValidationError("User already exists")

        if len(password) < 8:
            raise ValidationError("Password is too short")

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return JsonResponse({"status": "success", "message": f"User {username} registered"})
    except ValidationError as e:
        return JsonResponse({"status": "validationError", "message": e.message})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def sessionInfo(request):
    # get session info
    try:
        if request.user.is_authenticated:
            sessionKey = request.session.session_key
            return JsonResponse({"status": "success", "sessionKey": sessionKey})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getUsers(request):
    # If user is superuser, return all users
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            users = User.objects.all()

            toReturn = []

            for user in users:
                toReturn.append({
                    "username": user.username,
                    "isSuperuser": user.is_superuser
                })

            return JsonResponse({"status": "success", "users": toReturn})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def isSuperuser(request):
    # check if user is superuser
    try:
        if request.user.is_authenticated:
            return JsonResponse({"status": "success", "message": request.user.is_superuser})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getPermissions(request):
    # get projects that user has permissions to, superuser gets all projects
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                permissions = Project.objects.all()

                return JsonResponse({"status": "success", "permissions": [p.name for p in permissions]})
            else:
                permissions = Permissions.objects.filter(user=request.user)
                return JsonResponse({"status": "success", "permissions": [p.project.name for p in permissions]})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getAllPermissions(request):
    # get permissions for all users
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            permissions = Permissions.objects.all()

            toReturn = []

            for p in permissions:
                toReturn.append({
                    "user": p.user.username,
                    "project": p.project.name
                })

            return JsonResponse({"status": "success", "permissions": toReturn})
        else:
            return JsonResponse({"status": "error", "message": "User is not superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def givePermission(request):
    # give permission to user for project
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            user = User.objects.get(username=request.POST.get("user"))
            project = Project.objects.get(name=request.POST.get("projectName"))

            if user is None or project is None:
                return JsonResponse({"status": "error", "message": "Missing required fields"})

            if Permissions.objects.filter(user=user, project=project).exists():
                return JsonResponse({"status": "error", "message": "Permissions already granted"})
            else:
                Permissions.objects.create(user=user, project=project)
                return JsonResponse({"status": "success",
                                     "message": f"Permissions granted to {user.username} for {project.name}"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def removePermission(request, user, project):
    # remove permission from user for project
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            user = User.objects.get(username=user)
            project = Project.objects.get(name=project)

            if Permissions.objects.filter(user=user, project=project).exists():
                Permissions.objects.filter(user=user, project=project).delete()
                return JsonResponse({"status": "success",
                                     "message": f"Permissions removed from {user.username} for {project.name}"})
            else:
                return JsonResponse({"status": "error", "message": "Permissions not granted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except:
        return JsonResponse({"status": "error", "message": "Error"})
