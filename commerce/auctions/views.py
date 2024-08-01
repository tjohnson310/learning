from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "user": request.user
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(f"User: {user.is_authenticated}")

        # Check if authentication successful
        if user is not None:
            login(request, user)
            print("Logging in...")
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_new_listing(request):
    if request.method == "POST":
        category_checked = "category_check" in request.POST
        image_url_checked = "url_check" in request.POST

        if category_checked and request.POST["category_check"] is None:
            return HttpResponse('Category selection is required when checked!')

        if image_url_checked and request.POST["image_url"] == "":
            return HttpResponse('URL is required when checked!')
        
        if not category_checked:
            category = ""
        else:
            category = request.POST["category"].capitalize()

        # print(f"Category checked: {category_checked}")
        # print(f"Category; {category}")

        if not image_url_checked:
            image_url = ""
        else:
            image_url = request.POST["image_url"]

        # print(f"Category checked?: {category_checked}")
        # print(f"Title: {request.POST['title']}")
        # print(f"Image URL Checked?: {image_url_checked}. URL: {type(request.POST['image_url'])}")
        # print(f"Description: {request.POST['new_listing']}")

        listing = Listing(listing_user=request.user, title=request.POST["title"], 
                            description=request.POST["new_listing"], starting_bid=request.POST["starting_bid"],
                            image_url=image_url, category=category, current_bid=request.POST["starting_bid"])
        listing.save()
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })

    return render(request, "auctions/new_listing.html", {
        "user": request.user.username
    })

def delete_listing(request, listing_id):
    if request.method == "POST":
        id = listing_id

        Listing.objects.filter(pk=id).delete()

        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })
    
def nav_to_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_is_valid = isinstance(request.user, User)
    bids = Bid.objects.filter(listing=listing)

    if user_is_valid:
        try:
            watchlist = Watchlist.objects.get(user=request.user)
        except Exception as e:
            print(f"Unexpected Watchlist Error: {e}")
            watchlist = Watchlist(user=request.user)
            watchlist.save()
        
        remove = False
        if watchlist.listings.count() > 0:
            if listing in watchlist.listings.all():
                remove = True
    else:
        remove = False
                
    print(f"Closed: {listing.closed}")

    current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

    if current_bid is None:
        current_bid = listing.starting_bid

    print(f"Winner: {listing.winner}")
    print(f"User: {request.user.username}")

    return render(request, "auctions/listing_page.html", {
        "user": request.user.username,
        "listing": listing,
        "user_is_valid": user_is_valid,
        "remove": remove,
        "closed": listing.closed,
        "winner": listing.winner,
        "bids": bids,
        "current_bid": current_bid
    })

def update_bid(request, listing_id):
    if request.method == 'POST':
        try:
            new_bid = float(request.POST['new_bid'])
            listing = Listing.objects.get(pk=listing_id)
            user_is_valid = isinstance(request.user, User)

            if user_is_valid:
                try:
                    watchlist = Watchlist.objects.get(user=request.user)
                except Exception as e:
                    print(f"Unexpected Watchlist Error: {e}")
                    watchlist = Watchlist(user=request.user)
                    watchlist.save()
                
                remove = False
                if watchlist.listings.count() > 0:
                    if listing in watchlist.listings.all():
                        remove = True
            else:
                remove = False

            current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

            if current_bid is not None:
                if new_bid > current_bid:
                    bid = Bid.objects.filter(listing=listing, bidding_user=request.user).first()
                    bids = Bid.objects.filter(listing=listing)
                    if bid:
                        print("bid exists")
                        bid.new_bid = new_bid
                        bid.save()

                        listing.current_bid = new_bid
                        listing.save()
                    else:
                        print("Creating new bid.")
                        listing_bid = Bid(bidding_user=request.user, 
                                        listing=listing, new_bid=new_bid)
                        listing_bid.save()

                        listing.current_bid = new_bid
                        listing.save()

                    print(f"Winner: {listing.winner}")
                    print(f"User: {request.user.username}")

                    return render(request, 'auctions/listing_page.html', {
                            "user": request.user.username,
                            "listing": listing,
                            "user_is_valid": user_is_valid,
                            "remove": remove,
                            "closed": listing.closed,
                            "winner": listing.winner,
                            "bids": bids,
                            "current_bid": new_bid
                        })
                else:
                    return HttpResponse('Your bid must be greater than the top bid!')
            else:
                listing_bid = Bid(bidding_user=request.user, 
                                  listing=listing, new_bid=new_bid)
                listing_bid.save()

                listing.current_bid = new_bid
                listing.save()
                return render(request, 'auctions/listing_page.html', {
                        "user": request.user.username,
                        "listing": listing,
                        "user_is_valid": user_is_valid,
                        "remove": remove,
                        "closed": listing.closed,
                        "winner": listing.winner,
                        "bids": Bid.objects.filter(listing=listing),
                        "current_bid": new_bid
                    })
        except ValueError:
            return HttpResponse("Please provide a valid bid!")

def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing_id=listing_id)
    user_is_valid = isinstance(request.user, User)
    listing.closed = True

    current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

    for bid in bids:
        if bid.new_bid == current_bid:
            print(f"Auction winner: {bid.bidding_user.username}")
            listing.winner = bid.bidding_user.username
            break
        
    listing.save()

    if current_bid is None:
        current_bid = listing.starting_bid

    print(f"Winner: {listing.winner}")
    print(f"User: {request.user.username}")
    
    return render(request, 'auctions/listing_page.html', {
            "user": request.user.username,
            "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": True,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": bids,
            "current_bid": current_bid
        })

def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listing_id = int(listing_id)
        listing = Listing.objects.get(pk=listing_id)
        user_is_valid = isinstance(request.user, User)
        bids = Bid.objects.filter(listing=listing)

        try:
            watchlist = Watchlist.objects.get(user=request.user)

            if watchlist.listings.count() > 0:
                if listing not in watchlist.listings.all():
                    watchlist.listings.add(listing)
            else:
                watchlist.listings.add(listing)

        except Exception as e:
            watchlist = Watchlist(user=request.user)
            watchlist.listings.add(listing)
            watchlist.save()

        current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

        if current_bid is None:
            current_bid = listing.starting_bid

        print(f"Winner: {listing.winner}")
        print(f"User: {request.user.username}")
        
        return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
            "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": True,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": bids,
            "current_bid": current_bid
        })
    
def remove_from_watchlist(request, listing_id):
    if request.method == "POST":
        listing_id = int(listing_id)
        listing = Listing.objects.get(pk=listing_id)
        user_is_valid = isinstance(request.user, User)
        bids = Bid.objects.filter(listing=listing)

        try:
            watchlist = Watchlist.objects.get(user=request.user)

            if watchlist.listings.count() > 0:
                if listing in watchlist.listings.all():
                    watchlist.listings.remove(listing)
        except Exception as e:
            print(f"Watchlist removal error: {e}")
        
        current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

        if current_bid is None:
            current_bid = listing.starting_bid

        print(f"Winner: {listing.winner}")
        print(f"User: {request.user.username}")
        
        return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
            "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": False,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": bids,
            "current_bid": current_bid
        })
    
def navigate_to_watchlist(request):
    try:
        listings = Watchlist.objects.filter(user=request.user).values('listings')
    except Exception as e:
        print(f'Watchlist retrieval error: {e}')

    print(f"Listings: {listings}")

    titles_ids_of_listings = []
    if listings[0]["listings"] is not None:
        for listing in listings:
            titles_ids_of_listings.append((listing["listings"], Listing.objects.get(pk=listing["listings"]).title))

    print(f"Listings: {titles_ids_of_listings}")
   
    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": titles_ids_of_listings
    })
    
def add_comment(request, listing_id):
    if request.method == "POST":
        user_is_valid = isinstance(request.user, User)
        listing_id = int(listing_id)
        listing = Listing.objects.get(pk=listing_id)

        if user_is_valid:
            try:
                watchlist = Watchlist.objects.get(user=request.user)
            except Exception as e:
                print(f"Unexpected Watchlist Error: {e}")
                watchlist = Watchlist(user=request.user)
                watchlist.save()
            
            remove = False
            if watchlist.listings.count() > 0:
                if listing in watchlist.listings.all():
                    remove = True
        else:
            remove = False

        current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

        if current_bid is None:
            current_bid = listing.starting_bid

        print(f"Comment: {request.POST.get('new_comment')}")
        listing.comments.append({"user": request.user.username, "comment": request.POST.get("new_comment")})
        listing.save()
        bids = Bid.objects.filter(listing=listing)

        print(f"Winner: {listing.winner}")
        print(f"User: {request.user.username}")

        return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
            "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": remove,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": bids,
            "current_bid": current_bid
        })
        
def nav_to_categories(request):
    listings = Listing.objects.all()
    categories = []
    for listing in listings:
        if listing.category not in categories:
            categories.append(listing.category)
    
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def listings_in_category(request, category):
    category_listings = []
    listings = Listing.objects.all()
    for listing in listings:
        if listing.category == category:
            category_listings.append((listing.id, listing.title))
            
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "category_listings": category_listings
    })

def edit_comment(request, comment, listing_id, user):
    return render(request, "auctions/edit_comment.html", {
        "comment": comment,
        "listing_id": listing_id,
        "user": user
    })

def update_comment(request, listing_id, user):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        updated_comment = request.POST.get("updated_comment")
        user_is_valid = isinstance(request.user, User)

        if user_is_valid:
            try:
                watchlist = Watchlist.objects.get(user=request.user)
            except Exception as e:
                print(f"Unexpected Watchlist Error: {e}")
                watchlist = Watchlist(user=request.user)
                watchlist.save()
            
            remove = False
            if watchlist.listings.count() > 0:
                if listing in watchlist.listings.all():
                    remove = True
        else:
            remove = False

        bids = Bid.objects.filter(listing=listing)
        for comment in listing.comments:
            if comment["user"] == user:
                comment["comment"] = updated_comment
                listing.save()
                break

        current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

        if current_bid is None:
            current_bid = listing.starting_bid

        print(f"Winner: {listing.winner}")
        print(f"User: {request.user.username}")
        
        return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
            "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": remove,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": bids,
            "current_bid": current_bid
        })
    
def delete_comment(request, listing_id, user, comment):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user_is_valid = isinstance(request.user, User)

        if user_is_valid:
            try:
                watchlist = Watchlist.objects.get(user=request.user)
            except Exception as e:
                print(f"Unexpected Watchlist Error: {e}")
                watchlist = Watchlist(user=request.user)
                watchlist.save()
            
            remove = False
            if watchlist.listings.count() > 0:
                if listing in watchlist.listings.all():
                    remove = True
        else:
            remove = False

        bids = Bid.objects.filter(listing=listing)
        new_comments = []
        print(f"User: {user}")
        for saved_comment in listing.comments:
            if (saved_comment["user"] == user and comment == saved_comment["comment"]):
                print(f"Saved comment user: {saved_comment['user']}")
                print(f"Comment to delete: {comment}")
                print(f"Saved comment: {saved_comment['comment']}")
            else:
                new_comments.append(saved_comment)
        
        listing.comments = new_comments
        listing.save()

        current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

        if current_bid is None:
            current_bid = listing.starting_bid

        print(f"Winner: {listing.winner}")
        print(f"User: {request.user.username}")
        
        return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
            "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": remove,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": bids,
            "current_bid": current_bid
        })
    
def edit_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        bids = Bid.objects.filter(listing=listing)
        return render(request, "auctions/edit_listing.html", {
            "listing_id": listing.id,
            "title": listing.title,
            "current_bid": listing.starting_bid,
            "image_url": listing.image_url,
            "description": listing.description,
            "selected_category": listing.category
        })

def submit_edits(request, listing_id):
    if request.method == "POST":
        user_is_valid = isinstance(request.user, User)

        if user_is_valid:
            try:
                watchlist = Watchlist.objects.get(user=request.user)
            except Exception as e:
                print(f"Unexpected Watchlist Error: {e}")
                watchlist = Watchlist(user=request.user)
                watchlist.save()
            
            remove = False
            if watchlist.listings.count() > 0:
                if listing in watchlist.listings.all():
                    remove = True
        else:
            remove = False

        listing = Listing.objects.get(pk=listing_id)
        listing.title = request.POST.get("title")
        listing.category = request.POST.get("category").capitalize()
        listing.description = request.POST.get("new_listing")
        listing.starting_bid = request.POST.get("starting_bid")
        listing.current_bid = request.POST.get("starting_bid")
        listing.image_url = request.POST.get("image_url")
        listing.save()

        all_bids = Bid.objects.filter(listing=listing)

        return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
            "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": remove,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": all_bids,
            "current_bid": request.POST.get("starting_bid")
        })


def edit_bid(request, bid_id):
    current_bid_price = Bid.objects.get(id=bid_id).new_bid
    return render(request, "auctions/edit_bid.html", {
      "current_bid": current_bid_price,
      "bid_id": bid_id
    })

def submit_bid_edit(request, bid_id):
    current_bid = Bid.objects.get(id=bid_id)
    listing = current_bid.listing
    user_is_valid = isinstance(request.user, User)
    if not listing.closed:
        current_bid.new_bid = request.POST.get("new_bid")
        current_bid.save()

        master_bid = current_bid.new_bid

        print(f"Current bid: {listing.current_bid}")
        print(f"Listing title: {listing.title}")
        listing.starting_bid = request.POST.get("new_bid")
        listing.current_bid = request.POST.get("new_bid")
        listing.save()
    else:
        return HttpResponse("Listing is closed! No further edits can be made at this time.")

    all_bids = Bid.objects.filter(listing=listing)

    if user_is_valid:
        try:
            watchlist = Watchlist.objects.get(user=request.user)
        except Exception as e:
            print(f"Unexpected Watchlist Error: {e}")
            watchlist = Watchlist(user=request.user)
            watchlist.save()
        
        remove = False
        if watchlist.listings.count() > 0:
            if listing in watchlist.listings.all():
                remove = True
    else:
        remove = False

    return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
  	        "listing": current_bid.listing,
            "user_is_valid": user_is_valid,
            "remove": remove,
            "closed": current_bid.listing.closed,
            "winner": current_bid.listing.winner,
            "bids": all_bids,
            "current_bid": master_bid
        })

def delete_bid(request, bid_id):
    user_bid = get_object_or_404(Bid, pk=bid_id)
    listing = user_bid.listing
    all_bids = Bid.objects.filter(listing=listing)
    user_bid.delete()
    user_is_valid = isinstance(request.user, User)

    if user_is_valid:
        try:
            watchlist = Watchlist.objects.get(user=request.user)
        except Exception as e:
            print(f"Unexpected Watchlist Error: {e}")
            watchlist = Watchlist(user=request.user)
            watchlist.save()
        
        remove = False
        if watchlist.listings.count() > 0:
            if listing in watchlist.listings.all():
                remove = True
    else:
        remove = False

    current_bid = Bid.objects.filter(listing=listing).aggregate(Max('new_bid'))['new_bid__max']

    if current_bid is None:
        current_bid = listing.starting_bid
        listing.current_bid = listing.starting_bid
        listing.save()

    print(f"Winner: {listing.winner}")
    print(f"User: {request.user.username}")

    return render(request, "auctions/listing_page.html", {
            "user": request.user.username,
  	        "listing": listing,
            "user_is_valid": user_is_valid,
            "remove": remove,
            "closed": listing.closed,
            "winner": listing.winner,
            "bids": all_bids,
            "current_bid": current_bid
        })
