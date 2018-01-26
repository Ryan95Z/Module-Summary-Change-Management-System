from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from core.views import *

urlpatterns = [
    # login and logout routes
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),

    # urls for accessing admin parts
    url(r'^all/$', login_required(UserListView.as_view()), name='all_users'),
    url(r'^all/edit/(?P<pk>[0-9]+)/$', login_required(
        AdminUpdateUserPermissions.as_view()), name='edit_user'),

    # year tutor urls
    url(r'^tutors/$', login_required(
        AdminYearTutorListView.as_view()), name='all_year_tutors'),

    # generic user profile urls
    url(r'^profile/(?P<slug>[\w.@+-]+)/$',
        login_required(UserSettingsView.as_view()), name='user_settings'),
    url(r'^profile/(?P<slug>[\w.@+-]+)/details/$',
        login_required(UserUpdateDetailsView.as_view()), name='user_details'),
    url(r'^profile/(?P<slug>[\w.@+-]+)/password/$',
        login_required(UserUpdatePasswordView.as_view()), name='user_password')
]
