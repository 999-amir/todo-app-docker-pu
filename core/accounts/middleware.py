from .models import PageSeenModel


class PageSeenMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        system = request.META['HTTP_USER_AGENT']
        session_key = request.session.session_key
        PageSeenModel.objects.get_or_create(ip=ip, system=system, session_key=session_key)
        print('*************')
        print(request.session.session_key)
        print('*************')

        response = self.get_response(request)
        return response