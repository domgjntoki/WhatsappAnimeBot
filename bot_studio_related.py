import requests
import re
from get_anilist_query import get_studio_search_q, get_anilist_api_url
from js_caller import send_message, send_choose_list, send_media, \
    wait_for_response_generator, can_make_element_choice, delete_message
from bot_image_list_related import get_list_image, BotImageElement


def command_search_studio(driver, chat, wpp_message):
    studio_pattern = re.compile('!(estúdio|estudio)\\s+(.+)')
    studio_name = studio_pattern.match(wpp_message['message']).groups()[1]
    q = get_studio_search_q()
    variables = {
        'search': studio_name,
        'page': 1,
        'perPage': 50
    }
    results = requests.post(get_anilist_api_url(),
                            json={'query': q, 'variables': variables}).json()
    studio_results = results['data']['Page']['studios']
    total_results = len(studio_results)
    studio = None
    if total_results == 0:  # No results, send warning and that's it
        send_message(chat['id'],
                     f'Estúdio {studio_name} não encontrado.')
        return
    elif total_results == 1:  # Don't need to choose, only one option
        studio = studio_results[0]
    else:  # send a list to choose a studio
        choose_list_str = ''
        time_limit = 30
        i = 1
        for studio_result in studio_results[:20]:
            choose_list_str += f'*[{i:02}] {studio_result["name"]}*\n'
            i += 1
        choose_msg = send_choose_list(chat_id=chat['id'],
                                      q_type='estúdio',
                                      choose_list_str=choose_list_str,
                                      time_limit=time_limit)
        for cur_chat, cur_message in wait_for_response_generator(time_limit):
            msg = cur_message['message']
            if can_make_element_choice(wpp_message, cur_message, max_value=i):
                studio = studio_results[int(msg) - 1]
                delete_message(driver, chat['id'], choose_msg)
                break
            elif msg == '0':  # cancel sentinel
                delete_message(driver, chat['id'], choose_msg)
                return

        if studio is None:  # Did not send any value
            send_message(chat['id'], 'Tempo terminado.')
            delete_message(driver, chat['id'], msg=choose_msg)
            return

    animes = []
    for anime in studio['media']['nodes'][:25]:
        anime_info = f'Ano: {anime["startDate"]["year"]}\n' \
                     f'Tipo: {anime["format"]}'
        animes.append(BotImageElement(title=anime['title']['romaji'],
                                      image_info=anime_info,
                                      image_url=anime['coverImage']['large']))
    studio_image_result = get_list_image(animes, studio['name'])
    send_media(chat['id'], msg=f'*Estúdio {studio["name"]}*',
               img_base64=studio_image_result, msg_id=wpp_message['msg_id'],
               image_url=None)
