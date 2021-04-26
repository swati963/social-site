from django.urls import path
from .views import PostListing,PostContents,EditingPosts,DeletingPosts,DeleteComment, UserProfileView, EditProfile,AddFollowers,RemoveFollowers, AddLikes,DisLikes, UserSearch,FollowersList,CommentLikes,CommentDisLikes,CommentReply,PostNotification,FollowNotification, DeleteNotification,Stories


urlpatterns=[
		path('',PostListing.as_view(),name='postlist'),
		path('post/<int:pk>/',PostContents.as_view(),name='postcontent'),
		path('post/edit/<int:pk>/',EditingPosts.as_view(),name='editpost'),
		path('post/delete/<int:pk>/',DeletingPosts.as_view(),name='deletepost'),
		path('post/<int:post_pk>/comment/delete/<int:pk>/',DeleteComment.as_view(),name='deletecomment'),
		path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
		path('profile/edit/<int:pk>/',EditProfile.as_view(), name='editprofile'),
		path('profile/<int:pk>/followers/add',AddFollowers.as_view(), name='addfollowers'),
		path('profile/<int:pk>/followers/remove',RemoveFollowers.as_view(), name='removefollowers'),
		
		path('profile/<int:pk>/followers/',FollowersList.as_view(), name='followerslist'),


		path('post/<int:pk>/likes', AddLikes.as_view(), name='likes'),
        path('post/<int:pk>/dislikes', DisLikes.as_view(), name='dislikes'),


        path('post/<int:post_pk>/comment/<int:pk>/like', CommentLikes.as_view(), name='commentlikes'),
    	path('post/<int:post_pk>/comment/<int:pk>/dislike', CommentDisLikes.as_view(), name='commentdislikes'),
		
		path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReply.as_view(), name='commentreply'),
		
		path('search/',UserSearch.as_view(),name='profilesearch'),


		path('notification/<int:notification_pk>/post/<int:post_pk>', PostNotification.as_view(), name='postnotification'),
    	path('notification/<int:notification_pk>/profile/<int:profile_pk>', FollowNotification.as_view(), name='follownotification'),
    	path('notification/delete/<int:notification_pk>', DeleteNotification.as_view(), name='deletenotification'),

]
