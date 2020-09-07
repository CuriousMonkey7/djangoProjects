from django.shortcuts import render
from . import util
import markdown2
import random
from difflib import get_close_matches
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)

    if entry != None:
        title = entry[entry.find("#")+1:entry.find("\n")]
        htmlOfMd = markdown2.markdown(entry)
    else:
        htmlOfMd = "Oopsie! Requested page was not found."

    return render(request, "encyclopedia/entry.html", {"html": htmlOfMd, "title": title})


def search(request):
    title = request.POST['title']
    entries = util.get_entry(title)
    if entries != None:

        return entry(request, title)
    else:
        listOfSimilarKeyword = closeMatches(util.list_entries(), title)
        print(listOfSimilarKeyword)
        return render(request, "encyclopedia/searchResult.html", {
            "entries": listOfSimilarKeyword
        })


def createNewPage(request):
    return render(request, "encyclopedia/newPage.html")


def create(request):

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) == None:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entries', args=[title]))
        else:
            return render(request, "encyclopedia/newPage.html", {"message": "Title Already Exists. Change Title and try again", "content": content})
            # miscellaneous functions(Helpers)


def editPage(request, title):
    print(title)
    title = title.strip()
    print(title + "ch")
    content = util.get_entry(title)
    print(content)

    return render(request, "encyclopedia/editPage.html", {"content": content, 'title': title})


def edit(request, title):
    if request.method == "POST":
        title = request.POST['title']
        print(title)
        content = request.POST['content']
        print(content)
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse('entries', args=[title]))


def randomPage(request):

    randomEntry = random.choice(util.list_entries())
    return entry(request, randomEntry)


def closeMatches(patterns, word):

    listOfSimilarKeyword = []
    for i in patterns:
        if word.lower() in i.lower():
            listOfSimilarKeyword.append(i)
    return listOfSimilarKeyword
