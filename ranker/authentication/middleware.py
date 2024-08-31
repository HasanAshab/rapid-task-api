from ranker.users.models import User


class UsernameAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = request.GET.get('auth')
        print(username)
        if username:
            request.user = User.objects.filter(username=username).first()
        print(request.user)
        return self.get_response(request)
