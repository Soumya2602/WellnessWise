import os
import re

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render

from django.conf import settings
from .maindir.symptomChecker import prediction


def get_text(filed , filed1):
    print('done')

def symptoms(request):
    if request.method == 'POST' and 'audio' not in request.FILES:
        values = list(request.POST.dict().values())
        user_symptoms = values[:-1]
        days = int(values[-1])
        advice, output = prediction(user_symptoms , days)
        context = {
            "advice":advice,
            "output":output
        }
        return JsonResponse(context)
    
    if request.method == 'POST' and 'audio' in request.FILES:
        audio_data = request.FILES["audio"]
        fss = FileSystemStorage()
        file_name = audio_data.name + ".webm"
        file = fss.save(file_name, audio_data)
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        text = get_text(file_path , file_name)
        out = re.findall("[a-zA-Z]+", text)
        advice, output = prediction(out)
        print(advice , output)
        context = {
            "advice":advice,
            "output":output
        }
        return JsonResponse(context)
    
    else:
        return render(request , 'index.html')