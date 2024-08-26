from django.shortcuts import redirect
from django.urls import reverse


def redirect_to_docs(request):
    return redirect(reverse("swagger-ui"))
