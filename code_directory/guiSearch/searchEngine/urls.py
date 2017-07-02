from django.conf.urls import url

from . import views

# these are all of the urls that the various functions call that help redirect things
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^add_data$', views.add_data, name='add_data'),
    url(r'^usage$', views.usage, name='usage'),
    url(r'^countSearch/$', views.countSearch, name='countSearch'),
    url(r'^searchAlg/$', views.searchAlg, name='searchAlg'),
    url(r'^hamming_search/$', views.hamming_search, name='hamming_search'),
    url(r'^euclidean_search/$', views.euclidean_search, name='euclidean_search'),
    url(r'^parse_new_data/$', views.parse_new_data, name='parse_new_data'),
]

