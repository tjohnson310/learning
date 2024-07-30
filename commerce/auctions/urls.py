from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new_listing", views.create_new_listing, name="create_new_listing"),
    path("delete_listing/<int:listing_id>/", views.delete_listing, name="delete_listing"),
    path("listing/<int:listing_id>/", views.nav_to_listing, name="nav_to_listing"),
    path("update_bid/<int:listing_id>/", views.update_bid, name="update_bid"),
    path("close_auction/<int:listing_id>/", views.close_auction, name="close_auction"),
    path("add_to_watchlist/<int:listing_id>/", views.add_to_watchlist, name = "add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>/", views.remove_from_watchlist, name = "remove_from_watchlist"),
    path("watchlist", views.navigate_to_watchlist, name="navigate_to_watchlist")
]
