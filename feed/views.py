from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.views import View
from .models import Post,Comments,UserProfile,Notification,Stories
from .forms import PForms,CommentsForms
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView 



class PostListing(LoginRequiredMixin,View):

	def get(self,request,*args,**kwargs):		
		loggedinuser=request.user
		
		allpost=Post.objects.filter(createduser__profile__followers__in=[loggedinuser.id]
			).order_by('-createdon')
		

		form=PForms()
		context={
		'postlist':allpost,
		'form':form,
		}
		return render(request,'feed/postlist.html',context)

	def post(self,request,*args,**kwargs):
		
		loggedinuser=request.user
		allpost=Post.objects.filter(createduser__profile__followers__in=[loggedinuser.id]
			).order_by('-createdon')
		
		form=PForms(request.POST,request.FILES)
		if form.is_valid():
			newpost=form.save(commit=False)
			
			newpost.createduser=request.user
			newpost.save()
			messages.info(request," Congrats!! you just added a post on your profile")
		
			context={
				'postlist':allpost,
				'form':form,

			}
		return render(request,'feed/postlist.html',context)


class PostContents(LoginRequiredMixin,View):

	def get(self,request,pk,*args,**kwargs):

		
		allpost=Post.objects.get(pk=pk)
		form=CommentsForms()

		
		allcomments=Comments.objects.filter(post=allpost).order_by('-createdon')


		context={
				'post':allpost,
				'form':form,
				'comments':allcomments,
			}
		return render(request,'feed/postcontent.html',context)

	def post(self,request,pk,*args,**kwargs):
		
		allpost=Post.objects.get(pk=pk)
		
		form=CommentsForms(request.POST)
		if form.is_valid():
			newcomment=form.save(commit=False)
			newcomment.createduser=request.user			
			newcomment.post=allpost
			newcomment.save()
		
		
		allcomments=Comments.objects.filter(post=allpost).order_by('-createdon')

		notification=Notification.objects.create(notification_type=2,fromuser=request.user,touser=allpost.createduser,post=allpost )

		context={
				'post':allpost,
				'form':form,
				'comments':allcomments,
			}
		return render(request,'feed/postcontent.html',context)


class EditingPosts(LoginRequiredMixin, UserPassesTestMixin,UpdateView):

	model=Post
	fields=['bodyofpost','image']
	template_name='feed/editpost.html'

	def get_success_url(self):
		pk=self.kwargs['pk']
		return reverse_lazy('postcontent',kwargs={'pk':pk})
		

	def test_func(self):
		post=self.get_object()
		return self.request.user==post.createduser
		

class DeletingPosts(LoginRequiredMixin, UserPassesTestMixin,DeleteView):

	model=Post
	template_name='feed/deletepost.html'
	success_url=reverse_lazy('postlist')

	def test_func(self):
		post=self.get_object()
		return self.request.user==post.createduser

class DeleteComment(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
	model=Comments
	template_name='feed/deletecomment.html'
	
	def get_success_url(self):
		pk=self.kwargs['post_pk']
		return reverse_lazy('postcontent',kwargs={'pk':pk})

	def test_func(self):
		
		post=self.get_object()
		return self.request.user==post.createduser
		


class UserProfileView(View):
	def get(self,request,pk,*args,**kwargs):
		
		profile = UserProfile.objects.get(pk=pk)

		
		user=profile.user
	
		posts = Post.objects.filter(createduser=user).order_by('createdon')

		followers=profile.followers.all()
		following=profile.following.all()

		if len(followers)==0:
			is_following=False


		for follower in followers:
			if follower==request.user:
				is_following=True
				break
			else:
				is_following=False


		numberoffollowers=len(followers)
		numberoffollowing=len(following)
		context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'numberoffollowers':numberoffollowers,
            'is_following':is_following

		}

		return render(request, 'feed/profile.html', context)



class EditProfile(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
	
	model=UserProfile

	fields=['name','email','phone','gender','bio','birthday','urllink','location','profilepicture','gender']
	template_name='feed/editprofile.html'

	def get_success_url(self):
		pk=self.kwargs['pk']
		return reverse_lazy('profile',kwargs={'pk':pk})
		
	
	def test_func(self):
		
		profile=self.get_object()
		return self.request.user==profile.user
		



class AddFollowers(LoginRequiredMixin,View):
	def post(self,request,pk,*args,**kwargs):

		profile=UserProfile.objects.get(pk=pk)
 
		profile.followers.add(request.user)
		
        
		notification=Notification.objects.create(notification_type=3,fromuser=request.user,touser=profile.user )
		
		return redirect('profile',pk=profile.pk)



class RemoveFollowers(LoginRequiredMixin,View):
	def post(self,request,pk,*args,**kwargs):
		profile=UserProfile.objects.get(pk=pk)
		
		profile.followers.remove(request.user)

		return redirect('profile',pk=profile.pk)




class AddLikes(LoginRequiredMixin,View):
	def post(self,request,pk,*args,**kwargs):
		post=Post.objects.get(pk=pk)

		is_dislike=False

		for dislike in post.dislikes.all():
			if dislike== request.user:
				is_dislike=True
				break
	
		if is_dislike:
			post.dislikes.remove(request.user)

		is_like=False

		
		for like in post.likes.all():
			
			if like== request.user:
				is_like=True
				break
		if not is_like:
			
			post.likes.add(request.user)

		notification=Notification.objects.create(notification_type=1,fromuser=request.user,touser=post.createduser,post=post )
			
		if is_like:
			
			post.likes.remove(request.user)
		
		next=request.POST.get('next','/')
		return HttpResponseRedirect(next)


class DisLikes(LoginRequiredMixin,View):
	def post(self,request,pk,*args,**kwargs):
		post=Post.objects.get(pk=pk)

		is_like=False

		for like in post.likes.all():
			if like== request.user:
				is_like=True
				break
		 
		if is_like:
			post.likes.remove(request.user)

		is_dislike=False

		for dislike in post.dislikes.all():
			if dislike== request.user:
				is_dislike=True
				break

		if not is_dislike:
			post.dislikes.add(request.user)

		if is_dislike:
			post.dislikes.remove(request.user)

		next=request.POST.get('next','/')
		return HttpResponseRedirect(next)



class UserSearch(View):
	
	def get(self,request,*args,**kwargs):
		
		query=self.request.GET.get('query')

		profilelist=UserProfile.objects.filter(Q(user__username__icontains=query)|Q(email__icontains=query)|Q(phone__icontains=query))
		context={
			'profilelist':profilelist
		}
		if len(profilelist)==0:
			messages.warning(request," Sorry But There's no matching result based on your query")
		else:
			messages.info(request," We have found these results based on your search")
		


		return render(request,'feed/search.html',context)


class FollowersList(View):
	def get(self,request,pk,*args,**kwargs):
		profile=UserProfile.objects.get(pk=pk)

		followers=profile.followers.all()

		context={
		'profile':profile,
		'followers':followers,
		}

		return render(request,'feed/followerslist.html',context)




class CommentLikes(LoginRequiredMixin,View):
	def post(self,request,pk,*args,**kwargs):
		comment=Comments.objects.get(pk=pk)

		is_dislike=False

		for dislike in comment.dislikes.all():
			if dislike== request.user:
				is_dislike=True
				break
		if is_dislike:
			comment.dislikes.remove(request.user)

		is_like=False

		for like in comment.likes.all():
			if like== request.user:
				is_like=True
				break
		if not is_like:
			comment.likes.add(request.user)

		notification=Notification.objects.create(notification_type=1,fromuser=request.user,touser=comment.createduser,comment=comment )
			
		if is_like:
			comment.likes.remove(request.user)
		
		next=request.POST.get('next','/')
		return HttpResponseRedirect(next)


class CommentDisLikes(LoginRequiredMixin,View):
	def post(self,request,pk,*args,**kwargs):
		comment=Comments.objects.get(pk=pk)

		is_like=False

		for like in comment.likes.all():
			if like== request.user:
				is_like=True
				break
		
		if is_like:
			comment.likes.remove(request.user)

		is_dislike=False

		for dislike in comment.dislikes.all():
			if dislike== request.user:
				is_dislike=True
				break

		if not is_dislike:
			comment.dislikes.add(request.user)

		if is_dislike:
			comment.dislikes.remove(request.user)

		next=request.POST.get('next','/')
		return HttpResponseRedirect(next)



class CommentReply(LoginRequiredMixin,View):
	#to handle submission of form
	def post(self,request,pk,post_pk,*args,**kwargs):
		post=Post.objects.get(pk=post_pk)
		parent_comment=Comments.objects.get(pk=pk)

		form=CommentsForms(request.POST)

		if form.is_valid():
			newcomment=form.save(commit=False)
			newcomment.createduser=request.user
			newcomment.post=post
			newcomment.parent=parent_comment
			newcomment.save()


		notification=Notification.objects.create(notification_type=2,fromuser=request.user,touser=parent_comment.createduser,comment=newcomment )	

		return redirect('postcontent',pk=post_pk)





class PostNotification(View): 
	def get(self,request, notification_pk,post_pk,*args,**kwargs):
		notification=Notification.objects.get(pk=notification_pk)
		post=Post.objects.get(pk=post_pk)

		notification.userseen=True
		notification.save()

		return redirect('postcontent',pk=post_pk)


class FollowNotification(View):
	def get(self,request, notification_pk,profile_pk,*args,**kwargs):
		notification=Notification.objects.get(pk=notification_pk)
		profile=UserProfile.objects.get(pk=profile_pk)

		notification.userseen=True
		notification.save()

		return redirect('profile',pk=profile_pk)



class DeleteNotification(View):
	def delete(self, request, notification_pk, *args, **kwargs):
		notification = Notification.objects.get(pk=notification_pk)

		notification.userseen = True
		notification.save()

		return HttpResponse('Success', content_type='text/plain')




class Stories(View):
	def get(self,request,*args,**kkwargs):
		user=request.user
		return HttpResponse("Hello")