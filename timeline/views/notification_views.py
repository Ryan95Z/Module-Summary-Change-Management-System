from timeline.models import Notification, Watcher
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse


class NotificationHubView(View):
    model = Notification
    template = "timeline/notification_list.html"

    def get(self, request, *args, **kwargs):
        username = request.user.username
        user_id = request.user.pk

        # remove old notifications
        self.__remove_old_notifications(username)

        unseen = self.model.objects.get_unseen_notifications(username)
        all_notifications = self.model.objects.get_all_notifications(username)

        # get all the modules the user is watching
        watching = Watcher.objects.get(user=user_id).watching.all()
        context = {
            'unseen': unseen,
            'all': all_notifications,
            'watching': watching,
        }
        return render(request, self.template, context)

    def __remove_old_notifications(self, username):
        notifications = self.model.objects.get_unneeded_notifications(username)
        if(notifications.count() > 0):
            notifications.delete()


class NotificationRedirectView(View):
    model = Notification

    def get(self, request, *args, **kwargs):
        notification_id = kwargs['pk']
        notification = get_object_or_404(self.model, pk=notification_id)
        notification.seen = True
        notification.save()
        return redirect(notification.link)


class GetNotifications(View):
    model = Notification

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'post' or request.is_ajax():
            handle = self.post(request, *args, **kwargs)
        else:
            handle = self.http_method_not_allowed(request, *args, **kwargs)
        return handle

    def post(self, request, *args, **kwargs):
        username = request.POST.get('user', '')
        unseen = self.model.objects.get_unseen_notifications(username)
        data = {
            'has_notifications': unseen.count() > 0,
        }
        return JsonResponse(data)