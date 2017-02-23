from django.shortcuts import render,redirect
from models import users, travels, addeduser
import re
import inspect
from django.db.models import Count
email_re = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
import bcrypt
import datetime
travels_all = travels.objects.all()
def containnumber(string):
    return bool(re.search(r'\d', string))



def index(request):
    return render(request, 'index.html')

def add(request):
    firstname = request.POST.get('first')
    lastname = request.POST.get('last')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    passwordcon = request.POST.get('passcon')
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    error = False
    context = {
        }
    if len(firstname)<=2:
        error= True
        context['enterfirst'] = 'Enter a valid name'
    if containnumber(firstname)==True:
        error = True
        context['enterfirst'] = 'Enter a valid name'
    if len(lastname)<=2:
        error = True
        context['enterlast'] = 'Enter a valid name'
    if containnumber(lastname):
        error = True
        context['enterlast'] = 'Enter a valid name'
    if not email_re.match(email):
        error = True
        context['emailcon'] = 'Must be a valid email'
    if len(password)<9:
        error = True
        context['password'] = 'Password must be longer than 8 digits'
    if len(passwordcon)<9:
        error = True
        context['password'] = 'Password must be longer than 8 digits'
    if password != passwordcon:
        context['password'] = 'Passwords must match'
        error = True
    if not error:
        print pw_hash
        context['sucess'] =  'You sucessfully registerd'
        users.objects.create(first_name = request.POST.get('first'), last_name = request.POST['last'], email = request.POST['email'], password= pw_hash)
        user = users.objects.filter(first_name = request.POST.get('first'), last_name = request.POST['last'], email = request.POST['email'])
        hashed = user[0].password
        if user is not None:
            request.session['first_name'] = user[0].first_name
            request.session['last_name'] = user[0].last_name
            request.session['email'] = user[0].email
            request.session['id'] = user[0].id
            return redirect('/travels')
    else:
        return render(request, 'index.html',context)


def login(request):
    email_login = request.POST['email_login']
    if users.objects.filter(email = request.POST['email_login']).exists() == False:
        context = {
            'fail': 'Enter a valid email'
        }
        return render(request, 'index.html',context)
    else:
        password_login = request.POST['password_login']
        user = users.objects.filter(email = email_login)
        hashed = user[0].password
        if user is not None:
            if bcrypt.hashpw(password_login.encode(), hashed.encode()) == hashed:
                print user[0].first_name
                request.session['first_name'] = user[0].first_name
                request.session['last_name'] = user[0].last_name
                request.session['email'] = user[0].email
                request.session['id'] = user[0].id

                return redirect('/travels')
            else:
                context = {
                'fail': 'Email and password did not match'
                }
                return render(request, 'index.html', context)

def locations(request):
    userinstance = users.objects.get(id = request.session['id'])
    travellocations = travels.objects.all()
    plans = travels.objects.all().filter(user = userinstance)
    joinedplans = addeduser.objects.all().filter(adduser = userinstance)
    array = []
    for i in range(0,len(joinedplans)):
        if (joinedplans[i].adduser.id == request.session['id']):
            array.append(joinedplans[i].addtravel.id)
    print array[:]
    for x in range(0, len(array)):
        travellocations= travellocations.exclude(id = array[x])

    context = {
        'plans': plans,
        'joinedplans': joinedplans,
        'travels' : travellocations
    }
    return render(request, 'travels.html', context)


def adddestination(request):
    return render(request, 'adddestination.html')

def newdestination(request):
    userinstance = users.objects.get(id = request.session['id'])
    destination = request.POST.get('destination')
    description = request.POST.get('description')
    start = request.POST.get('start')
    finish = request.POST.get('finish')
    error = False
    CurrentDate = datetime.date
    print CurrentDate
    if (start < CurrentDate):
        error = True
    if len(destination)<2:
        error = True
    if len(description)< 10:
        error = True
    if start == None:
        error = True
    if finish == None:
        error = True
    if finish < start:
        error = True
        print 'fail'
    if not error:
        travels.objects.create(user = userinstance, destination = destination, description = description, startdate = start, enddate = finish)
        return redirect('/travels')
    else:
        return render(request, 'adddestination.html')

def viewdestination(request, id):
    destination = travels.objects.all().filter(id = id)
    context = {
        'destination' : destination,
        'other': addeduser.objects.all().filter(addtravel = destination)
    }
    return render(request, 'destination.html', context)

def join(request, id):
    userinstance = users.objects.get(id = request.session['id'])
    travelinstance = travels.objects.get(id = id)
    addeduser.objects.create(adduser = userinstance, addtravel = travelinstance )
    return redirect('/travels')
