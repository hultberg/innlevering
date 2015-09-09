from pprint import pprint
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from core._core_functions import user_is_crew

from .models import Compo, Bidrag, BidragFile


def indexview(request):
    c = {}

    if request.user.is_authenticated():
        c['isLoggedin'] = True

    # fetch compos
    c['compos'] = Compo.objects.filter()
    return render(request, 'index.html', c)


# ----------------------------------------------------
# View compo	
def compoview(request, composlug):
    c = {}

    # fetch compo
    try:
        theCompo = Compo.objects.get(pk=composlug)
    except Compo.DoesNotExist:
        raise Http404("Compo was not found")

    c['pageTitle'] = theCompo.name
    c['compo'] = theCompo
    c['bidrags'] = theCompo.get_bidrag()

    if request.user.is_authenticated():
        c['isLoggedin'] = True
        c['user'] = request.user
        c['isCrew'] = user_is_crew(request.user)

    return render(request, 'compos/view.html', c)


# ----------------------------------------------------
# View bidrags in compo
def compobidragview(request, composlug):
    c = {}

    if not request.user.is_authenticated() or not user_is_crew(request.user):
        return HttpResponseForbidden()

    # fetch compo
    try:
        theCompo = Compo.objects.get(pk=composlug)
    except Compo.DoesNotExist:
        raise Http404("Compo was not found")

    c['pageTitle'] = theCompo.name
    c['compo'] = theCompo
    c['bidrags'] = theCompo.get_bidrag()
    c['isLoggedin'] = True
    c['user'] = request.user
    c['isCrew'] = user_is_crew(request.user)

    return render(request, 'compos/see_bidrags.html', c)


# ----------------------------------------------------
# View single bidrag in compo
def composinglebidragview(request, composlug, bidragslug):
    c = {}

    if not request.user.is_authenticated() or not user_is_crew(request.user):
        return HttpResponseForbidden()

    # fetch compo
    try:
        theCompo = Compo.objects.get(pk=composlug)
        theBidrag = Bidrag.objects.get(id=bidragslug, compo=theCompo)
    except Compo.DoesNotExist:
        raise Http404("Compo was not found")
    except Bidrag.DoesNotExist:
        raise Http404("Bidrag was not found")

    c['pageTitle'] = theBidrag.name + ' / ' + theCompo.name
    c['compo'] = theCompo
    c['bidrag'] = theBidrag
    c['bnumfiles'] = theBidrag.get_num_files()
    c['bfiles'] = theBidrag.get_files()
    c['isLoggedin'] = True
    c['user'] = request.user
    c['isCrew'] = user_is_crew(request.user)

    return render(request, 'compos/view_bidrag.html', c)


# ----------------------------------------------------
# Account view
def accountview(request):
    c = {}

    if request.user.is_authenticated() is not True:
        return HttpResponseRedirect("/")

    c['isLoggedin'] = True
    c['user'] = request.user

    return render(request, 'account/view.html', c)


# ----------------------------------------------------
# Upload bidrag	
def uploadview(request, composlug):
    c = {}

    if request.user.is_authenticated() is not True:
        return HttpResponseRedirect("/")

    c['isLoggedin'] = True
    c['user'] = request.user

    # fetch compo
    c['compo'] = get_object_or_404(Compo, id=composlug)
    return render(request, 'upload.html', c)


#-----------------------------------------------------
# Register form
def registerview(request):
    c = {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']

        if len(username) > 0 and len(email) > 0 and len(password) > 0 and len(firstName) > 0 and len(lastName) > 0:
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = firstName
                user.last_name = lastName
                user.save()
                c['createdUser'] = username
            except IntegrityError:
                c['error_message'] = 'Brukernavnet finnes allerede'
        else:
            c['error_message'] = 'Alle felter er påkrevd'

    return render(request, "account/register.html", c)


#-----------------------------------------------------
# Login form
def loginview(request):
    c = {}

    if request.method == 'POST':
        gotUsername = request.POST['username']
        gotPassword = request.POST['password']

        if len(gotUsername) > 0 and len(gotPassword) > 0:
            user = authenticate(username=gotUsername, password=gotPassword)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    c['error_message'] = 'Brukeren er deaktivert'
            else:
                c['error_message'] = 'Brukernavn eller passord er feil'
        else:
            c['error_message'] = 'Alle felter er påkrevd'

    return render(request, "account/login.html", c)


#-----------------------------------------------------
# Logout form
def logouthandle(request):
    logout(request)
    return HttpResponseRedirect("/")


# ----------------------------------------------------
# Upload handler
def uploadhandler(request, composlug):
    c = {}

    theCompo = get_object_or_404(Compo, id=composlug)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        instance = Bidrag(compo=theCompo, creator=request.user, votes=0, name=request.POST['title'])
        instance.save()

        for afile in request.FILES.getlist("files"):
            BidragFile(bidrag=instance, file=afile).save()

        return HttpResponseRedirect('/view/' + str(theCompo.id) + '/')

    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponseRedirect('/view/' + str(theCompo.id) + '/upload/')
