from models import ASK_TO_SHARE_TOKEN

def ask_to_share(request):
    context = {}
    if ASK_TO_SHARE_TOKEN in request.session:
        del request.session[ASK_TO_SHARE_TOKEN]
        context["ask_to_share"] = True
    return context