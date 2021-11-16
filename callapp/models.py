from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

Bookingchoice =(
    ("Marital/Relationship", "Marital/Relationship"),
    ("Birthday wishes/greetings", "Birthday wishes/greetings"),
    ("Counselling/motivation", "Counselling/motivation"),
    ("Business tips/ideas", "Business tips/ideas"),
    ("Call a friend", "Call a friend"),
    ("Other", "Other"),
)

approval_choice =(
    ("Pending", "Pending"),
    ("Approved","Approved"),
    ("Denied","Denied")
)

class profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    country = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

class book(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=250,null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    specify = models.CharField(max_length=250)
    message = models.TextField()
    identification = models.IntegerField(null=True)
    schedule = models.CharField(max_length=250)
    send_dt = models.DateTimeField(null=True)     
    status = models.CharField( choices=approval_choice, max_length=250, default="Pending")
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    feedback = models.TextField(null=True)

# class blog(models.Model):
#     author = models.ForeignKey(User,on_delete=models.CASCADE)
#     topic = models.CharField(max_length=250)
#     image = models.ImageField()
#     description = models.TextField()
#     like = models.ManyToManyField()
    
# class account(models.Model):
#     owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name="top")
#     account_balance = models.DecimalField(max_digits=10,decimal_places=2)
#     date_created = models.DateField(auto_now_add=True)
#     account_number = models.CharField(max_length=50)


# class transfer(models.Model):
#     owner = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True)
#     from_account = models.CharField(max_length=50)
#     to_account = models.CharField(max_length=50)
#     amount = models.CharField(max_length=50)
#     date_created = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return str(self.amount)
        
    





# @receiver(post_save, sender=User)
# def update_user_profile(sender,instance, created, **kwargs):
#     if created:
#         profile.objects.create(user=instance)
#         instance.profile.save()

# @receiver(post_save, sender=User) #add this
# def create_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		profile.objects.create(user=instance)

# @receiver(post_save, sender=User) #add this
# def save_user_profile(sender, instance, **kwargs):
# 	instance.profile.save()
