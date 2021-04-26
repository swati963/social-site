from django.urls import path
from land.views import Index
urlpatterns=[
path('',Index.as_view(),name='index'),

]


