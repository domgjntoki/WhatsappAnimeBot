from bot_help import command_help
from bot_anime_manga_related import command_anime_search, command_manga_search, \
    command_character_search
from bot_user_related import command_user_manager
from bot_favorite_related import command_user_favorites
from bot_release_related import command_release_manager
from bot_top_related import command_top_manager
from bot_monogatari_order import command_monogatari_order
from bot_list_related import command_list_manager
from bot_message_related import command_msg_count_manager, \
    command_msg_count_rank
from bot_system_related import command_measure_temp
from bot_studio_related import command_search_studio
from js_caller import send_message
import re
from time import time
from bot_spoiler_related import command_spoiler


wait_rank = 900


class Last:
    last = {}


def make_call(driver, chat, wpp_message, msgs_count):
    """Sends the response message to a command, if there is one

         :Args:
         - driver: The webdriver to execute the JS scrips
         - chat: the chat to send the message
         - message: the message send by the user

         :Usage:
             chat = Output.output[0]
             message = chat['messages'][0]
             threading.Thread(
                 target=make_call, args=[driver, chat, message]).start()
    """

    wpp_message['message'] = wpp_message['message'].strip().lower()

    # stripping spaces after !
    wpp_message['message'] = \
        re.sub('!\\s+(.+)', r'!\1', wpp_message['message'])

    command = wpp_message['message']
    if command == '!help':
        command_help(driver, chat, wpp_message)
    elif command.startswith('!anime'):
        command_anime_search(driver, chat, wpp_message)
    elif command.startswith('!manga') or command.startswith('!mangá'):
        command_manga_search(driver, chat, wpp_message)
    elif command.startswith('!personagem'):
        command_character_search(driver, chat, wpp_message)
    elif command.startswith('!estúdio') or command.startswith('estúdio'):
        command_search_studio(driver, chat, wpp_message)
    elif command.startswith('!user'):
        command_user_manager(driver, chat, wpp_message)
    elif command.startswith('!favorit'):
        command_user_favorites(driver, chat, wpp_message)
    elif command.startswith('!semana') or command.startswith('!lançamento'):
        command_release_manager(driver, chat, wpp_message)
    elif command.startswith('!top'):
        command_top_manager(driver, chat, wpp_message)
    elif command == '!monogatari':
        command_monogatari_order(driver, chat, wpp_message)
    elif command.startswith('!list'):
        command_list_manager(driver, chat, wpp_message)
    elif command.startswith('!spoiler'):
        command_spoiler(chat, wpp_message)
    elif command == '!temp':
        command_measure_temp(chat)
    elif command.startswith('!rank') or command.startswith("!contador rank"):
        print(Last.last)
        if chat['id'] in Last.last.keys() and command not in Last.last[chat['id']]:
            print('iffffffff')
            Last.last[chat['id']][command] = time() - wait_rank - 1
        elif chat['id'] not in Last.last:
            print('elseeeeee')
            Last.last[chat['id']] = {}
            Last.last[chat['id']][command] = time() - wait_rank - 1

        time_passed = time() - Last.last[chat['id']][command]

        if time_passed > wait_rank:
            command_msg_count_manager(chat, driver, wpp_message, msgs_count)
            Last.last[chat['id']][command] = time()
        else:
            remain = wait_rank - time_passed
            mn = remain // 60
            sec = remain % 60
            send_message(chat['id'],
                         f'Espere *{mn:.0f} min* e *{sec:.0f}s* para'
                         f' usar !rank novamente nesse chat (15 em 15 min)')
    elif command.startswith('!contador'):
        command_msg_count_manager(chat, driver, wpp_message, msgs_count)
