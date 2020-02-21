import requests
import re
from datetime import datetime
from js_caller import send_message, send_media
from utils import get_date_from_sec
from bot_help import get_help
from get_anilist_query import get_release_from_anime_q, get_anilist_api_url
from bot_image_list_related import get_list_image, BotImageElement
import threading

days_of_week = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']
dias_da_semana = ['segunda', 'terça', 'quarta',
                  'quinta', 'sexta', 'sábado', 'domingo']
bar = '*' + ('=-' * 9) + '*'


def command_release_manager(driver, chat, wpp_message):
    command = wpp_message['message']
    today_releases_pattern = re.compile(
        '!(semanal|lançamento|semana)\\s+'
        '(antes\\s+de\\s+ontem|anteontem|ontem|hoje'
        '|amanhã|amanha|depois\\s+de\\s+amanhã)$')
    anime_releases_pattern = re.compile(
        '!(semanal|lançamento|semana)\\s+(.+)')
    day_releases_pattern = re.compile(
        '!(semanal|lançamento|semana)\\s+'
        '(segunda|terça|terca|quarta|quinta|sexta|sabado|sábado|domingo)$')

    if day_releases_pattern.match(command):
        dia = day_releases_pattern.match(command).groups()[1]
        dia = dia.replace('terca', 'terça')
        dia = dia.replace('sabado', 'sábado')
        command_day_releases(driver, chat, dias_da_semana.index(dia),
                             wpp_message)
    elif today_releases_pattern.match(command):
        q_type = today_releases_pattern.match(command).groups()[1]
        command_today_releases(driver, chat, q_type, wpp_message)
    elif anime_releases_pattern.match(command):
        anime = anime_releases_pattern.match(command).groups()[1]
        command_anime_release(driver, chat, anime)
    else:
        # send_message(driver, chat['id'], help_semanal())
        get_help(driver, chat, '!semanal', wpp_message)


def get_day_results(page, results):
    q = get_release_from_anime_q()
    variables = {
        'page': page,
        'perPage': 50,
        'startDate_greater': 19000000,
        'format_in': ['TV', 'TV_SHORT', 'ONA']
    }
    result = requests.post(get_anilist_api_url(),
                           json={'query': q,
                                 'variables': variables}).json()
    results.extend(result['data']['Page']['media'])


def command_day_releases(driver, chat, week_day, wpp_message):
    send_message(chat['id'], 'Pesquisando lançamentos...')
    q = get_release_from_anime_q()
    variables = {
        'page': 1,
        'perPage': 50,
        'startDate_greater': 19000000,
        'format_in': ['TV', 'TV_SHORT', 'ONA']
    }
    result = requests.post(get_anilist_api_url(),
                           json={'query': q, 'variables': variables}).json()
    pages = result['data']['Page']['pageInfo']['lastPage']
    results = [result['data']['Page']['media'][0]]
    threads = [threading.Thread(target=get_day_results, args=[page, results])
               for page in range(2, pages)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    elements = []

    i = 1

    for anime_r in results:
        anime_title = anime_r["title"]["romaji"]
        airing_data = anime_r['nextAiringEpisode']
        image_url = anime_r['coverImage']['large']
        anime_info = ''
        if airing_data is None:
            continue
        # if will release
        air_at = airing_data['airingAt']
        air_remain = airing_data['timeUntilAiring']
        air_date = datetime.fromtimestamp(air_at)
        # if is the requested day and is less than a week needed
        if air_date.weekday() == week_day \
                and air_remain <= 7 * 24 * 60 * 60:
            episodes = anime_r['episodes']
            episode = airing_data["episode"]

            if air_remain < 60 * 60 * 24 \
                    or air_date.weekday() != datetime.today().weekday():
                anime_info += f'EP: {episode} / ' \
                              f'{"?" if episodes is None else episodes}\n'
            elif episode - 1 > 0:
                anime_info += f'Ep: {episode - 1} / ' \
                              f'{"?" if episodes is None else episodes}' \
                              f' (Lançado)\n'
            i += 1

            anime_info += f'Próximo Ep: {get_date_from_sec(air_remain)}'
            elements.append(BotImageElement(title=anime_title,
                                            image_info=anime_info,
                                            image_url=image_url))

    if len(elements) == 0:
        send_message(chat['id'], 'Nada encontrado')
    else:
        header_text = f'Episódios que lançam {dias_da_semana[week_day]}:'
        list_image = get_list_image(elements, header_text)
        send_media(chat['id'], f"*{header_text}*",
                   None, wpp_message['msg_id'], list_image)


def command_today_releases(driver, chat, q_type, wpp_message):
    weekday = datetime.today().weekday()
    q_type = re.sub('\\s+', ' ', q_type)
    today_dic = {'antes de ontem': (weekday - 2) % 7,
                 'anteontem': (weekday - 2) % 7,
                 'ontem': (weekday - 1) % 7,
                 'hoje': weekday,
                 'amanhã': (weekday + 1) % 7,
                 'amanha': (weekday + 1) % 7,
                 'depois de amanhã': (weekday + 2) % 7}
    command_day_releases(driver, chat, today_dic[q_type], wpp_message)


def command_anime_release(driver, chat, anime):
    # Starting searching using MyAnimeList because the searching engine is
    # way better, only get the 10 first results
    search_url = f'https://api.jikan.moe/v3/search/anime?page=1&q={anime}'
    search_results = requests.get(search_url).json()['results'][:10]
    mal_ids = []
    for mal_anime in search_results:
        mal_ids.append(mal_anime['mal_id'])

    # Querying with the mal_ids from the MAL search
    q = get_release_from_anime_q()
    variables = {
        'idMal_in': mal_ids,
        'page': 1,
        'perPage': 50
    }
    result = requests.post(get_anilist_api_url(),
                           json={'query': q, 'variables': variables}).json()
    s = ''
    for anime_r in result['data']['Page']['media']:
        anime_title = anime_r["title"]["romaji"]
        airing_data = anime_r['nextAiringEpisode']
        # If doesn't have a airing schedule, show release start date
        if airing_data is None:
            st_date = anime_r['startDate']
            d = st_date['day'] if st_date['day'] is not None else '?'
            m = st_date['month'] if st_date['month'] is not None else '?'
            y = st_date['year'] if st_date['year'] is not None else '?'
            dv = '28' if d == '?' else d
            mv = '12' if m == '?' else m
            yv = '3000' if y == '?' else y
            if datetime.strptime(
                    f'{dv}{mv}{yv}', '%d%m%Y') >= datetime.today():
                s += f'O anime *"{anime_title}"* ' \
                     f'não tem uma data de lançamento específica.\n' \
                     f'*Data mais próxima:* {d}/{m}/{y}\n\n'
            continue

        tua = get_date_from_sec(airing_data['timeUntilAiring'])
        air_datetime = datetime.fromtimestamp(airing_data['airingAt'])
        release_weekday_i = air_datetime.weekday()
        release_weekday = dias_da_semana[release_weekday_i]
        episodes = anime_r['episodes']
        s += f'*{anime_title}*\n'

        episode = airing_data["episode"]
        if 60 * 60 * 24 <= airing_data['timeUntilAiring'] <= 60 * 60 * 24 * 7 \
                and release_weekday_i == datetime.today().weekday():
            s += f'O episódio lança hoje! ep: {episode - 1}\n'
        s += f'*Próximo episódio: {episode}* / ' \
             f'{"?" if episodes is None else episodes}\n' \
             f'O próximo episódio será lançado daqui a ' \
             f'{tua}' \
             f' *({release_weekday})*\n\n'
    if s == '':
        send_message(chat['id'],
                     f'O anime "{anime}" não foi encontrado '
                     f'ou já foi finalizado.')
    else:
        send_message(chat['id'], s)
