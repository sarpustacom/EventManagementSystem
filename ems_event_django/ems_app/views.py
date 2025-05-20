from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, UserChangeForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models
from . import ticket_create as tck
# Create your views here.
#MARK: Index
def index(request):
    return render(request, 'ems_app/index.html')

#MARK: Dashboard
@login_required(login_url=reverse_lazy("login"))
def dashboard(request):
    return render(request, 'ems_app/dashboard.html')

#MARK: Logout
@login_required(login_url=reverse_lazy("login"))
def log_out(request):
    logout(request)
    return redirect(reverse_lazy("index"))

#MARK: Account
@login_required(login_url=reverse_lazy("login"))
def account(request):
    return render(request, 'ems_app/account.html')

#MARK: Dashboard Events
@login_required(login_url=reverse_lazy("login"))
def dashboard_events(request):
    events = models.EventModel.objects.filter(organizedby=request.user)
    return render(request, 'ems_app/event/dashboard_events.html', context={"events":events})

#MARK: Create Event
@login_required(login_url=reverse_lazy("login"))
def create_event(request):

    if request.POST and request.FILES:
        form = forms.EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.fields["organizedby"] = request.user
            event = form.save(commit=False)
            event.organizedby = request.user
            event.save()
            return redirect(reverse_lazy("dashboard_events"))
        else:
            return render(request, 'ems_app/event/create_event.html', {"form":form, "error":form.errors})
    else:
        event_form = forms.EventForm()
        return render(request, 'ems_app/event/create_event.html', {"form":event_form})

#MARK: Edit Event
@login_required(login_url=reverse_lazy("login"))
def edit_event(request, id):
    event = models.EventModel.objects.get(pk=id)
    if request.POST:
        form = forms.EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizedby = request.user
            event.save()
            return redirect(reverse_lazy("dashboard_events"))
        else:
            return render(request, 'ems_app/event/edit_event.html', {"form":form, "error":form.errors})
    else:
        event_form = forms.EventForm(instance=event)
        return render(request, 'ems_app/event/edit_event.html', {"form":event_form})


#MARK: Delete Event
@login_required(login_url=reverse_lazy("login"))
def delete_event(request, id):
    if request.POST:
        event = models.EventModel.objects.get(id=id)
        event.coverphoto.delete()
        event.delete()
        return redirect(reverse_lazy("dashboard_events"))
    else:
        return render(request, 'ems_app/event/del_event_confirm.html')
    
#MARK: Event Details
@login_required(login_url=reverse_lazy("login"))
def dashboard_event_details(request, id):
    event = models.EventModel.objects.get(id=id)
    return render(request, 'ems_app/event/dashboard_event_details.html', {"event":event})

#MARK: View Attendees
@login_required(login_url=reverse_lazy("login"))
def view_attendees(request, id):
    event = models.EventModel.objects.get(id=id)
    attendees = models.AttendeeModel.objects.filter(event=event)
    return render(request, 'ems_app/event/view_attendees.html', {"event":event,"attendees":attendees})

#MARK: Edit Account
@login_required(login_url=reverse_lazy("login"))
def delete_attendee(request, eid, aid):
    attendee = models.AttendeeModel.objects.get(id=aid)
    attendee.delete()
    return redirect(reverse_lazy("attendees"))

#MARK: Events & Details (Home)

def events(request):
    events = models.EventModel.objects.all()
    return render(request, 'ems_app/event/events.html', {"events":events})

def event_details(request, id):
    event = models.EventModel.objects.get(id=id)
    return render(request, 'ems_app/event/event_details.html', {"event":event})

#MARK: Attend Event
def attend_event(request, id):
    event = models.EventModel.objects.get(id=id)
    if request.POST:
        form = forms.AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.event = event
            attendee.ticket = tck.create_ticket(attendee)
            attendee.save()
            print(attendee.ticket.url)
            return redirect(reverse_lazy("attendee_ticket", kwargs={"eid":id,"aid":attendee.id}))
        else:
            return render(request, 'ems_app/event/attend_event.html', {"form":form, "error":form.errors})
    else:
        attendee_form = forms.AttendeeForm()
        return render(request, 'ems_app/event/attend_event.html', {"form":attendee_form, "event":event})
    
#MARK: Show Ticket
@login_required(login_url=reverse_lazy("login"))
def show_ticket(request, eid, aid):
        attendee = models.AttendeeModel.objects.get(id=aid)
        ticket_path = attendee.ticket.url
        return render(request, 'ems_app/event/show_ticket.html', {"ticket":ticket_path})

#MARK: Show Ticket after Registration
def attendee_ticket(request,eid, aid):
    attendee = models.AttendeeModel.objects.get(id=aid)
    return render(request, 'ems_app/event/attendee_ticket.html', {"attendee":attendee})

## Custom Forms compatible with Bootstrap 4
# MARK: Custom Forms
class CustomCreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model= User
        fields = ["first_name","last_name","username", "email", "password1", "password2"]


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model= User
        fields = ["username", "password"]

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model= User
        fields = ["old_password", "new_password1", "new_password2"]

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model= User
        fields = ["email"]

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        model= User
        fields = ["first_name","last_name","username", "email"]


## Form Views for User Registration and Login
## MARK: Form Views
class CreateAccountView(CreateView):
    form_class = CustomCreateUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("login")

class LoginAccountView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy("dashboard")
    redirect_authenticated_user = True

class CHPasswordView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy("account")

class PWDResetView(PasswordResetView):
    
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy("login")

class EDAccountView(UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/edit_account.html'
    success_url = reverse_lazy("account")

    def get_object(self):
        return self.request.user

class DLAccountView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'registration/delete_user_confirm.html'
    success_message = "User Deleted Successfully"
    success_url = reverse_lazy("index")

    def get_object(self):
        return self.request.user
    

