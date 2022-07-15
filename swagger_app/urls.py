from django.urls import path

from swagger_app.views import index

urlpatterns = [
    path('', index),
    path('s-<str:service_slug>/', index),
    path('b-<str:brand_slug>/', index),
    path('st-<str:style_slug>/', index),
    path('s-<str:service_slug>/b-<str:brand_slug>/', index),
    path('s-<str:service_slug>/b-<str:brand_slug>/st-<str:style_slug>/', index),
]
