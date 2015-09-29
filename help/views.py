from django.shortcuts import render


def helpindex(request):
    return render(request, "help/index.html")