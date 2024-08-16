from .models import ProfileModel, PageSeenModel


def profile_information(request):
    if request.user.is_authenticated:
        profile = ProfileModel.objects.get(user=request.user)
    else:
        profile = ''
    return {'profile': profile}

def page_seen_number(request):
    return {'page_seen_number': PageSeenModel.objects.all().count()}