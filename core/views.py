
# coding=utf-8
import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError

from core._core_functions import user_is_crew, get_innlevering_user, can_upload, has_voted
from .models import Compo, Bidrag, BidragFile, InnleveringUser, UserVote


def indexview(request):
    c = {}

    if request.user.is_authenticated():
        c['isLoggedin'] = True

    # Has error?
    if request.GET.get("error"):
        print(request.GET.get("error"))
        if request.GET.get("error") == "1":
            c["errorMessage"] = "Konkurransen er ikke publisert"

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

    # is the compo published?
    if not theCompo.isPublished:
        return HttpResponseRedirect("/?error=1")

    c['pageTitle'] = theCompo.name
    c['compo'] = theCompo
    c['bidrags'] = theCompo.get_bidrag()

    if (theCompo.isVotingMode):
        return compovotingview(request, c)

    if request.GET.get("shighvote"):
        c['bidrags'] = Bidrag.objects.order_by("-votes")

    return componormalview(request, c)


def componormalview(request, c):
    theCompo = c['compo']

    # User has already sent bidrag?
    if request.user.is_authenticated():
        c['isLoggedin'] = True
        c['user'] = request.user
        c['isCrew'] = user_is_crew(request.user)

        bidragUserCompo = Bidrag.objects.filter(compo=theCompo, creator=request.user)
        if bidragUserCompo.count() > 0:
            bidragUserCompo = bidragUserCompo[0]
            c['userHasBidragID'] = bidragUserCompo

    return render(request, 'compos/view.html', c)


def compovotingview(request, c):
    # User has already sent bidrag?
    if request.user.is_authenticated():
        c['isLoggedin'] = True
        c['user'] = request.user
        c['isCrew'] = user_is_crew(request.user)

    return render(request, 'compos/voting.html', c)


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

    # is the compo published?
    if not theCompo.isPublished:
        return HttpResponseRedirect("/?error=1")

    c['pageTitle'] = theCompo.name
    c['compo'] = theCompo
    c['bidrags'] = theCompo.get_bidrag()
    c['isLoggedin'] = True
    c['user'] = request.user
    c['isCrew'] = user_is_crew(request.user)

    if request.GET.get("shighvote"):
        c['bidrags'] = Bidrag.objects.order_by("-votes")

    return render(request, 'compos/see_bidrags.html', c)


# ----------------------------------------------------
# View single bidrag in compo
def composinglebidragview(request, composlug, bidragslug):
    c = {}

    if request.user.is_authenticated() is False:
        return HttpResponseForbidden("You are not logged in")

    # fetch compo and bidrag
    try:
        theCompo = Compo.objects.get(pk=composlug)
        theBidrag = Bidrag.objects.get(id=bidragslug, compo=theCompo)
    except Compo.DoesNotExist:
        raise Http404("Compo was not found")
    except Bidrag.DoesNotExist:
        raise Http404("Bidrag was not found")

    # is the compo published?
    if not theCompo.isPublished:
        return HttpResponseRedirect("/?error=1")

    isOwner = (request.user.id == theBidrag.creator.id)

    # Check if user in session has access to this page.
    # Only crew or uploader can view.
    # When in voting mode, everyone can view an bidrag.
    if not theCompo.isVotingMode and not user_is_crew(request.user) and not isOwner:
        return HttpResponseForbidden("No access")  # No access to view this..

    # Set params for view
    c['pageTitle'] = theBidrag.name + ' / ' + theCompo.name
    c['compo'] = theCompo
    c['bidrag'] = theBidrag
    c['bnumfiles'] = theBidrag.get_num_files()
    c['bfiles'] = theBidrag.get_files()
    c['isLoggedin'] = True
    c['user'] = request.user
    c['isCrew'] = user_is_crew(request.user)
    c['hasAccess'] = True  # Access forbidden is be catched over
    c['compoIsVoting'] = theCompo.isVotingMode

    # Show success message?
    if request.GET.get("uploaded", False):
        c['successMessage'] = "Ditt bidrag har blitt innlevert!"

    # Show error message?
    if request.GET.get("error"):
        c['errorMessage'] = "Du har allerede levert et bidrag!"

    return render(request, 'compos/view_bidrag.html', c)


# ----------------------------------------------------
# View single bidrag in compo
def bidragdelete(request, composlug, bidragslug):
    c = {}

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    # fetch compo
    try:
        theCompo = Compo.objects.get(pk=composlug)
        theBidrag = Bidrag.objects.get(id=bidragslug, compo=theCompo)
    except Compo.DoesNotExist:
        raise Http404("Compo was not found")
    except Bidrag.DoesNotExist:
        raise Http404("Bidrag was not found")

    isOwner = (request.user.id == theBidrag.creator.id)

    # Check if user in session has access to this page.
    # Only crew or uploader can view.
    if not user_is_crew(request.user) and not isOwner:
        return HttpResponseForbidden("No access")  # No access to view this..

    # Delete this bidrag
    theBidrag.delete()

    # Redir to compo
    return HttpResponseRedirect("/view/" + str(theCompo.id) + "/")


# ----------------------------------------------------
# View single bidrag in compo
def bidragvote(request, composlug, bidragslug):
    c = {}

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    # fetch compo
    try:
        theCompo = Compo.objects.get(pk=composlug)
        theBidrag = Bidrag.objects.get(id=bidragslug, compo=theCompo)
    except Compo.DoesNotExist:
        raise Http404("Compo was not found")
    except Bidrag.DoesNotExist:
        raise Http404("Bidrag was not found")

    isOwner = (request.user.id == theBidrag.creator.id)

    if has_voted(request.user, theBidrag):
        return HttpResponseRedirect("/view/" + str(theCompo.id) + "/?voted=false&hasvoted=true#b" + str(theBidrag.id))

    # Check if user in session has access to this page.
    # Only crew or uploader can view.
    if not theCompo.isVotingMode or isOwner:
        return HttpResponseRedirect("/view/" + str(theCompo.id) + "/?voted=false#b" + str(theBidrag.id))

    # Add one vote to this bidrag.
    theBidrag.votes += 1
    theBidrag.save()

    vote = UserVote(user=request.user, bidrag=theBidrag)
    vote.save()

    # Redir to compo
    return HttpResponseRedirect("/view/" + str(theCompo.id) + "/?voted=true#b" + str(theBidrag.id))


# ----------------------------------------------------
# View single bidrag in compo
def bidrageditsave(request, composlug, bidragslug):
    c = {}

    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    # fetch compo
    try:
        theCompo = Compo.objects.get(pk=composlug)
        theBidrag = Bidrag.objects.get(id=bidragslug, compo=theCompo)
    except Compo.DoesNotExist:
        raise Http404("Compo was not found")
    except Bidrag.DoesNotExist:
        raise Http404("Bidrag was not found")

    isOwner = (request.user.id == theBidrag.creator.id)

    # Check if user in session has access to this page.
    # Only crew or uploader can view.
    if not user_is_crew(request.user) and not isOwner:
        return HttpResponseForbidden("No access")  # No access to view this..

    # Save this bidrag
    theBidrag.name = request.POST["title"]
    theBidrag.data = request.POST["data"]
    theBidrag.save()

    # Redir to compo
    return HttpResponseRedirect("/view/" + str(theCompo.id) + "/b/" + str(theBidrag.id) + "/")


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
    theCompo = get_object_or_404(Compo, id=composlug)

    # is the compo published?
    if not theCompo.isPublished:
        return HttpResponseRedirect("/?error=1")

    c['canUpload'] = can_upload(request.user)
    c['compo'] = theCompo

    return render(request, 'upload.html', c)


#-----------------------------------------------------
# Login form
def loginview(request):
    c = {}

    if request.method == 'GET' and int(request.GET['id']) > 0 and request.GET['timestamp'] and request.GET['token']:
        # Validate the session from GE
        params = {"user_id": request.GET['id'], "timestamp": request.GET['timestamp'], "token": request.GET['token']}
        r = requests.post("https://www.geekevents.org/sso/validate/", params)
        rj = r.json()

        if rj['status']:
            # Create an user in the our database with extra information.
            foundUser = InnleveringUser.objects.filter(geID=request.GET['id'])

            # Has user?
            if foundUser.count() < 1:
                # Create a new user for this one.
                # Fetch userinfo
                userinfo = requests.post("https://www.geekevents.org/sso/userinfo/", params)
                userinfojson = userinfo.json()
                if userinfojson['status'] is False:
                    raise HttpResponse("Userinfo request failed, contact game-desk!")

                user = User.objects.create_user(username=userinfojson['username'])
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                innleveringuser = InnleveringUser(geID=int(request.GET['id']), geUsername=userinfojson['username'], user=user)
                innleveringuser.save()
            else:
                innleveringuser = foundUser[0]
                user = User.objects.get(pk=innleveringuser.user.id)
                user.backend = 'django.contrib.auth.backends.ModelBackend'

            innleveringuser.currenttoken = request.GET["token"]
            innleveringuser.currenttimestamp = request.GET["timestamp"]
            innleveringuser.save()

            # Login the user
            login(request, user)
            return HttpResponseRedirect("/?login=true")

    return HttpResponseRedirect("/?login=failed")


#-----------------------------------------------------
# View users bidrags
def mybidrags(request):
    if request.user.is_authenticated() is not True:
        return HttpResponseRedirect("/")

    c = {}
    c['isLoggedin'] = True
    c['bidrags'] = Bidrag.objects.filter(creator=request.user)

    return render(request, "account/mybidrags.html", c)


#-----------------------------------------------------
# Logout form
def logouthandle(request):

    # Clear API variables
    innleveringuser = get_innlevering_user(request.user)
    if innleveringuser:
        innleveringuser.currenttoken = ""
        innleveringuser.currenttimestamp = ""
        innleveringuser.save()

    logout(request)
    return HttpResponseRedirect("/")


# ----------------------------------------------------
# Upload handler
def uploadhandler(request, composlug):
    c = {}

    theCompo = get_object_or_404(Compo, id=composlug)

    # Check if the user already has uploaded
    userBidragsInCompo = Bidrag.objects.filter(creator=request.user, compo=theCompo)
    if userBidragsInCompo.count() > 0:
        # User has already uploaded a bidrag
        theBidragUserHas = userBidragsInCompo[0]

        # Return to the bidrag
        return HttpResponseRedirect("/view/" + str(theCompo.id) + "/b/" + str(theBidragUserHas.id) + "/?error=1")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        instance = Bidrag(compo=theCompo, creator=request.user, votes=0, name=request.POST['title'])
        instance.save()

        for afile in request.FILES.getlist("files"):
            BidragFile(bidrag=instance, file=afile).save()

        return HttpResponseRedirect('/view/' + str(theCompo.id) + '/b/' + str(instance.id) + '/?uploaded=true')

    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponseRedirect('/view/' + str(theCompo.id) + '/upload/')
