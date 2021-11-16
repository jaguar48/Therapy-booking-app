import decimal
from django.contrib.auth import authenticate, backends,login, tokens, views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.api import success
from django.db.models.query_utils import Q
from django.dispatch.dispatcher import receiver
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import EmailMessage
from django.views.generic import TemplateView,View, DeleteView,DetailView
from .models import book, profile
from .forms import LoginForm, SignUpForm,ProfileEditForm,UserEditForm,BookForm
from django.urls import reverse_lazy, reverse
from django.contrib.sites.shortcuts import get_current_site
from  django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import accountactivation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, request
from django.utils import timezone
from .models import User
# import shortuuid

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class Homepage(TemplateView):
    template_name= "home/home.html"

def user_login(request):
    prime = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":

        if prime.is_valid():
            username = prime.cleaned_data.get("username")
            password = prime.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect(reverse_lazy('calls'))
                else:
                    login(request, user)
                    return redirect("/")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the prime'    

    return render(request, "registration/login.html", {"prime": prime, "msg" : msg})

def register(request):
    msg     = None
    success = False

    if request.method == "POST":
        prime = SignUpForm(request.POST)
        
        
        if prime.is_valid():
           
            user = prime.save(commit= False)
        
            user.is_active = False
            # user_id = shortuuid.ShortUUID(alphabet ="0123456789")
            # user_rand = user_id.random(length= 5)

            # user = prime.objects.create(field_name = user_rand)
            
            user.save()
            
         
            
            profile.objects.create(user=user)
            current_site = get_current_site(request)

            subject = "activate your account to proceed"
            message = render_to_string('emails/account_activation_email.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': accountactivation.make_token(user),
            })
            to_email = prime.cleaned_data.get('email')
            email = EmailMessage(subject,message, to = [to_email])
            email.send('please confirm your email to complete registration')

            msg     = 'User created - please go to your email to confirm to enable login <a href="/login">login</a>.'
            success = True
        else:
            msg = 'prime is invalid'
        
    else:
        prime = SignUpForm()
    return render(request, "registration/register.html", {"prime": prime,'msg':msg, 'success':success})



class Accountactivate(View):
    def get(self, request, uidb64, token, *args, **kwargs):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and accountactivation.check_token(user,token):
            user.is_active = True
            user.save()
            login(request,user)
            messages.success(request, 'your account has been confirmed')
            return redirect('/')
        else:
            messages.warning(request,'the confirmation link is invalid, possibly it has been used')
        return redirect('/')

@login_required
def edit(request):
    if request.method == 'POST':
        user_prime = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_prime = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
                                    
        if user_prime.is_valid() and profile_prime.is_valid():
            user_prime.save()
            profile_prime.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('/')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_prime = UserEditForm(instance= request.user)
        profile_prime = ProfileEditForm(instance= request.user.profile)

    return render(request,'registration/edit.html',{'user_prime': user_prime,'profile_prime': profile_prime})


@login_required
def contact(request):
    success = False
    if request.method == 'POST':
        prime = BookForm(data=request.POST)
        if prime.is_valid():
            
            prime.save(commit=False)
            
            user_email = prime.cleaned_data['email']
            subject = prime.cleaned_data['subject']
            if prime.cleaned_data['subject'] == "Other":
                prime.subject = request.POST.get('specify')
            
            pindetails = prime.cleaned_data['identification']
            # cc_myself = prime.cleaned_data['cc_myself']
            
            reciptents = 'admin@example.com'

            send_dt = prime.cleaned_data['send_dt']
            if send_dt is None:
                send_dt = "Immediately"
            else: 
                send_dt = prime.cleaned_data['send_dt']
            
            text = f'hello {request.user.username} booked a call with number: {pindetails}, your scheduled date is {send_dt} and {subject} is the topic'
            
            prime.instance.user = request.user
            prime.save()
            # texts= f'hello {name} you have sucessfully booked a call with number: {pindetails}, and {subject} is your topic..An agent will connect {send_dt}'
            # message_2 = (subject, texts,user_email,['admin@example.com'] )
            
            try:
                send_mail(subject,text,user_email,[reciptents])
                success = True
            except BadHeaderError:
                return HttpResponse('Invalid header found')
    else: 
        prime = BookForm()
    return render(request, 'home/schedule.html', {'prime': prime,'success':success})

def call_logs(request):
    

    calls = book.objects.filter(user= request.user)
    print(calls)
    return render(request,'home/call_logs.html',{
        'calls':calls
    })

class call_delete(DeleteView):
    model = book
    success_url = "/"
    template_name = "home/delete_view.html"

class see_feedback(DetailView):
    model = book
    context_object_name ="feeds"
    template_name = "feed_view.html"

