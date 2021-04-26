from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 

class Post(models.Model):
	bodyofpost=models.TextField()
	image=models.ImageField(upload_to='uploads/postphotos',blank=True,null=True)
	createdon=models.DateTimeField(default=timezone.now)
	createduser=models.ForeignKey(User,on_delete=models.CASCADE)
	likes=models.ManyToManyField(User,blank=True,related_name='likes')
	dislikes=models.ManyToManyField(User,blank=True,related_name='dislikes')

	def __str__(self):
		return str(self.createduser)



class Comments(models.Model):
	
	comment=models.TextField()
	createdon=models.DateTimeField(default=timezone.now)
	createduser=models.ForeignKey(User,on_delete=models.CASCADE)
	post=models.ForeignKey('Post',on_delete=models.CASCADE)
	likes=models.ManyToManyField(User,blank=True,related_name='commentlikes')
	dislikes=models.ManyToManyField(User,blank=True,related_name='commentdislikes')

	
	parent=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='+')
	def __str__(self):
		return str(self.createduser)+"-"+str(self.createdon)




	@property
	def children(self):
		return Comments.objects.filter(parent=self).order_by('-createdon')

	@property
	def is_parent(self):		
		if self.parent is None:
			return True
		return False


class UserProfile(models.Model):

	
	user=models.OneToOneField(User,primary_key=True,verbose_name='user',related_name='profile',on_delete=models.CASCADE)
	name=models.CharField(max_length=100,blank=True,null=True)
	email=models.TextField(max_length=500,blank=True,null=True)
	phone=models.CharField(max_length=10,blank=True,null=True)
	bio=models.TextField(max_length=500,blank=True,null=True)
	gender=models.CharField(max_length=10,blank=True,null=True)
	birthday=models.DateField(null=True,blank=True)
	location=models.CharField(max_length=100,blank=True,null=True)
	profilepicture=models.ImageField(blank=True,upload_to='uploads/profilepictures',default='uploads/profilepictures/default.png')
	followers=models.ManyToManyField(User,default=0,related_name='followers')
	urllink=models.CharField(max_length=150,blank=True,null=True)

	following=models.ManyToManyField(User,default=0,related_name='following')
	def __str__(self):
		return str(self.user)




		
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()




class Notification(models.Model):
	
	notification_type=models.IntegerField()
	touser=models.ForeignKey(User,related_name='notificationto',on_delete=models.CASCADE,null=True)
	fromuser=models.ForeignKey(User,related_name='notificationfrom',on_delete=models.CASCADE,null=True)
	post=models.ForeignKey(Post,related_name='+',on_delete=models.CASCADE,null=True,blank=True)
	comment=models.ForeignKey(Comments,related_name='+',on_delete=models.CASCADE,null=True,blank=True)
	date=models.DateTimeField(default=timezone.now)
	userseen=models.BooleanField(default=False)
	def __str__(self):
		return str(self.notification_type)+"-"+str(self.date)





class Stories(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	image=models.ImageField(upload_to='uploads/poststories',blank=True,null=True)
	createdon=models.DateTimeField(default=timezone.now)
	createdend=models.BooleanField(default=False)


	def __str__(self):
		return str(self.user)+"-"+str(self.createdon)


