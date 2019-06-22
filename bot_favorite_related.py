import requests
import re
from js_caller import send_message, send_media
from bot_help import get_help
from bot_image_list_related import get_list_image, BotImageElement


def command_user_favorites(driver, chat, wpp_message):
    command = wpp_message['message']
    favorite_pattern = re.compile(
        '!favorit(e|o)\\s+(anime|manga|personagem)\\s+(.+)')
    if favorite_pattern.match(command):
        user = favorite_pattern.match(command).groups()[2]
        q_type = favorite_pattern.match(command).groups()[1]
        q_type = q_type.replace('personagem', 'characters')

        # If user is not found, send a warning
        response = requests.get("https://api.jikan.moe/v3/user/" + user)
        if response.status_code == 404:
            send_message(chat['id'],
                         f'O usuário "{user}" não foi encontrado.')
            return
        elif 'error' in response.json().keys():
            send_message(chat['id'],
                         f'Ocorreu um erro ao analisar'
                         f' *"{user}"*, verifique se o '
                         f'usuário está correto, ou sua conta está vazia.')
        elements = []
        favorites = response.json()['favorites']
        user = response.json()['username']

        s = f"{user}'s favorite {q_type}:"
        for i, anime in enumerate(favorites[q_type], 1):
            elements.append(BotImageElement(title=anime['name'],
                                            image_info=f'{i}',
                                            image_url=anime['image_url']))

        if len(elements) > 0:
            list_image = get_list_image(elements, s)
            send_media(chat['id'], s, None, wpp_message['msg_id'],
                       list_image)
        else:
            send_message(chat['id'], s)
    else:
        get_help(driver, chat, '!favorite', wpp_message)

  













