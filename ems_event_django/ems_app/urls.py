from . import views
from django.urls import path

urlpatterns = [
    path('', views.events, name='index'),
    path("organizator/register/", views.CreateAccountView.as_view(), name="register"),
    path("organizator/login/", views.LoginAccountView.as_view(), name="login"),
    path("organizator/dashboard/", views.dashboard, name="dashboard"),
    path("organizator/logout/", views.log_out, name="logout"),
    path("organizator/dashboard/account/", views.account, name="account"),
    path("organizator/dashboard/account/edit/", views.EDAccountView.as_view(), name="edit_account"),
    path("organizator/dashboard/account/change-password/", views.CHPasswordView.as_view(), name="change_password"),
    path("organizator/reset-password/", views.PWDResetView.as_view(), name="reset_password"),
    path("organizator/dashboard/account/delete", views.DLAccountView.as_view(), name="delete_account"),
    path("organizator/dashboard/events/", views.dashboard_events, name="dashboard_events"),
    path("organizator/dashboard/events/new/", views.create_event, name="create_event"),
    path("organizator/dashboard/events/<int:id>/edit", views.edit_event, name="edit_event"),
    path("organizator/dashboard/events/<int:id>/delete", views.delete_event, name="delete_event"),
    path("organizator/dashboard/events/<int:id>/", views.dashboard_event_details, name="dashboard_event_details"),
    path("organizator/dashboard/events/<int:id>/attendees", views.view_attendees, name="attendees"),
    path("organizator/dashboard/events/<int:eid>/attendees/<int:aid>/delete", views.delete_attendee, name="delete_attendee"),
    path("organizator/dashboard/events/<int:eid>/attendees/<int:aid>/ticket", views.show_ticket, name="show_ticket"),
    path("events/<int:eid>/attendance/<int:aid>/ticket", views.attendee_ticket, name="attendee_ticket"),
    path("events/", views.events, name="events"),
    path("events/<int:id>/", views.event_details, name="event_details"),
    path("events/<int:id>/register/", views.attend_event, name="register"),

]