from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Return, Project


@require_http_methods(["POST"])
@csrf_exempt
def createReturn(request):
    # create a new return, available even if the user is not authenticated
    try:
        project = Project.objects.get(name=request.POST.get("projectName"))
        title = request.POST.get("returnTitle")
        date = request.POST.get("returnDate")
        amount = float(request.POST.get("returnAmount"))
        description = request.POST.get("returnDescription")
        accountToReturn = request.POST.get("accountToReturn")
        invoice = request.FILES.get("invoice")

        if not project or not title or not date or not amount or not accountToReturn:
            return JsonResponse({"status": "error", "message": "Missing required fields"})

        returnObj = Return(project=project,
                           title=title,
                           date=date,
                           amount=amount,
                           description=description,
                           accountToReturn=accountToReturn,
                           invoice=invoice)
        returnObj.save()

        return JsonResponse({"status": "success", "message": "Return created"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getReturns(request):
    # If the user is authenticated and is a superuser, return all returns
    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteReturn(request, returnId):
    # If the user is authenticated and is a superuser, delete the return
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            returnObj = Return.objects.get(id=returnId)
            returnObj.delete()
            return JsonResponse({"status": "success", "message": f"Return {returnId} deleted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

