import requests
import re
from js_caller import send_message, send_media
from bot_help import help_user, get_help
from utils import read_more


def command_user_manager(driver, chat, wpp_message):
    command = wpp_message['message']
    user_profile_pattern = re.compile('!user\\s+(perfil\\s+)?(.+)')
    user_history_pattern = re.compile('!user\\s+(historico|histórico)\\s+(.+)')
    if user_history_pattern.match(command):
        user = user_history_pattern.match(command).groups()[1]
        send_message(chat['id'], command_user_history(user))
    elif user_profile_pattern.match(command):
        user = user_profile_pattern.match(command).groups()[1]
        user_profile = command_user_profile(user)
        # If the user does not have a photo
        if user_profile[1] is not None:
            send_media(chat['id'], user_profile[0], user_profile[1],
                       wpp_message['msg_id'])
        else:
            send_message(chat['id'], user_profile[0])
    else:  # if command if incorrect, send explanation
        # send_message(driver, chat['id'], help_user())
        get_help(driver, chat, '!user', wpp_message)


def command_user_history(user):
    response = requests.get(f'https://api.jikan.moe/v3/user/{user}/history')
    search_result = response.json()

    # read_more_str = "\u200b" * 4000
    str_header = f"{user}'s history:\n"
    str_result = str_header + '=' * len(str_header) + '\n' + read_more() + '\n'

    i = 1
    limit = 10
    for hist_element in search_result['history']:
        meta_element = hist_element['meta']
        element_type = meta_element['type']
        element_title = meta_element['name']
        element_increment = hist_element['increment']

        str_result += f'{element_title} {element_increment} [{element_type}]\n'
        i += 1
        if i > limit:
            break
    return str_result


def command_user_profile(user):
    response = requests.get("https://api.jikan.moe/v3/user/" + user)

    if response.status_code == 404:  # if user does not exist
        return [f'O usuário "{user}" não foi encontrado.', None]
    elif 'error' in response.json().keys():
        return [f'Ocorreu um erro ao analisar' 
                f' *"{user}"*, verifique se o ' 
                f'usuário está correto, ou sua conta está vazia.', None]
    stats = response.json()
    name = stats['username']
    user_url = stats['url']
    anime_stats = stats["anime_stats"]
    manga_stats = stats["manga_stats"]

    final_str = f"User: {user_url}\n"
    final_str += f"\n*Anime Stats ({anime_stats['total_entries']} entries):*\n"
    final_str += build_str(anime_stats)
    final_str += f"\n\n*Manga Stats ({manga_stats['total_entries']} " \
                 f"entries):*{read_more()}\n"
    final_str += build_str(manga_stats)

    return [final_str, stats['image_url']]


def build_str(stats):
    stats_list = []
    for key, value in stats.items():
        key = 'days' if key.startswith('days') else key
        stats_list.append(f"*{key.capitalize()}:* {value}")

    spacer = " | "

    top = [f"{stats_list[1]}{spacer}{stats_list[0]}\n"]

    # max length with + 3 to be more legible
    max_length_mid = max([len(stats) + 3 for stats in stats_list[2:5]])
    mid = []
    mid_build = {2: 4, 3: 6, 5: 8}
    for x1, x2 in mid_build.items():
        spaces = " " * (max_length_mid - len(stats_list[x1]))
        mid.append(f"{stats_list[x1]}{spaces}{spacer}"
                   f"{stats_list[x2]}\n")

    bot = [f'{stats}\n' for stats in stats_list[9:]]

    bar = ("-" * 52) + "\n"

    final_list = [''.join(part_list) for part_list in [top, mid, bot]]
    return f"{bar}".join(final_list).replace('_', ' ')
