import os
from Output import Output
import sys
import base64
import requests
from time import time
from utils import read_more
import traceback
from BotRequests import ScriptsToExecute

# directory = os.path.dirname(sys.argv[0])
# os.chdir(directory)


def execute_scripts(driver):
    ScriptsToExecute.is_loading = True
    for script in ScriptsToExecute.scripts:
        try:
            driver.execute_script(script)
        except Exception as e:
            #traceback.print_stack()
            print('error', e)
            #print(script + ', Error while sending message: ', e)
    ScriptsToExecute.is_loading = False
    ScriptsToExecute.scripts = []


def load_functions(driver):
    for js_file in os.listdir('js_codes'):
        with open(f'js_codes/{js_file}') as code:
            driver.execute_script(code.read())


def send_message(chat_id, msg):
    if msg != '':
        msg = '%r' % msg
        msg = msg.replace(r'\r', r'\n')
        script = f"sendMsg2('{chat_id}', {msg})"
        while ScriptsToExecute.is_loading:  # Wait if is executing scripts
            pass
        ScriptsToExecute.scripts.append(script)


def send_media(chat_id, msg, image_url, msg_id=None,
               img_base64=None):

    if img_base64 is None:
        image_base64 = base64.b64encode(requests.get(image_url).content) \
                           .decode('utf-8')
    else:  # if provided base64 image, use that
        image_base64 = img_base64
    image_base64 = 'data:image/jpeg;base64,' + image_base64
    msg_id = 'null' if msg_id is None else f"'{msg_id}'"
    msg = '%r' % msg
    msg = msg.replace(r'\r', r'\n')
    script = f"send_media('{chat_id}', String.raw`{image_base64}`, " \
             f"{msg}, {msg_id})"
    #print(f'msg: {msg}')
    #print('\timage base64: ', image_base64)
    #print('\tchat_id:' + chat_id)
    #print('msg_id: ' + msg_id)
    #print('the send_media script=' + script)
    while ScriptsToExecute.is_loading:  # Wait if is executing scripts
        pass
    ScriptsToExecute.scripts.append(script)


def delete_message(driver, chat_id, msg):
    print('delete message from:' + msg)
    # Excluding new lines, bold
    msg = msg.strip('\n')
    msg = '%r' % msg
    script = f"deleteMessage('{chat_id}', {msg})"
    ScriptsToExecute.scripts.append(script)


def messages_generator():
    for chat in Output.output:
        for message in chat['messages']:
            yield chat, message


def wait_for_response_generator(time_limit):
    start = time()
    current = start
    while current - start < time_limit:
        for chat, cur_message in messages_generator():
            yield chat, cur_message
        current = time()


def can_make_element_choice(user_message, current_message, max_value):
    user_id = user_message['id']
    cur_text = current_message['message'].strip()
    cur_id = current_message['id']
    # if is the user who asked for the search, the message text is numeric, and
    # 1 <= message number <= max_value, send true, else false
    return user_id == cur_id and cur_text.isnumeric() and 1 <= int(
        cur_text) <= max_value


def send_choose_list(chat_id, q_type, time_limit, choose_list_str):
    choose_msg = f'Escolha o {q_type} a partir do número (Envie *"0"* para ' \
                 f'para cancelar)\n' \
                 f'Tempo limite: {time_limit}s\n' \
                 f'{read_more()}{choose_list_str}'
    send_message(chat_id, choose_msg)
    return choose_msg
