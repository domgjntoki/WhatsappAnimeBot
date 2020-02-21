import re
import requests
from js_caller import send_message, send_media
from utils import read_more
from bot_help import get_help
from bot_image_list_related import get_list_image, BotImageElement


def command_list_manager(driver, chat, wpp_message):
    anime_list_pattern = re.compile(
        '!list(a)?\\s+anime\\s+(watching|completed|onhold|dropped|ptw)?\\s*(.+)')
    manga_list_pattern = re.compile(
        '!list(a)?\\s+manga\\s+(reading|completed|onhold|dropped|ptr)?\\s*(.+)')
    command = wpp_message['message']
    if anime_list_pattern.match(command):
        re_groups = anime_list_pattern.match(command).groups()
        user = re_groups[2]
        req = re_groups[1] if re_groups[1] is not None else 'watching'
        command_anime_manga_list(driver, chat, user, req, 'anime', wpp_message)
    elif manga_list_pattern.match(command):
        re_groups = manga_list_pattern.match(command).groups()
        user = re_groups[2]
        req = re_groups[1] if re_groups[1] is not None else 'reading'
        command_anime_manga_list(driver, chat, user, req, 'manga', wpp_message)
    else:
        # send_message(driver, chat['id'], help_list())
        get_help(driver, chat, '!list', wpp_message)


def command_anime_manga_list(driver, chat, user, q, q_type, wpp_message):
    response = requests.get(
        f'https://api.jikan.moe/v3/user/{user}/{q_type}list/{q}')
    if response.status_code == 400:
        send_message(chat['id'],
                     f'Ocorreu um erro ao pesquisar a lista do usuário '
                     f'*"{user}"* verifique se o nome está correto')
    results = response.json()[q_type]
    results = sorted(results, key=lambda k: k['score'], reverse=True)
    i = 1
    head = f"Continuação da lista de {q_type} {q} de *'{user}'*:\n"
    s = ''
    elements = []
    for e in results:
        title = e["title"]
        e_str = ''
        e_str += f'*{e["title"]}* '
        if q_type == 'manga':
            e_info = f'c.{e["read_chapters"]} v.{e["read_volumes"]}'
            e_str += f'*c.{e["read_chapters"]} v.{e["read_volumes"]}*'
        else:
            total_episodes = e['total_episodes']
            total_episodes = '?' if total_episodes == 0 else total_episodes
            e_info = f'Episodes: {e["watched_episodes"]}/{total_episodes}'
            e_str += f'_{e["watched_episodes"]} eps_'
        e_info += f'\nScore: {e["score"]}'
        elements.append(BotImageElement(title=title,
                                        image_info=e_info,
                                        image_url=e['image_url']))
        e_str += f' [ {e["score"]} ] \n'
        if i == 16:
            s += read_more()
        if i > 16:
            s += e_str
        i += 1
    # send_message(driver, chat['id'], s)
    if len(elements) > 0:
        header_text = f"lista de {q_type} {q} de '{user}':"
        list_image = get_list_image(elements[:16], header_text)
        send_media(chat['id'], image_url=None,
                   msg=head + s,
                   msg_id=wpp_message['msg_id'], img_base64=list_image)
    else:
        send_message(chat['id'],
                     f"Não há nada na lista de {q_type} {q} de *'{user}'*:\n")


