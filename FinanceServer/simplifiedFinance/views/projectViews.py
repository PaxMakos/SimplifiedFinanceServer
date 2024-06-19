from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Project, Permissions
from django.db import IntegrityError


@require_http_methods(["GET"])
@csrf_exempt
def getProjects(request):
    # If the user is authenticated, return all projects the user has access to
    try:
        if request.user.is_authenticated:
            projects = Project.objects.all()

            if not request.user.is_superuser:
                permissions = Permissions.objects.filter(user=request.user)
                projects = [p.project for p in permissions]

            toReturn = []

            for project in projects:
                toReturn.append({"name": project.name,
                                 "description": project.description,
                                 "startDate": project.startDate,
                                 "endDate": project.endDate,
                                 "status": project.status})

            return JsonResponse({"status": "success", "projects": toReturn})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createProject(request):
    # If user is superuser, create a new project
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            name = request.POST.get("projectName")
            description = request.POST.get("projectDescription")
            startDate = request.POST.get("projectStartDate")
            endDate = request.POST.get("projectEndDate")
            status = request.POST.get("projectStatus")

            if not name or not startDate or not endDate or not status:
                raise ValueError("Missing required fields")

            if Project.objects.filter(name=name).exists():
                raise IntegrityError("Project already exists")
            else:
                project = Project(name=name,
                                  description=description,
                                  startDate=startDate,
                                  endDate=endDate,
                                  status=status)
                project.save()

            return JsonResponse({"status": "success", "message": f"Project {name} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except IntegrityError as e:
        return JsonResponse({"status": "error", "message": str(e)})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteProject(request, name):
    # If user is superuser, delete a project
    try:
        if request.user.is_authenticated and request.user.is_superuser:

            project = Project.objects.get(name=name)
            project.delete()
            return JsonResponse({"status": "success", "message": f"Project {name} deleted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Project.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Project does not exist"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Project is in use"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["PUT"])
@csrf_exempt
def endProject(request, name):
    # If user is superuser, end a project, changing its status to "Completed"
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            project = Project.objects.get(name=name)
            project.status = "Completed"
            project.save()
            return JsonResponse({"status": "success", "message": f"Project {name} completed"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Project.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Project does not exist"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
