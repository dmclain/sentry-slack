from __future__ import absolute_import

from django import forms

from sentry.plugins import plugins
from sentry.rules.actions.base import EventAction


class NotifySlackRoomForm(forms.Form):
    room = forms.CharField()
    label = forms.CharField()


class NotifySlackRoomAction(EventAction):
    form_cls = NotifySlackRoomForm
    label = 'Send a notification to a Slack {room} labeled {label}'

    def after(self, event, state):
        room = self.get_option('room')

        if not room:
            return

        plugin = plugins.get('slack')
        if not plugin.is_enabled(self.project):
            return

        prefix = self.get_option('label') or 'Rule Triggered'
        yield self.future(plugin.send_event_to_slack, event=event, prefix=prefix, room=room)
