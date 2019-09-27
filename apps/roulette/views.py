from django.shortcuts import render, HttpResponse, redirect
import requests
from django.contrib import messages
from . models import *
import bcrypt
from yelpapi import YelpAPI
import random
from code import *


def index(request):
    return render(request, 'index.html')

def optionsDisplay(request):
    return render (request, 'options.html')

def roulett(request):
    #These will come from the options page
    #category_from_options = request.session['category']
    #location = request.session['location']
    #price_max = request.session['price_max']
    # Get the list of all price levels up to the max price set by the user
    #price_list = []
    #for i in range(0, price_max, 1):
    #   price_list[i] = i+1
    #radius = request.session['radius']
    # Multiply radius to convert miles to meters (yelp API uses meters)
    #radius *= 1609
    asian=['korean','chinese','thai','vietnamese', 'japanese']
    american=['tradamerican','newamerican']
    mediterranean=['italian', 'french','greek']
    latin_american=['mexican','latin']

    category1 = random.choice(asian)
    category2 = random.choice(mediterranean)

    yelp_api = YelpAPI(api_key)
    search_results1 = yelp_api.search_query(categories=category1, location='95112', radius=8045, price=2, limit=50)
    search_results2 = yelp_api.search_query(categories=category2, location='95112', radius=8045, price=2, limit=50)

    if len(search_results2['businesses']) < len(search_results1['businesses']):
        results_count = len(search_results2['businesses'])-1
    else:
        results_count = len(search_results1['businesses'])-1

    print(len(search_results2['businesses']))
    random_choice_from_list = random.randint(0,results_count)

    context={
        "results": search_results1,
        "name_1": search_results1['businesses'][random_choice_from_list]['name'],
        "image_1": search_results1['businesses'][random_choice_from_list]['image_url'],
        "desc_1": search_results1['businesses'][random_choice_from_list]['categories'][0]['title'],
        "address_1": search_results1['businesses'][random_choice_from_list]['location']['display_address'],
        "phone_1": search_results1['businesses'][random_choice_from_list]['display_phone'],
        "name_2": search_results2['businesses'][random_choice_from_list]['name'],
        "image_2": search_results2['businesses'][random_choice_from_list]['image_url'],
        "desc_2": search_results2['businesses'][random_choice_from_list]['categories'][0]['title'],
        "address_2": search_results2['businesses'][random_choice_from_list]['location']['display_address'],
        "phone_2": search_results2['businesses'][random_choice_from_list]['display_phone']
    }

    request.session['result_1_name'] = context['name_1']
    request.session['result_1_image'] = context['image_1']
    request.session['result_1_desc'] = context['desc_1']
    request.session['location_1'] = context['address_1']
    request.session['phone_1'] = context['phone_1']

    request.session['result_2_name'] = context['name_2']
    request.session['result_2_image'] = context['image_2']
    request.session['result_2_desc'] = context['desc_2']
    request.session['location_2'] = context['address_2']
    request.session['phone_2'] = context['phone_2']

    return redirect ('/resultsDisplay')

def resultsDisplay(request):

    return render (request, 'results.html')

def viewInfo(request, result_id):
    result_choice = result_id

    if result_choice == '1':
        name = request.session['result_1_name']
        img = request.session['result_1_image']
        desc = request.session['result_1_desc']
        loc = request.session['location_1']
        phone = request.session['phone_1']
    else:
        name = request.session['result_2_name']
        img = request.session['result_2_image']
        desc = request.session['result_2_desc']
        loc = request.session['location_2']
        phone = request.session['phone_2']

    context = {
        'name': name,
        'image': img,
        'desc': desc,
        'location': loc,
        'phone': phone
    }
    return render (request, 'view.html', context)

def goBack(request):
    return redirect ('/')

def loginReg(request):
    return render(request, 'loginReg.html')

def newUser(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/loginReg')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name = request.POST["first_name"],
                                        last_name = request.POST["last_name"],
                                        email = request.POST["email"],
                                        username=request.POST['email'],
                                        password=pw_hash)
        return redirect(f'/dashboard/{new_user.id}')
    return redirect ('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/loginReg')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard')
            # return redirect(f"/dashboard/{request.session['user_id']}")

def dashboard(request):
    if 'user_id' in request.session:
        return render (request, 'dashboard.html')
    else:
        return redirect('/loginReg')


def editFaves(request):
    return redirect ('/dashboard')
