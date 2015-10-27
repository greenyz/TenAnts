from django.conf.urls import url

from . import views
# ************* THIS IS WHERE /api URLS GO


urlpatterns = [
    url(r'^account$', views.account, name='account'),
    url(r'^login$', views.login_api, name='login_api'),
    url(r'^logout$', views.logout_api, name='logout_api'),
    url(r'^housing$', views.handle_search, name='handle_search'),
    url(r'^housing/(?P<post_id>[0-9]+)$', views.handle_full_post, name='handle_full_post'),
]
