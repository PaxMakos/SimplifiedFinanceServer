from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Transaction
import matplotlib.pyplot as plt
import os


@require_http_methods(["GET"])
@csrf_exempt
def generateGraph(request):
    if request.user.is_authenticated:
        try:
            startDate = request.GET.get("startDate")
            endDate = request.GET.get("endDate")
            project = request.GET.get("project")

            transactions = Transaction.objects.filter(date__range=[startDate, endDate])

            if project:
                transactions = transactions.filter(project__name=project)

            income = 0
            outcome = 0

            for transaction in transactions:
                if transaction.amount > 0:
                    income += transaction.amount
                else:
                    outcome += transaction.amount

            plt.bar(["income", "outcome"], [income, outcome])

            if not os.path.exists("../graphs"):
                os.mkdir("../graphs")

            plt.savefig("../graphs/graph.png")

            with open("../graphs/graph.png", "rb") as file:
                response = HttpResponse(file.read(), content_type="image/png")
                response["Content-Disposition"] = "attachment; filename=graph.png"
                return response
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


