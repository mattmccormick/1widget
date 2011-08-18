from django.contrib.auth.models import User

class EmailBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
        if user.check_password(password):
            return user