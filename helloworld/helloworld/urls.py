# yourproject/helloworld/urls.py
## This should exist
from django.conf.urls import url
from django.contrib import admin
## END This should exist

## Important : Import the views from the demo folder
## to get the index action
from demo import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ## Create the action for : http://127.0.0.1/
    ## Use the index action from the views on /demo/views.py
    url(r'', views.index),
]