from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from .models import Headline

# Create your views here.


def scrape(request):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://www.myjoyonline.com/"
    content = session.get(url).content
    soup = BSoup(content, "html.parser")
    News = soup.find_all('div', {"class":"cw4lnv-11 dFCKPx"})
    for article in News:
        main = article.find_all('a',href=True)
        links = article.find('a', {"class":"sc-1out364-0 hMndXN js_link"})
        link=links['href']
        images=main[0].find('img',src=True)
        image_src=images['srcset'].split(" ")[-4]
        titles = article.find('h2', {"class":"sc-759qgu-0 cYlVdn cw4lnv-6 eXwNRE"})
        title = titles.text
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_src
        new_headline.save()
    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }
    return render(request, "news/home.html", context)