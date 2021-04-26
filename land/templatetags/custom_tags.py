from django import template
from feed.models import Notification

register=template.Library()


#route of location of template, tkaescontnt allow to pass content to template

@register.inclusion_tag('feed/notifications.html',takes_context=True)
def shownotifications(context):
	#get current user who is logged in and all notifications
	#context that we passedin in that dict we have and obj request in which we have property of user
	request_user=context['request'].user

	#to user is hwo is recving notifction so get all notifctns excpt seen this current user if recving (if rcving and rqstng user matches take notiction) and show newest first
	notifications=Notification.objects.filter(touser=request_user).exclude(userseen=True).order_by('-date')

	return {'notifications':notifications}




