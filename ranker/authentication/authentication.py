from rest_framework.authentication import BaseAuthentication
from ranker.users.models import User


class UsernameAuthentication(BaseAuthentication):

    def authenticate(self, request):
        username = request.GET.get('auth')
        if username:
            user = User.objects.filter(username=username).first()
            return (user, None)
