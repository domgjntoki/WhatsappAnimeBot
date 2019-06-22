from js_caller import send_message
import re
from utils import read_more
from datetime import datetime, timedelta
import json
from utils import read_more
from bot_help import get_help
import os

person_pattern = re.compile('!contador\\s+@(\d+)')

def command_msg_count_manager(chat, driver, wpp_message, msgs_count):
    command = wpp_message['message']
    rank_pat = re.compile('!(contador\\s+rank|rank|ranking)\\s*(all|mes|mês|mensal|hoje|dia|diário|diario|semana|semanal)?$')

    if rank_pat.match(command):
        mode = rank_pat.match(command).groups()[1]
        command_msg_count_rank(chat, msgs_count, mode)
    elif command.startswith('!contador palavra'):
        command_words_count(chat, wpp_message, msgs_count)
    elif command.startswith('!contador help'):
        get_help(driver, chat, '!contador help', wpp_message)
    else:
        command_msg_count(chat, driver, wpp_message, msgs_count)


def command_words_count(chat, wpp_message, msgs_count):
    command = wpp_message['message']
    person_pattern = re.compile('!contador\\s+palavras\\s+@(\d+)')
    if person_pattern.match(command):
        contact_number = person_pattern.match(command).groups()[0]
    else:
        contact_number = wpp_message['id']
    messages = msgs_count[chat['contact']][contact_number]['messages']
    contact = msgs_count[chat['contact']][contact_number]['contact']
    
    word_counter = {}
    types_counter = {}
    times_counter = {}
    excluded_words = ['eles', 'elas', 'comigo', 'contigo', 'conosco', 
                      'convosco','lhes', 'você', 'voce', 'minha', 'mais',
                      'meus', 'minhas', 'teus', 'tuas', 'seus', 'suas', 
                      'nosso', 'nossa', 'nossos', 'nossas', 'vosso', 
                      'vossa', 'vossos', 'vossas', 'seus', 'suas', 
                      'mesmo', 'mesma', 'mesmos', 'mesmas', 'tais',  
                      'quem', 'qual', 'quais', 'quanto', 'quanta', 
                      'quantos', 'quantas', 'assim', 'então', 'logo', 
                      'pois', 'portanto', 'porque', 'pois', 'porquanto', 
                      'como', 'embora', 'conquanto', 'caso', 'quando'
                      'esses', 'essas', 'esse', 'essa', 'isso', 'isto']
    total_words = 0
    for message in messages:
        # counting types
        msg_type = '!comandos' if message['message'].startswith('!') else message['type']
        if msg_type in types_counter:
            types_counter[msg_type] += 1
        else: 
            types_counter[msg_type] = 1

        msg_txt = message['message']
        if msg_txt == '(Sem mensagem)': continue
        
        # gets all words and count them, includes pitch accents
        words = re.findall('[a-zA-ZáéíóúâêîôûãõüÁÉÍÓÚÂÊÎÔÛÃÕÜ]+', msg_txt)
        total_words += len(words)
        for word in words:
            word = word.lower()
            word = 'kkkk (e variantes)' if word == 'k' * len(word) else word
            if len(word) < 4 or (word in excluded_words): continue
            if word in word_counter:
                word_counter[word] += 1
            else:
                word_counter[word] = 1
                
        # couting hours
        date = datetime.strptime(message['time'], '%d/%m/%Y (%H:%M)')
        if date.hour in times_counter:
            times_counter[date.hour] += 1
        else:
            times_counter[date.hour] = 1
    ordered_words = sorted(word_counter.keys(), 
                          key= lambda x: word_counter[x], reverse=True)
    s = f'*Palavras mais usadas de {contact}:*'
    s += f'{read_more()}\n*Total:* {len(messages)}\n'
    chat_count = 1 if 'chat' not in types_counter else types_counter['chat']
    s += f'*Média de palavras {(total_words / chat_count):.2f} por mensagem*\n'
    for i, word in enumerate(ordered_words[:10], 1):
        s += f'*{i}. {word}* [{word_counter[word]}]\n'
        
    s += '\n*Tipos de mensagens e contagem:*\n'
    ordered_types = sorted(types_counter.keys(), 
                          key= lambda x: types_counter[x], reverse=True)
    for i, msg_type in enumerate(ordered_types, 1):
        s += f'*{i}. {msg_type}* [{types_counter[msg_type]}]\n'
        
    s += '\n*Horários e contagem:*\n'
    ordered_times = sorted(times_counter.keys(), 
                          key= lambda x: times_counter[x], reverse=True)
    for msg_time in ordered_times:
        s+= (f'*{msg_time:02}:00~{((msg_time + 1) % 24):02}:00-* '
             f'{times_counter[msg_time]}\n')
    send_message(chat['id'], s)
    pass


def reset_count(c, mode):
    mode_map = {'mês': 'month', 'mes': 'month', 'mensal': 'month',
                'dia':'day', 'diário':'day', 'diario': 'day', 'hoje': 'day',
                None: 'week', 'semana':'week', 'semanal':'week',
                'all': 'all'}
    mode = 'week' if mode not in mode_map else mode_map[mode]
    count = 0
    if mode == 'all':
        return c['count']
    td = datetime.today()
    without_hours = datetime(td.year, td.month, td.day) 
    for msg_obj in c['messages']:
        d = datetime.fromtimestamp(msg_obj['timestamp'])
        if mode == 'week' and d >= (without_hours - timedelta(days=td.weekday())):
            count += 1
        elif mode == 'month' and d >= (without_hours - timedelta(days=30)):
            count += 1
        elif mode == 'day' and d >= without_hours:
            count += 1
    return count
    
    
def command_msg_count_rank(chat, msgs_count, count_mode):
    print("mode of !rank: ", count_mode)
    contacts = msgs_count[chat['contact']]
    count_sorted = sorted([participant['id']
                           for participant in chat['participants']],
                          key=lambda x: reset_count(contacts[x], count_mode),
                          reverse=True)
    reset_day = 0
    ghost = '👻'
    total_count = 0
    rank_str = ''
    for i, contact_id in enumerate(count_sorted, 1):
        contact_info = contacts[contact_id]
        count = reset_count(contact_info, count_mode)
        rank_str += f'\t*{i}. {contact_info["contact"]} [{count}]*'
        if count < 100:
            rank_str += f' {ghost}'
            rank_str += f'\n  - Número: ({contact_id})'
            if count > 0:
                first_msg_date = contact_info['messages'][0]['time']
                rank_str += f'\n  - 1ª msg: {first_msg_date}'
        rank_str += '\n'
        total_count += count

    if chat['id'] == "559492596286-1468686780@g.us":  # Amigos Otakus
        warning = '*meta: 100 msgs*\n'
    else:
        warning = ''
    rank_str = f'Rank de mensagens (Total: ' \
               f'{total_count})\n{warning}{read_more()}{rank_str}'
    send_message(chat['id'], rank_str)


def command_msg_count(chat, driver, wpp_message, msgs_count):
    command = wpp_message['message']
    contacts = msgs_count[chat['contact']]
    number_choose_pat = re.compile('!contador\\s+(\\d+)\\s*(all|mes|mês|mensal|hoje|dia|diário|diario|semana|semanal)?$')
    person_pattern = re.compile('!contador\\s+@(\\d+)\\s*(all|mes|mês|hoje|dia|mensal|diário|diario|semana|semanal)?')
    default_pattern = re.compile('!contador\\s*(all|mes|mês|mensal|hoje|dia|diário|diario|semana|semanal)?')
    
    if number_choose_pat.match(command):
        mode = number_choose_pat.match(command).groups()[1]
    elif person_pattern.match(command):
        mode = person_pattern.match(command).groups()[1]
    elif default_pattern.match(command):
        mode = default_pattern.match(command).groups()[0]
    count_sorted = sorted([participant ['id'] 
                           for participant in chat['participants']],
                          key=lambda x: reset_count(contacts[x], mode),
                          reverse=True)

    if person_pattern.match(command):
        m_id = person_pattern.match(command).groups()[0]
        try:
            contact = contacts[m_id]
        except KeyError:
            send_message(chat['id'], f'Número "{m_id}" não encontrado')
            return
    elif number_choose_pat.match(command):
        n = int(number_choose_pat.match(command).groups()[0])
        try:
            if n - 1 < 0:
                raise IndexError('Go fuck yourself you fucking cunt')
            m_id = count_sorted[n - 1]
            contact = contacts[m_id]
        except IndexError:
            send_message(chat['id'], f'Número {n} fora de alcance')
            return
    elif default_pattern.match(command):
        contact = contacts[wpp_message['id']]
        m_id = wpp_message['id']
    contagem = f"{contact['contact']}, enquanto o bot esteve ligado," \
               f" escreveu {reset_count(contact, mode)} mensagens. " \
               f"({count_sorted.index(m_id) + 1}º lugar)" \
               f" "
    send_message(chat['id'], contagem)


def add_people_with_zero_msgs(chat, msg_count):
    chat_contact = chat['contact']
    for participant in chat["participants"]:
        if 'contact' not in participant.keys():
                participant['contact'] = 'Eu'
        if participant['id'] not in msg_count[chat_contact].keys():
            msg_count[chat_contact][participant['id']] = \
                {'contact': participant['contact'], 'count': 0,
                 'messages': []}
        # update all names
        msg_count[chat_contact][
            participant['id']]['contact'] = participant['contact']


def make_message_obj(msg):
    time = datetime.fromtimestamp(msg['timestamp'])
    msg_text = msg['message'].replace('\u200b', '')
    return {'message': msg_text,
            'time': time.strftime('%d/%m/%Y (%H:%M)'),
            'timestamp': msg['timestamp'],
            'type': msg['type']
            }


def save_messages(messages_count):
    print('saving messages...')
    with open('fonts/messages_count.json', 'r+') as json_file:
        a = json.load(json_file, strict=False)
        a.update(messages_count)
    # temporary file avoids data corruption
    with open('fonts/messages_count.json.temp', 'w+') as temp:
        temp.seek(0)
        json.dump(a, temp)
        temp.truncate()
    os.replace('fonts/messages_count.json.temp', 'fonts/messages_count.json')
    print('all messages were saved.')
                
               
def change_messages_count_obj(chat, msg, msg_count):
    if 'contact' not in msg.keys():
        msg['contact'] = 'Eu'
    if 'message' not in msg.keys():
        msg['message'] = '(Sem mensagem)'

    print(f"{msg['contact']} ({chat['contact']}): "
          f"{msg['message']}")
    chat_contact = chat['contact']
    if chat_contact in msg_count.keys():
        add_people_with_zero_msgs(chat, msg_count)
        if msg['id'] in msg_count[chat_contact].keys():
            msg_count[chat_contact][msg['id']][
                'count'] += 1
            msg_count[chat_contact][msg['id']][
                'messages'] \
                .append(make_message_obj(msg))
        else:
            msg_count[chat_contact][msg['id']] = \
                {'contact': msg['contact'], 'count': 1,
                 'messages': [make_message_obj(msg)]}
    else:
        add_msg = {'contact': msg['contact'], 'count': 1,
                   'messages': [make_message_obj(msg)]}
        msg_count[chat['contact']] = {}
        msg_count[chat['contact']][msg['id']] = add_msg
        add_people_with_zero_msgs(chat, msg_count)
