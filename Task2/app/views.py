from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib import messages
from .models import UserModel,ArticleModel
from .forms import ArticleForm
from django.db.models import Q


def LoginPage(request):
    return render(request,"login.html")


def RegisterPage(request):
    uf = RegistrationForm()
    if request.method == "POST":
        urf = RegistrationForm(request.POST)
        if urf.is_valid():
            uname = request.POST.get("username")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            if password == confirm_password:
                if UserModel.objects.filter(username=uname).exists():
                    messages.success(request, "Username already used")
                    return render(request, "register.html", {"form": urf})
                else:
                    UserModel(username=uname,password=password).save()
                    messages.success(request, "Successfully Registered")
                    return render(request, "register.html", {"form": uf})
            else:
                messages.success(request, "Password Not Matching")
                return render(request, "register.html", {"form": urf})
        else:
            return render(request, "register.html", {"form": urf, "msg": urf.errors})
    else:
        return render(request, "register.html", {"form": uf})


def login_check(request):
    uname = request.POST.get("username")
    upass = request.POST.get("password")
    try:
        sam = UserModel.objects.get(username=uname, password=upass)
        request.session['username'] = sam.username
        return redirect('welcome')
    except:
        messages.success(request, "Invalid User")
        return render(request, 'login.html')

def welcome(request):
    res = request.session.get("username", None)
    if res:
        data = ArticleModel.objects.filter(username=res)
        return render(request, 'welcome.html',{"data":data})
    else:
        return redirect('login')



def logout(request):
    try:
        del request.session['username']
        return redirect('login')
    except KeyError:
        return redirect('login')


def create_article(request):
    af = ArticleForm()
    if request.POST:
        afp = ArticleForm(request.POST, request.FILES)
        if afp.is_valid():
            username =  request.session.get("username", None)
            topic_name = request.POST.get("topic_name")
            image = request.FILES['image']
            description = request.POST.get("description")
            article_type = request.POST.get("article_type")
            ArticleModel(username=username,topic_name=topic_name,description=description,article_type=article_type,image=image).save()
            messages.success(request, "Successfully Registered")
            return render(request, "article_create.html", {"form":af})
        else:
            messages.success(request, afp.errors)
            return render(request,"article_create.html",{"form":afp})
    else:
        return render(request, "article_create.html", {"form": af})


def others_article(request):
    data = ArticleModel.objects.filter(article_type='Public')
    return render(request,"others_article",{"data":data})


def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        if search:
            match = ArticleModel.objects.filter(Q(topic_name__icontains= search))
            if match:
                data = []
                for x in match:
                    if x.article_type == 'Public':
                        data.append(x)
                    else:
                        continue
                print(data)
                return render(request,"others_article",{"data":data})
            else:
                messages.success(request,"no result found")
                return render(request, "others_article", {"data": match})
    return redirect('others_article')