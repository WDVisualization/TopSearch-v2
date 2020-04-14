from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('analysis', views.analysisview, name='analysisview'),

    path('lists', views.lists, name = 'lists'),
    path('wdcld', views.wdcld, name = 'wdcld'),
    path('toptwenty', views.toptwenty, name='toptwenty'),
    path('changelists', views.changelists, name='changelists'),

]
