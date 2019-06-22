import requests
import re
from js_caller import send_message
from utils import read_more
from bot_help import help_top, get_help

translator = {'pop': 'bypopularity', 'novel': 'novels', 'temporada': 'airing',
              'pessoa': 'people', 'personagem': 'characters', 'filme': 'movie'}


def command_top_manager(driver, chat, wpp_message):
    command = wpp_message['message']
    top_general_pattern = re.compile('!top\\s+(anime|manga|pessoa|personagem)$')
    top_animes_specific_pattern = re.compile(
        '!top\\s+anime\\s+(temporada|filme|ova|tv|pop|favorite)')
    top_mangas_specific_pattern = re.compile(
        '!top\\s+(manga|mangá)\\s+(manga|novel|oneshot|manhwa|manhua|pop|favorite)')
    if top_general_pattern.match(command):
        c = top_general_pattern.match(command).groups()[0]
        req = translator[c] if c in translator.keys() else c
        command_get_top(driver, chat, f'{c.capitalize()} top', req)
    elif top_animes_specific_pattern.match(command):
        c = top_animes_specific_pattern.match(command).groups()[0]
        req = translator[c] if c in translator.keys() else c
        msg = 'Animes mais populares' \
            if c == 'pop' else 'Top animes da temporada'
        req = f'anime/1/{req}'
        print('Animes especfici pattern req: ' + req)
        command_get_top(driver, chat, msg, req)
    elif top_mangas_specific_pattern.match(command):
        c = top_mangas_specific_pattern.match(command).groups()[1]
        req = translator[c] if c in translator.keys() else c
        if c == 'pop':
            msg = 'Mangas mais populares'
        elif c in ['manga', 'novel', 'oneshot', 'manhwa', 'manhua']:
            msg = f'Top do tipo {c}'
        elif c == 'favorite':
            msg = 'Mangas mais favoritados'
        else:
            msg = 'wtf'
        req = f'manga/1/{req}'
        command_get_top(driver, chat, msg, req)
    else:
        # send_message(driver, chat['id'], help_top())
        get_help(driver, chat, '!top', wpp_message)


def command_get_top(driver, chat, msg, req):
    print(req)
    results = requests.get(f'https://api.jikan.moe/v3/top/{req}')\
        .json()['top']
    i = 1
    s = f'*{msg}:*\n'

    for e in results:
        try:
            s += f'\t*{i}. {e["title"]} [{e["type"]}]* {e["score"]}\n'
            if i == 10:
                s += read_more()
            i += 1
        except KeyError:
            s += f'\t*{i}. {e["title"]}*\n'
            if i == 10:
                s += read_more()
            i += 1

    send_message(chat['id'], s)
