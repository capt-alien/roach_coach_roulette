from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index), # to homepage
    url(r'^optionsDisplay$', views.optionsDisplay), # to page where they will choose distance
    url(r'^roulette/(?P<choice_id>\d+)$', views.roulette), # will process their request and redirect to resultsDisplay
    url(r'^resultsDisplay$', views.resultsDisplay), # to page that will display results
    url(r'^viewInfo/(?P<result_id>\d+)$', views.viewInfo), #to page that will display details about specific restaurant
    url(r'^GoBack$', views.goBack),# to go back to homepage and start over "delete session"
    url(r'^loginReg$',views.loginReg),# to login and registration page
    url(r'^newUser$', views.newUser),# to create the new user
    url(r'^dashboard$', views.dashboard), # to display their personal dashboard
    url(r'^edit/(?P<fav_id>\d+)$', views.edit), # to edit the user's favorites to add notes.
    url(r'^edit_note/(?P<fav_id>\d+)$', views.edit_note),
    url(r'^refresh$', views.refresh), # to refresh the options
    url(r'^login$', views.login), #login
    url(r'reset$', views.reset), # clear cookies
    url(r'^save/(?P<choice_id>\d+)$', views.save), # save for later
    url(r'^move_to_fav/(?P<save_id>\d+)$', views.move_to_fav),
    url(r'remove_from_saved/(?P<save_id>\d+)$', views.remove_from_saved)
]
