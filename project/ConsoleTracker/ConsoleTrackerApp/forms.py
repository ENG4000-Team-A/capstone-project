from django import forms
from .InternalSocketConnect import InternalSocket

# Login Form
class NameForm(forms.Form):
    uname = forms.CharField(label='Username', max_length=50)
    pword = forms.CharField(label='Password', max_length=50)

    def validate_login(self, username, password):
        socket = InternalSocket()
        return socket.send_request(username, password)
