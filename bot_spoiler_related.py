import re
from js_caller import send_message
from utils import read_more


def command_spoiler(chat, wpp_message):
    spoiler_pattern = re.compile('!spoiler\s+([^/|]+)[/|](.+)')
    command = wpp_message['message']
    if 'contact' not in wpp_message.keys():
        wpp_message['contact'] = 'Eu'
    if spoiler_pattern.match(command):
        spoiler_data = spoiler_pattern.match(command).groups()
        spoiler_warning = spoiler_data[0].strip()
        spoiler_content = spoiler_data[1].strip()
        send_message(chat['id'],
                     f'*[SPOILER {spoiler_warning}]* ({wpp_message["contact"]})'
                     f'{read_more()}\n\n\n{spoiler_content}')
