from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt

from PIL import Image, ImageFilter
from tesserocr import PyTessBaseAPI
from django.shortcuts import render, redirect, get_object_or_404


def form(request):
    if request.method == 'POST':
        with PyTessBaseAPI() as api:
            with Image.open(request.FILES['image']) as image:
                sharpened_image = image.filter(ImageFilter.SHARPEN)
                api.SetImage(sharpened_image)
                utf8_text = api.GetUTF8Text()

        return JsonResponse({'utf8_text': utf8_text})
    else:
        return render(request, 'documents/ocr_form.html', {})
