import os
import random
from django.http import Http404
from django.shortcuts import render
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    contents = util.get_entry(entry)
    if contents is None:
        return render(request, "encyclopedia/error.html", {
            "error_type": "404 Not Found",
            "error_message": f"The {entry} page is not avilable."
        })
    else:
        markdowner = Markdown()
        conversion_to_html = markdowner.convert(contents)
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry,
            "entry": conversion_to_html
        })

def search(request):
    if request.method == "GET":
        query = request.GET["q"]

        contents = util.get_entry(query)

        if contents is None:
            entries_md = os.listdir('entries/')
            entries = [entry.split(".md")[0] for entry in entries_md]
            results = []
            for entry in entries:
                if query in entry:
                    results.append(entry)

            return render(request, "encyclopedia/results.html", {
                "entries": results
            })
        else:
            markdowner = Markdown()
            conversion_to_html = markdowner.convert(contents)
            return render(request, "encyclopedia/entry.html", {
                "entry_name": query,
                "entry": conversion_to_html
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    
    elif request.method == "POST":
        print("Method is GET")
        title = request.POST["title"]
        content = request.POST["content"]
        html_content = Markdown().convert(content)

        new_proposed_page = f"{title}.md"
        current_pages = os.listdir('entries/')

        if new_proposed_page not in current_pages:
            with open(f"entries/{title}.md", 'w') as f:
                f.write(content)

            return render(request, "encyclopedia/entry.html", {
                "entry_name": title,
                "entry": html_content
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "error_type": "Page Exists!",
                "error_message": f"The {title} page already exists."
            })
    else:
        print("Method is neither POST nor GET")

def edit_page(request, page_name):
    if request.method == "GET":
        content = util.get_entry(page_name)
        return render(request, "encyclopedia/edit_page.html", {
            "page_name": page_name,
            "content": content
        })
    elif request.method == "POST":
        page_to_edit = f"entries/{page_name}.md"
        os.remove(page_to_edit)
        with open(page_to_edit, 'w') as f:
            f.write(request.POST["new_page_contents"])

        content = Markdown().convert(request.POST["new_page_contents"])
        return render(request, "encyclopedia/entry.html", {
  	    	    "entry_name": page_name,
  		        "entry": content
  	    })
    
def random_page(request):
    if request.method == "GET":
        entries_md = os.listdir('entries')
        entries = [entry.split(".md")[0] for entry in entries_md]
        random_page = random.choice(entries)
        content = util.get_entry(random_page)
        page_name = random_page.split(".md")[0]

        html_content = Markdown().convert(content)
        return render(request, "encyclopedia/entry.html", {
            "entry_name": page_name,
            "entry": html_content
        })

