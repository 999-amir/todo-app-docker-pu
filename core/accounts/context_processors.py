from .models import ProfileModel


def profile_information(request):
    if request.user.is_authenticated:
        profile = ProfileModel.objects.get(user=request.user)
    else:
        profile = ""
    return {"profile": profile}
