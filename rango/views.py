from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import loader,Template,Context
from rango.models import Category,Page
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import redirect

def index(request):
    request.session.set_test_cookie()
    context_list = Category.objects.order_by('-likes')[:5]
    context_dict = { 'categories' : context_list}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request,'rango/index.html',context= context_dict)
   

def about(request):
    if request.session.test_cookie_worked():
        print("Test Cookie Worked!")
        request.session.delete_test_cookie()
    return render(request,'rango/about.html',context = None)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug = category_name_slug)
        #pages = Page.objects.filter(category = category)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['pages'] = None
    
    context_dict['query'] = category.name
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            context_dict['query'] = query
            context_dict['result_list'] = result_list
    return render(request,'rango/category.html',context_dict)


def add_category(request):

    form = CategoryForm()

    if request.method == 'POST' :   # POST : user submits data through the form 
        form = CategoryForm(request.POST)

        if form.is_valid():
            cat = form.save(commit=True)
            return index(request)  #direct user back to index page
        
        else:
            print(form.errors)  #print errors in form inputs

    context_dict = {'form' : form}

    return render(request,'rango/add_category.html',context_dict)

def add_page(request,category_name_slug):

    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist :
        category = None

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit = False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request,category_name_slug)  # redirect user to the page list for that category

        else:
            print(form.errors)

    context_dict = {'form' : form , 'category' : category}
    return render(request,'rango/add_page.html',context_dict)


def register(request):
    registered = False # to check whether the user is already registered

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if  'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
    
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered}

    return render(request,'rango/register.html',context_dict)


def user_login(request):

    if request.method == "POST" : 
        username = request.POST.get('username')
        password = request.POST.get('password')  #info already obtained from the login form
        user = authenticate( username = username,password = password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango Account has been disabled")
        else:
            print("Invalid Login Details: {0},{1}".format(username,password))
            return HttpResponse("Invalid Login Details Entered")

    else:
        context_dict = {}
        return render(request,'rango/login.html',context_dict)

@login_required
def restricted(request):
    return HttpResponse("Since you are logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))

def get_server_side_cookie(request,cookie,default_val = None): #helper method
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits',1))

    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 1:
        visits+=1
        request.session['last_visit'] = str(datetime.now())
    
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
     #instead of storing the cookies in the request and on the client's machine, we are storing the cookie in the server side
     # in request.session dictionary 

def track_url(request):
    page_id = None
    url = "/rango/"

    if request.method == "GET":
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(id = page_id)
                page.views+=1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)

def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    return render(request, 'rango/category.html', {'result_list': result_list})


@login_required
def register_profile(request):

    form = UserProfileForm()

    if request.method == "POST":
        form = UserProfileForm(request.POST,request.files)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            form.errors
    
    context_dict = {'form' : form}
    return render(request,'rango/profile_registration.html',context_dict)






