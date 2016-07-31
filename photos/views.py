import telepot
import json
import random
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Photo

telegramBot = telepot.Bot('')

def getPhoto():
    photos = Photo.objects.all()
    ind = random.randint(0, len(photos)-1)
    return photos[ind].file_id

def showHelp():
    return render_to_string('help.md')


class BotView(View):
    def post(self, request, botToken):
        if botToken != '':
            return HttpResponseForbidden('Invalid token')

        raw = request.body.decode('utf-8')

        try:
            payload = json.loads(raw)
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            chat_id = payload['message']['chat']['id']

            if 'photo' in payload['message']:
                cnt = payload['message']['photo']
                image = payload['message']['photo'][len(cnt)-1]['file_id']
                photo = Photo(file_id=image)
                all_photo = Photo.objects.all().count()
                photo.save()
                telegramBot.sendMessage(chat_id=chat_id, text='Saved!')
            elif 'text' in payload['message']:
                cmd = payload['message'].get('text')
                if cmd == '/get':
                    photo_id = getPhoto()
                    telegramBot.sendPhoto(chat_id=chat_id, photo=photo_id)
                elif cmd == '/start' or cmd == '/help':
                    text = showHelp()
                    telegramBot.sendMessage(chat_id=chat_id, text=text)
                else:
                    telegramBot.sendMessage(chat_id=chat_id, text='Just send photo or /get it!')
            else:
                telegramBot.sendMessage(chat_id=chat_id, text='Just send photo or /get it!')

        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BotView, self).dispatch(request, *args, **kwargs)
