from django.shortcuts import render

from user_auth.decorators import if_logged

import lang_parser

import json
import os


# Create your views here.
@if_logged
def info(request, lang):
    with open(os.path.join(os.path.dirname(__file__), f'lang/{lang}/info.json'), "r", encoding='utf-8') as f:
        data = json.load(f)
    print(data['about_game_header'])
    data = lang_parser.format_data(data)
    print(data)
    with open('log.txt', 'w') as f:
        f.write(str(data))
    return render(request, 'info/info.html', {'lang_data': data})
