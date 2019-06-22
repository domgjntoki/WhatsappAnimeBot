from js_caller import *
from bot_anime_manga_perso_resume import anime_mange_perso_resume
from bot_help import get_help
import re
import traceback
import ast

type_conversion = {'anime': 'anime', 'manga': 'manga', 'mangá': 'manga',
                   'personagem': 'character'}


def command_anime_search(driver, chat, wpp_message):
    """Searches a anime in the MyAnimeList, and then messages with 10
        results to the user choose, after that wait for 25 seconds for
        the user response to show a anime

        :Args:
        - command: the bot command to do the search

    """
    command_ani_manga_perso_search(driver, chat, wpp_message, 'anime')


def command_manga_search(driver, chat, wpp_message):
    """Searches a manga in the MyAnimeList, and then messages with 10
        results to the user choose, after that wait for 25 seconds for
        the user response to show a manga

        :Args:
        - command: the bot command to do the search

    """
    command_ani_manga_perso_search(driver, chat, wpp_message, 'manga')


def command_character_search(driver, chat, wpp_message):
    """Searches a manga in the MyAnimeList, and then messages with 10
        results to the user choose, after that wait for 25 seconds for
        the user response to show a manga

        :Args:
        - command: the bot command to do the search

    """
    command_ani_manga_perso_search(driver, chat, wpp_message, 'personagem')


def command_ani_manga_perso_search(driver, chat, wpp_message, q_type):
    """Searches a anime, manga or person in the MyAnimeList, and returns
        a message with 10 results to the user choose in a time limit of 25s

        :Args:
        - command: the bot command to do the search
    """
    max_search_results = 20
    command = wpp_message['message']
    search_command_pattern = re.compile(f'![^\s]+\\s+(.+)')
    # if pattern doesn't matches, send a explanation
    if not search_command_pattern.match(command):
        # send_message(driver, chat['id'], help_anime_manga_personagem(q_type))
        get_help(driver, chat, f'!{q_type}', wpp_message)
        return

    search = search_command_pattern.match(command).groups()[0]
    print('requesting search of anime, manga, or character...')
    if type_conversion[q_type] == 'manga':
        r_str = (f'https://www.mangaupdates.com/series.html?'
                 f'output=jsonp&search={search}')
    else:
        r_str = f'https://api.jikan.moe/v3/search/' \
                 f'{type_conversion[q_type]}?' \
                 f'page=1&q={search}'
    try:  # try two times, max time 3 seconds.
        response = requests.get(r_str, timeout=3)
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as err:
        print('Too long, trying again...')
        response = requests.get(r_str)
    print('search request done.')
    if response.status_code == 404:
        send_message(chat['id'],
                     f'Nenhum resultado encontrado para "{search}"')
        return

    if type_conversion[q_type] != 'manga':
        results = response.json()['results']
    else:
        response_str = re.sub('callback\\((.+)\\);', r'\1', response.text)
        response_replace = {'null': 'None', 'false': 'False', 'true': 'True'}
        for k, v in response_replace.items():
            response_str = response_str.replace(k, v)
        search_result = ast.literal_eval(response_str.strip())
        results = search_result['results']['items']

    if len(results) == 0:  # if not results:
        no_result_warning = f'Nenhum {q_type} com nome "{search}" foi encontrado.'
        send_message(chat['id'], no_result_warning)
        return

    # Sending results...
    if type_conversion[q_type] == 'manga':
        search_list = get_search_results(
            q_type, results[:max_search_results], id_type='id')
    else:
        search_list = get_search_results(q_type, results[:max_search_results])
    search_results_str = search_list[0]
    mal_ids = search_list[1]

    time_limit = 60
    choose_msg = send_choose_list(chat_id=chat['id'],
                                  q_type=q_type, time_limit=time_limit,
                                  choose_list_str=search_results_str)
    for cur_chat, cur_message in wait_for_response_generator(time_limit):
        try:
            msg = cur_message['message']
            if can_make_element_choice(wpp_message, cur_message, len(mal_ids)):
                search_id = str(mal_ids[int(msg) - 1])
                print('requesting anime, manga, or character...')
                ma_response = anime_mange_perso_resume(
                    search_id, type_conversion[q_type])
                print('anime, manga or character request done.')

                # Delete the list search results and send the chosen anime
                send_media(chat['id'], msg=ma_response[0],
                           image_url=ma_response[1],
                           msg_id=wpp_message['msg_id'])
                delete_message(driver, cur_chat['id'], choose_msg)
                return
            elif msg.lower() == '0' and cur_message['id'] == wpp_message['id']:
                delete_message(driver, cur_chat['id'], choose_msg)
                return
        except Exception as e:
            print('exception in anime manga related', e)
            traceback.print_exc()
            pass

    send_message(chat['id'], 'Tempo terminado.')
    delete_message(driver, chat['id'], choose_msg)


def get_search_results(q_type, results, id_type='mal_id'):
    s = ''
    media_ids = []
    for i, anime_q in enumerate(results, 1):
        ma_id = anime_q[id_type]
        ma_title = anime_q['title' if q_type != 'personagem' else 'name']

        if q_type == 'anime':
            ma_type = anime_q['type']
            s += f'[{i:02d}] - {ma_title} [{ma_type}]\n'
        elif q_type == 'manga':
            s += f'[{i:02d}] - {ma_title}\n'
        else:
            animes_size_t = len(anime_q['anime'])
            media_t = 'manga' if animes_size_t == 0 else 'anime'
            media = anime_q[media_t][0]['name']
            s += f'[{i:02d}] - {ma_title} *[{media}]*\n'
        media_ids.append(ma_id)
    return [s, media_ids]
