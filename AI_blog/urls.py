from django.urls import path, include
from . import views

urlpatterns = [
   path('',views.index,name='index'),
   path('login/',views.user_login,name='login'),
   path('signup/',views.user_signup,name='signup'),
   path('logout/',views.logout,name='logout'),
   path('generate-blog',views.gen_blog,name='gen_blog'), #SAVE BLOG TO DATABASE
   
]