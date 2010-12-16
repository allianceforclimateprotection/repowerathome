from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from forms import StickerImageUpload

def sticker_upload(request):
    form = StickerImageUpload(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Thanks for sharing! We'll put it up after we take a quick look.")
    else:
        messages.error(request, "There was a problem uploading your image.")
    return redirect('trendsetter_sticker')
