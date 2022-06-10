
from email import message
from django.shortcuts import  render
from django.http import  HttpResponse, HttpResponseNotFound, HttpResponseNotModified, HttpResponseServerError, JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
import re
from markdown2 import Markdown
from . import util
import random




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "headers": "All Pages"
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return HttpResponseNotFound
    else :
        markdowner = Markdown()
        entryhtml = markdowner.convert(entry)       
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entryhtml
        } )

def search(request):
    try:
        title = request.GET['q']
    except:
        return HttpResponseServerError()
    entry = util.get_entry(title)
    if entry == None:
        results = []
        entries = util.list_entries()
        for e in entries:
            if re.search(title.lower(),e.lower()):
                results.append(e)
        return render(request,"encyclopedia/index.html", {
            "entries" : results,
            "headers": "Similar results"
        })           
    else:
        return HttpResponseRedirect(reverse('title',args=(title,)))   

def to_create_page(request):
    return render(request, "encyclopedia/newPage.html")
    
def create_page(request):
    try:
        title = request.POST["t"]
        content = request.POST["c"]
    except:
        return HttpResponseServerError()
    existing = util.list_entries()
    for e in existing:
        if title.lower() == e.lower():
            status = 400
            msg = "The page you want to add already exist"
            return JsonResponse({"error": msg}, status = status)
    try:
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('index'))
    except:
        return HttpResponseServerError()

def to_edit_page(request,title):
    current_entry = util.get_entry(title)
    if current_entry == None:
        return HttpResponseNotFound()
    else : 
        entries_names = util.list_entries()
        for e  in entries_names:
            if title.lower() == e.lower():
                title = e
                break
        return render(request, "encyclopedia/editPage.html",{
            "title": title,
            "content": current_entry
        })

def edit_page(request):
    title = request.POST["t"]
    content = request.POST["c"]
    try:
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse('index'))
    except:
        return HttpResponseServerError()

def random_page(request):
    entries = util.list_entries()
    randomentry = random.randint(0,len(entries) - 1)
    print(randomentry)
    return  HttpResponseRedirect(reverse('title',args=(entries[randomentry],)))

