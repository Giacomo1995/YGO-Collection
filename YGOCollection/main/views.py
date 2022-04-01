from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from urllib import parse
from .models import *
from .forms import CreateSet
import requests
import os


def forbidden(request, exception, templatename=os.path.join('main', '403.html')):
    response = render_to_response(templatename)
    response.status_code = 403
    return response


def notfound(request, exception, templatename=os.path.join('main', '404.html')):
    response = render_to_response(templatename)
    response.status_code = 404
    return response


def servererror(request, *args, **argv):
    return render(request, os.path.join('main', '500.html'), status=500)


def home(request):
    if request.method == 'POST':
        if request.POST.get('delete'):
            for item in UserSet.objects.all():
                if request.POST.get(str(item.id)) == 'clicked':
                    item.delete()
    return render(request, os.path.join('main', 'home.html'), {'usersetlist': list(UserSet.objects.all().values())})


def cardlist(request, setname):
    if request.method == 'POST':
        if request.POST.get('delete'):
            for item in Card.objects.all():
                if request.POST.get(str(item.id)) == 'clicked':
                    item.delete()
                    setid = UserSet.objects.get(name=item.userset).id
                    usrset = UserSet.objects.get(id=setid)
                    if item.collected:
                        usrset.collected -= 1
                    else:
                        usrset.missing -= 1
                    usrset.save()
        elif request.POST.get('check'):
            for item in Card.objects.all():
                if request.POST.get(str(item.id)) == 'clicked':
                    setid = UserSet.objects.get(name=item.userset).id
                    usrset = UserSet.objects.get(id=setid)
                    if not item.collected:
                        usrset.collected += 1
                        usrset.missing -= 1
                        item.collected = True
                    usrset.save()
                    item.save()
        else:
            for item in Card.objects.all():
                if request.POST.get(str(item.id)) == 'clicked':
                    setid = UserSet.objects.get(name=item.userset).id
                    usrset = UserSet.objects.get(id=setid)
                    if item.collected:
                        usrset.collected -= 1
                        usrset.missing += 1
                        item.collected = False
                    usrset.save()
                    item.save()
    setid = UserSet.objects.get(name=setname).id
    return render(request, os.path.join('main', 'cardlist.html'), {'cards': [setname, list(Card.objects.filter(userset=setid))]})


def createset(request):
    if request.method == 'POST':
        form = CreateSet(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            try:
                item = UserSet(name=name)
                item.save()
                return HttpResponseRedirect('/')
            except:
                return render(request, os.path.join('main', 'addset.html'), {'data': [{'error': True}, {'form': form}]})
        else:
            form = CreateSet()
            return render(request, os.path.join('main', 'addset.html'), {'data': [{'error': False}, {'form': form}]})
    else:
        form = CreateSet()
        return render(request, os.path.join('main', 'addset.html'), {'data': [{'error': False}, {'form': form}]})


def search(request):
    if request.method == 'POST':
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?"
        if request.POST.get('searchbutton') == 'pressed' and len(request.POST.get('searchtext')) > 0:
            output = requests.get(url + 'fname=' + request.POST.get('searchtext'))
            details = output.json()
            if output.status_code == 200:
                details = details['data']
                return render(request, os.path.join('main', 'search.html'), {'data': [{'ok': True}, details, {'type': request.POST.get('filter')}, {'usersetlist': list(UserSet.objects.all().values())}, {'searchkey': request.POST.get('searchtext')}, {'addbutton': False}]})
            else:
                return render(request, os.path.join('main', 'search.html'), {'data': [{'ok': False}, details, {}, {}, {'searchkey': request.POST.get('searchtext')}, {'addbutton': False}]})
        elif request.POST.get('addcard'):
            searchkey = request.POST.get('addcard')
            url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?fname=" + parse.quote(searchkey)
            output = requests.get(url)
            cards = output.json()
            if output.status_code == 200:
                cards = cards['data']
                usersetname = request.POST.get('setlist')
                for card in cards:
                    if card.get('card_sets'):
                        for set in card.get('card_sets'):
                            if request.POST.get(str(set['set_code'])) == 'clicked':
                                if card.get('type') != 'Spell Card' and card.get('type') != 'Trap Card' and card.get('type') != 'Link Monster' and card.get('type') != 'Skill Card':
                                    newcard = Card(
                                    userset = UserSet.objects.get(name=usersetname),
                                    collected=False,
                                    cardid=card['id'],
                                    name=card['name'],
                                    type=card['type'],
                                    desc=card['desc'],
                                    attack=card['atk'],
                                    defence=card['def'],
                                    level=card['level'],
                                    attribute=card['attribute'],
                                    cardsetname=set['set_name'],
                                    cardsetcode=set['set_code'],
                                    cardsetrarity=set['set_rarity'],
                                    cardsetraritycode=set['set_rarity_code'],
                                    image_url=card['card_images'][0]['image_url'],
                                    image_url_small=card['card_images'][0]['image_url_small']
                                    )
                                elif card.get('type') == 'Link Monster':
                                    newcard = Card(
                                    userset = UserSet.objects.get(name=usersetname),
                                    collected=False,
                                    cardid=card['id'],
                                    name=card['name'],
                                    type=card['type'],
                                    desc=card['desc'],
                                    attack=card['atk'],
                                    attribute=card['attribute'],
                                    cardsetname=set['set_name'],
                                    cardsetcode=set['set_code'],
                                    cardsetrarity=set['set_rarity'],
                                    cardsetraritycode=set['set_rarity_code'],
                                    image_url=card['card_images'][0]['image_url'],
                                    image_url_small=card['card_images'][0]['image_url_small']
                                    )
                                else:
                                    newcard = Card(
                                    userset = UserSet.objects.get(name=usersetname),
                                    collected=False,
                                    cardid=card['id'],
                                    name=card['name'],
                                    type=card['type'],
                                    desc=card['desc'],
                                    cardsetname=set['set_name'],
                                    cardsetcode=set['set_code'],
                                    cardsetrarity=set['set_rarity'],
                                    cardsetraritycode=set['set_rarity_code'],
                                    image_url=card['card_images'][0]['image_url'],
                                    image_url_small=card['card_images'][0]['image_url_small']
                                    )

                                usrset = UserSet.objects.get(name=usersetname)
                                for _ in range(int(request.POST.get('quantity-' + set['set_code']))):
                                    newcard.copy().save()
                                    usrset.missing += 1

                                usrset.save()

                return render(request, os.path.join('main', 'search.html'), {'data': [{'ok': True}, cards, {'type': request.POST.get('filter')}, {'usersetlist': list(UserSet.objects.all().values())}, {'searchkey': searchkey}, {'addbutton': True}]})
            else:
                return render(request, os.path.join('main', 'search.html'), {'data': [{'ok': False}, details, {}, {}, {'searchkey': request.POST.get('searchtext')}, {'addbutton': False}]})
        else:
            return render(request, os.path.join('main', 'search.html'), {'data': [{'ok': False}, {}, {}, {}, {}, {'addbutton': False}]})
    else:
        return render(request, os.path.join('main', 'search.html'), {'data': [{'ok': True}, {}, {}, {}, {}, {'addbutton': False}]})


def explore(request):
    url = "https://db.ygoprodeck.com/api/v7/cardsets.php"
    errorflag = False
    cardsets = None

    try:
        output = requests.get(url)
        if output.status_code == 200:
            cardsets = output.json()
            for item in cardsets:
                if item.get('set_name'):
                    item['set_name_url'] = parse.quote(item.get('set_name'))
        else:
            errorflag = True
    except:
        errorflag = True

    return render(request, os.path.join('main', 'explore.html'), {'data': [cardsets, errorflag]})


def setdetail(request, selectedset):
    if request.method == 'GET':
        requesttype = 'get'
        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset=" + parse.quote(selectedset)
        output = requests.get(url)
        errorflag = False
        cards = None

        if output.status_code == 200:
            cards = output.json()['data']
        else:
            errorflag = True
    else:
        requesttype = 'post'
        if request.POST.get('addcard'):
            usersetname = request.POST.get('setlist')
            url = "https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset=" + parse.quote(selectedset)
            output = requests.get(url)
            errorflag = False
            cards = None

            if output.status_code == 200:
                cards = output.json()['data']

                for card in cards:
                    if card.get('card_sets'):
                        for set in card.get('card_sets'):
                            if request.POST.get(str(set.get('set_code'))) == 'clicked':
                                if card.get('type') != 'Spell Card' and card.get('type') != 'Trap Card' and card.get('type') != 'Link Monster' and card.get('type') != 'Skill Card':
                                    newcard = Card(
                                    userset = UserSet.objects.get(name=usersetname),
                                    collected=False,
                                    cardid=card['id'],
                                    name=card['name'],
                                    type=card['type'],
                                    desc=card['desc'],
                                    attack=card['atk'],
                                    defence=card['def'],
                                    level=card['level'],
                                    attribute=card['attribute'],
                                    cardsetname=set['set_name'],
                                    cardsetcode=set['set_code'],
                                    cardsetrarity=set['set_rarity'],
                                    cardsetraritycode=set['set_rarity_code'],
                                    image_url=card['card_images'][0]['image_url'],
                                    image_url_small=card['card_images'][0]['image_url_small']
                                    )
                                elif card.get('type') == 'Link Monster':
                                    newcard = Card(
                                    userset = UserSet.objects.get(name=usersetname),
                                    collected=False,
                                    cardid=card['id'],
                                    name=card['name'],
                                    type=card['type'],
                                    desc=card['desc'],
                                    attack=card['atk'],
                                    attribute=card['attribute'],
                                    cardsetname=set['set_name'],
                                    cardsetcode=set['set_code'],
                                    cardsetrarity=set['set_rarity'],
                                    cardsetraritycode=set['set_rarity_code'],
                                    image_url=card['card_images'][0]['image_url'],
                                    image_url_small=card['card_images'][0]['image_url_small']
                                    )
                                else:
                                    newcard = Card(
                                    userset = UserSet.objects.get(name=usersetname),
                                    collected=False,
                                    cardid=card['id'],
                                    name=card['name'],
                                    type=card['type'],
                                    desc=card['desc'],
                                    cardsetname=set['set_name'],
                                    cardsetcode=set['set_code'],
                                    cardsetrarity=set['set_rarity'],
                                    cardsetraritycode=set['set_rarity_code'],
                                    image_url=card['card_images'][0]['image_url'],
                                    image_url_small=card['card_images'][0]['image_url_small']
                                    )

                                usrset = UserSet.objects.get(name=usersetname)
                                for _ in range(int(request.POST.get('quantity-' + set['set_code']))):
                                    newcard.copy().save()
                                    usrset.missing += 1

                                usrset.save()
            else:
                errorflag = True

    return render(request, os.path.join('main', 'setdetail.html'), {'data': [cards, errorflag, list(UserSet.objects.all().values()), selectedset, requesttype]})
