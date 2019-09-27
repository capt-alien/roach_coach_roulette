from django.shortcuts import render, HttpResponse, redirect
import requests
from django.contrib import messages
from . models import *
import bcrypt
from yelpapi import YelpAPI
import random
from code import *
api_key = "cFXNVM3kT5nEUDOmpyDpJi6JD6-CZQFt0ZDWyS8M79PU7l7ldGv9ePpZ28FHrMnMKIpR7rb0GeqWgacKqdE81mJdUBJ9ilFXTpmax3WB6m2QYlrYAQYI2craOeqMXXYx"



def index(request):
    return render(request, 'index.html')

def optionsDisplay(request):
    return render (request, 'options.html')

def roulette(request, choice_id):


    #These will come from the options page
    asian=['korean','chinese','thai','vietnamese', 'japanese']
    american=['tradamerican','newamerican']
    mediterranean=['italian', 'french','greek']

    if choice_id == '1':
        request.session['choice_id'] = '1'

        if 'category_from_options' not in request.session:
            request.session['category_from_options'] = request.POST['category']
            print(request.session['category_from_options'])
        if 'radius' not in request.session:
            radius = int(request.POST['distance'])
            radius *= 1609
            print(radius)
            request.session['radius'] = radius
            print(request.session['radius'])
        if 'price_max' not in request.session:
            request.session['price_max'] = int(request.POST['price'])
        
        #Get the list of all price levels up to the max price set by the user
        price_list = []
        for i in range(0, request.session['price_max'],1):
            price_list.append(i+1)
        
        if request.session['category_from_options'].lower() == 'asian':
            request.session['category1'] = random.choice(asian)
            request.session['category2'] = random.choice(asian)
        if request.session['category_from_options'].lower() == 'american':
            request.session['category1'] = random.choice(american)
            request.session['category2'] = random.choice(american)
        if request.session['category_from_options'].lower() == 'mediterranean':
            request.session['category1'] = random.choice(mediterranean)
            request.session['category2'] = random.choice(mediterranean)
        if request.session['category_from_options'].lower() == 'latin american':
            latin_american=['mexican','latin']
            request.session['category1'] = random.choice(latin_american)
            request.session['category2'] = random.choice(latin_american)
    
    if choice_id == '2':
        request.session['choice_id'] = '2'
        options = ['asian','american','mediterranean','latin_american']
        request.session['category1'] = random.choice(options)
        request.session['category2'] = random.choice(options)
        request.session['radius'] = random.randint(2000,24000)
        request.session['price_max'] = random.randint(1,3)

        print(request.session['radius'])

        price_list = []
        for i in range(0, request.session['price_max'],1):
            price_list.append(i+1)


    yelp_api = YelpAPI(api_key)
    search_results1 = yelp_api.search_query(categories=request.session['category1'], 
                                                location='95112',
                                                radius=request.session['radius'], 
                                                price=price_list,
                                                limit=50)
    search_results2 = yelp_api.search_query(categories=request.session['category2'], 
                                                location='95112', 
                                                radius=request.session['radius'], 
                                                price=price_list,
                                                limit=50)

    if len(search_results2['businesses']) < len(search_results1['businesses']):
        results_count = len(search_results2['businesses'])-1
    else:
        results_count = len(search_results1['businesses'])-1

    print(len(search_results2['businesses']))
    random_choice_from_list = random.randint(0,results_count)
    random_choice_from_list2 = random.randint(0,results_count)

    context={
        "results": search_results1,
        "name_1": search_results1['businesses'][random_choice_from_list]['name'],
        "image_1": search_results1['businesses'][random_choice_from_list]['image_url'],
        "desc_1": search_results1['businesses'][random_choice_from_list]['categories'][0]['title'],
        "address_1": search_results1['businesses'][random_choice_from_list]['location']['display_address'],
        "phone_1": search_results1['businesses'][random_choice_from_list]['display_phone'],
        "name_2": search_results2['businesses'][random_choice_from_list2]['name'],
        "image_2": search_results2['businesses'][random_choice_from_list2]['image_url'],
        "desc_2": search_results2['businesses'][random_choice_from_list2]['categories'][0]['title'],
        "address_2": search_results2['businesses'][random_choice_from_list2]['location']['display_address'],
        "phone_2": search_results2['businesses'][random_choice_from_list2]['display_phone']
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
        'phone': phone,
        'result_choice': result_choice
    }
    return render (request, 'view.html', context)

def save(request, choice_id):
    user = User.objects.get(id=request.session['user_id'])

    if choice_id == '1':
        restaurant = Restaurant.objects.create(image=request.session['result_1_image'], name=request.session['result_1_name'],
        desc=request.session['result_1_desc'], location=request.session['location_1'])
        user.saved.add(restaurant)

    if choice_id == '2':
        restaurant = Restaurant.objects.create(image=request.session['result_2_image'], name=request.session['result_2_name'],
        desc=request.session['result_2_desc'], location=request.session['location_2'])
        user.saved.add(restaurant)

    return redirect('/dashboard')

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
        confirm_PW = request.POST['confirm_PW']
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User.objects.create(first_name = request.POST["first_name"],
                                        last_name = request.POST["last_name"],
                                        email = request.POST["email"],
                                        username=request.POST['email'],
                                        password=pw_hash.decode('utf-8'))
        request.session['user_id'] = new_user.id

        if request.session['choice_id']:
            return redirect('save/'+request.session['choice_id'])

        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/loginReg')

    user = User.objects.filter(email=request.POST['email'])

    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), logged_user.password.encode('utf-8')):
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard')
        else:
            messages.error(request, "Invalid password. Please try again.")
            return redirect("/loginReg")
    else:
        messages.error(request, "Email not found. Please try again, or Register for an account.")
        return redirect("/loginReg")

    return redirect("/loginReg")

def dashboard(request):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user_first_name': user.first_name.upper(),
            'user_favorites': user.favorites.all(),
            'user_saved': user.saved.all()
        }

        return render (request, 'dashboard.html', context)
    else:
        return redirect('/loginReg')


def edit(request,fav_id):
    restaurant = Restaurant.objects.get(id=fav_id)
    context = {
        'restaurant': restaurant,
        'notes': restaurant.restaurant_name.all()
    }

    print(context['notes'])
    return render(request, 'editNote.html', context)

def edit_note(request, fav_id):
    print(request.POST['text'])
    restaurant = Restaurant.objects.get(id=fav_id)
    user = User.objects.get(id=request.session['user_id'])
    new_note = Note.objects.create(content=request.POST['text'], user=user, restaurant=restaurant)
    return redirect('/dashboard')

def refresh(request):
    return redirect('/roulette/'+request.session['choice_id'])

def move_to_fav(request, save_id):
    user = User.objects.get(id=request.session['user_id'])
    restaurant = Restaurant.objects.get(id=save_id)

    user.saved.remove(restaurant)
    user.favorites.add(restaurant)

    return redirect('/dashboard')

def remove_from_saved(request, save_id):
    user = User.objects.get(id=request.session['user_id'])
    restaurant = Restaurant.objects.get(id=save_id)

    user.saved.remove(restaurant)  

    return redirect('/dashboard')  

def reset(request):
    request.session.clear()
    return redirect('/')