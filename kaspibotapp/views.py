from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm
from bs4 import BeautifulSoup 
import requests
import re
import json

# Create your views here.
def home(request):
    return render(request, 'index.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)    
                    return redirect('dash')
        else:
            form = LoginForm()
        return render(request, 'signin.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                print(form)
                return redirect('signin')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('signin')

def dashboard(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            # url_to_scrape = "https://www.google.com/search?q={}&sca_esv=571272750&rlz=1C1CHBD_enIN925IN925&tbm=shop&sxsrf=AM9HkKk0G6R_h-7c9KG-IpuVpgBCJ6IENg:1696589103326&source=lnms&sa=X&ved=2ahUKEwijltX2nuGBAxXnzzgGHTDJDtoQ_AUoAXoECAUQAw&biw=1536&bih=786&dpr=1.25".format(inp)
            url_to_scrape = "https://www.google.com/search?q=red+lamp&sca_esv=571272750&rlz=1C1CHBD_enIN925IN925&tbm=shop&sxsrf=AM9HkKk0G6R_h-7c9KG-IpuVpgBCJ6IENg:1696589103326&source=lnms&sa=X&ved=2ahUKEwijltX2nuGBAxXnzzgGHTDJDtoQ_AUoAXoECAUQAw&biw=1536&bih=786&dpr=1.25"
            response = requests.get(url_to_scrape)
            html_document = response.text
            soup = BeautifulSoup(html_document, 'html.parser')

            print(html_document)

            for span in soup.find_all('span', text = re.compile('₹')):
                spantext = span.text
                if '-' in spantext or 'filter' in spantext or 'Under' in spantext or 'Over' in spantext or 'Up' in spantext or 'delivery' in spantext:
                    print("")
                else:
                    parenttag = span.parent.parent.prettify()

                    for link in BeautifulSoup(parenttag).find('a'):
                        pname = link.text.replace("\n   ", "")

                    plink = BeautifulSoup(parenttag).find('a')['href'].replace("/url?q=", "")
                    pprice = spantext
                    pfrom = span.parent.text.split("from ")[-1]

                    print("\nProduct: {}\nLink: {}\nPrice: {}\nFrom: {}\n".format(pname, plink, pprice, pfrom))
        else:
            context = {}
            return (request, 'dashboard.html', context)
    else:
        return redirect('home')
    return render(request, 'dashboard.html')

def testing(request):
    url_to_scrape = "https://www.google.com/search?q=red+lamp&sca_esv=571272750&rlz=1C1CHBD_enIN925IN925&tbm=shop&sxsrf=AM9HkKk0G6R_h-7c9KG-IpuVpgBCJ6IENg:1696589103326&source=lnms&sa=X&ved=2ahUKEwijltX2nuGBAxXnzzgGHTDJDtoQ_AUoAXoECAUQAw&biw=1536&bih=786&dpr=1.25"
    response = requests.get(url_to_scrape)
    html_document = response.text
    soup = BeautifulSoup(html_document, 'html.parser')

    finallist = []

    for span in soup.find_all('span', text = re.compile('₹')):
        spantext = span.text
        if '–' in spantext or 'filter' in spantext or 'Under' in spantext or 'Over' in spantext or 'Up' in spantext or 'delivery' in spantext:
            print("")
        else:
            parenttag = span.parent.parent.prettify()

            for link in BeautifulSoup(parenttag, 'html.parser').find('a'):
                pname = link.text.replace("\n  ", "")

            plink = BeautifulSoup(parenttag, 'html.parser').find('a')['href'].replace("/url?q=", "")
            pprice = spantext
            pfrom = span.parent.text.split("from ")[-1]

            newlist = {
                'name': pname,
                'link': plink,
                'price': pprice,
                'from': pfrom
            }

            finallist.append(newlist)
            print(finallist)

    return render(request, 'dashboard.html', {'finallist': finallist})

def dash(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            searchterm = request.POST.get('searchterm')
            searchterm = searchterm.replace(" ", "+")
            url_to_scrape = "https://www.google.com/search?q={}&sca_esv=571272750&rlz=1C1CHBD_enIN925IN925&tbm=shop&sxsrf=AM9HkKk0G6R_h-7c9KG-IpuVpgBCJ6IENg:1696589103326&source=lnms&sa=X&ved=2ahUKEwijltX2nuGBAxXnzzgGHTDJDtoQ_AUoAXoECAUQAw&biw=1536&bih=786&dpr=1.25".format(searchterm)
            response = requests.get(url_to_scrape)
            html_document = response.text
            soup = BeautifulSoup(html_document, 'html.parser')

            finallist = []

            for span in soup.find_all('span', text = re.compile('₹')):
                spantext = span.text
                if '–' in spantext or 'filter' in spantext or 'Under' in spantext or 'Over' in spantext or 'Up' in spantext or 'delivery' in spantext:
                    print("")
                else:
                    parenttag = span.parent.parent.prettify()

                    for link in BeautifulSoup(parenttag, 'html.parser').find('a'):
                        pname = link.text.replace("\n  ", "")

                    plink = BeautifulSoup(parenttag, 'html.parser').find('a')['href'].replace("/url?q=", "")
                    pprice = spantext
                    pfrom = span.parent.text.split("from ")[-1]

                    newlist = {
                        'name': pname,
                        'link': plink,
                        'price': pprice,
                        'from': pfrom
                    }

                    finallist.append(newlist)

            return render(request, 'dashboard.html', {'finallist': finallist})
        else:
            return render(request, 'dashboard.html')
    else:
        return redirect('signin')