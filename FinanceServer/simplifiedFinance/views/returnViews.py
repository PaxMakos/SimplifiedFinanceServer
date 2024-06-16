from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Return, Project


@require_http_methods(["POST"])
@csrf_exempt
def createReturn(request):
    try:
        project = Project.objects.get(name=request.POST.get("projectName"))
        title = request.POST.get("returnTitle")
        date = request.POST.get("returnDate")
        amount = float(request.POST.get("returnAmount"))
        description = request.POST.get("returnDescription")
        accountToReturn = request.POST.get("accountToReturn")
        invoice = request.FILES.get("invoice")

        returnObj = Return(project=project,
                           title=title,
                           date=date,
                           amount=amount,
                           description=description,
                           accountToReturn=accountToReturn,
                           invoice=invoice)
        returnObj.save()

        return JsonResponse({"status": "success", "return": returnObj.id})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getReturns(request):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            returns = Return.objects.all()
            returnList = []
            for returnObj in returns:
                returnList.append({"id": returnObj.id,
                                   "project": returnObj.project.name,
                                   "title": returnObj.title,
                                   "date": returnObj.date,
                                   "amount": returnObj.amount,
                                   "description": returnObj.description,
                                   "accountToReturn": returnObj.accountToReturn})
            return JsonResponse({"status": "success", "returns": returnList})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated or is not a superuser"})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteReturn(request, returnId):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            returnObj = Return.objects.get(id=returnId)
            returnObj.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not a superuser"})
