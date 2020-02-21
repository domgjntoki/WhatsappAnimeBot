import requests
import uuid
import re
import threading
from utils import read_more, get_datetime_from_format, translate
from bot_character_resume import character_resume
from bs4 import BeautifulSoup as Bs



def get_json_result(key, url, json_result):
        json_result[key] = requests.get(url)
    
    
def anime_mange_perso_resume(id, q_type):
    if q_type == 'anime':
        return anime_resume(id, q_type)
    elif q_type == 'manga':
        return manga_resume(id)
    elif q_type == 'character':
        return character_resume(id)


def manga_resume(id):
    url = f'https://www.mangaupdates.com/series.html?id={id}'

    manga_req = requests.get(url, 
        cookies={'secure_session': 'db0554f45387ac8e677e3d37b4de4587'})
    soup = Bs(manga_req.content, 'html.parser')

    target_dict = {'description': 0, 'type': 1, 'releases': 5, 'status': 6,
                   'animeend': 8, 'rating': 11, 'image': 13, 'genres': 14,
                   'author': 18, 'artist': 19, 'year': 20, 'publisher': 21,
                   'serialization': 22}
    all_containers = soup.select('div[class=sContent]')

    title = soup.select_one("span[class='releasestitle tabletitle']").text

    description = soup.select_one(
        "div[id='div_desc_more']")

    if description is None:  # if does not have "More..."
        description = all_containers[0]
    description = str(description).replace('<br/>', '\n')
    description = re.sub('<.+>', '', description)

    anime_end = all_containers[target_dict['animeend']]
    anime_end = str(anime_end).replace('<br/>', '\n')
    anime_end = re.sub('(Starts at|Ends at)', r'*\1*', anime_end)
    anime_end = re.sub('<.+>', '', anime_end)

    genre_container = all_containers[target_dict['genres']]
    genres = [genre.text for genre in genre_container.select('a')][:-1]

    rating_info = all_containers[target_dict['rating']].text
    rating = re.findall('Bayesian Average: (\d+.?\\d+)', rating_info)
    rating = '?' if len(rating) == 0 else rating[0]

    latest_releases = all_containers[target_dict['releases']].text.split('ago')[
                      :-1]
    latest_releases = [release + ' ago' for release in latest_releases]

    manga_type = all_containers[target_dict['type']].text.replace('\n', '')
    status = all_containers[target_dict['status']].text.replace('\n', '')

    author = all_containers[target_dict['author']].text.replace('\n', '')
    artist = all_containers[target_dict['artist']].text.replace('\n', '')
    year = all_containers[target_dict['year']].text.replace('\n', '')
    publisher = all_containers[target_dict['publisher']].text.replace('\n', '')
    serialization = all_containers[
        target_dict['serialization']].text.replace('\n', '')

    image_url = all_containers[target_dict['image']].find('img')['src']

    bar = "*====================*"
    latest_releases_str = '\n'.join(latest_releases)
    
    genres_str = ", ".join(genres)
    description_en = description
    genres_str, latest_releases_str, description = translate(
        genres_str, latest_releases_str, description)
    s = (f'*{title.upper()} [{manga_type}]*\n\n'
         f'*{genres_str.title()}*\n'
         f'{bar}\n'
         f'*Nota:* {rating}\n'
         f'*Status:* {status}\n'
         f'*Autor:* {author} *|* *Artist:* {artist}\n'
         f'*Editora:* {publisher}\n'
         f'*Serialização:* {serialization}\n'
         f'*Ano:* {year}\n'
         f'{bar}\n'
         f'*Informações de Lançamento: {read_more()}*\n'
         f'*Últimos lançamentos:*\n'
         f'{latest_releases_str}\n\n'
         f'*Capítulo Inicial/Final do anime:*\n'
         f'{anime_end}'
         f'{bar}\n'
         f'*Sinopse:*{description}\n\n'
         f'*Synopsis(English):*{read_more()}{description_en}')
    return [s, image_url]


def anime_resume(id, q_type):
    url = f'https://api.jikan.moe/v3/{q_type}/{id}'
    characters_staff = None
    if q_type == 'manga':
        response = requests \
            .get(f'https://api.jikan.moe/v3/{q_type}/{id}')
        search_result = response.json()
    else:  # Making image with characters and getting staff info
        json_result = {}
        thread1 = threading.Thread(target=get_json_result,
                                   args=['anime', url, json_result])
        thread2 = threading.Thread(
            target=get_json_result,
            args=['characters_staff', f'{url}/characters_staff', json_result])
        threads = [thread1, thread2]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        search_result = json_result['anime'].json()
        characters_staff = json_result['characters_staff'].json()

    bar = "===================="

    s = ""

    ma_name = search_result["title"]
    ma_type = search_result["type"]

    ma_score = search_result["score"]
    ma_rank = search_result["rank"]
    ma_popular = search_result["popularity"]
    ma_status = search_result["status"]
    ma_synopsis = search_result["synopsis"]
    ma_genre = search_result["genres"]
    ma_ep_chap = search_result[
        "episodes" if q_type == 'anime' else 'chapters']
    ma_publisher = search_result[
        "studios" if q_type == 'anime' else 'serializations']
    ma_rating = '' if q_type == 'manga' else f'_{search_result["rating"]}_'

    # Formating release dates
    ma_pub_date = search_result['aired' if q_type == 'anime' else 'published']
    ma_pub_from = get_datetime_from_format(ma_pub_date['from'])
    ma_pub_to = get_datetime_from_format(ma_pub_date['to'])
    from_formatted = '?' if ma_pub_from is None \
        else ma_pub_from.strftime('%b %d, %Y')
    to_formatted = '?' if ma_pub_to is None \
        else ma_pub_to.strftime('%b %d, %Y')

    # Mangas has chapters and volumes, and animes episodes
    if q_type == 'anime':
        ep_or_chap = \
            f'*Episódios:* {"?" if ma_ep_chap is None else ma_ep_chap}'
    else:
        m_volumes = search_result["volumes"]
        ep_or_chap = \
            f'*Chapters:* {"?" if ma_ep_chap is None else ma_ep_chap} ' \
            f'*Volumes:* {"?" if  m_volumes is None else m_volumes}'

    #translating
    genres = get_formatted_list(ma_genre)
    ma_synopsis_en = ma_synopsis
    genres, ma_rating, ma_synopsis, from_formatted, to_formatted  = translate(
        genres, ma_rating, ma_synopsis, from_formatted, to_formatted)
    title = f'*{ma_name.upper()} [{ma_type}]* #{ma_rank}\n' \
            f'{ma_rating }\n*{genres.title()}*\n'
            
    data = f'*Nota:* {ma_score} | *Popularidade:* {ma_popular}\n' \
           f'*Status:* {ma_status}.\n' \
           f'{ep_or_chap}\n' \
           f'*{"Estúdios" if q_type == "anime" else "Serialization"}:* ' \
           f'{get_formatted_list(ma_publisher)}\n' \
           f'*Lançamento:* De {from_formatted} até {to_formatted}\n'

    # if has directors and staff, add it to data
    if characters_staff is not None:
        directors = []
        if 'staff' in characters_staff:
            for person in characters_staff['staff']:
                if person["positions"] == ['Director']:
                    directors.append(f'*[{person["name"]}]*')
            if len(directors) > 0:
                data += f'*Diretores:* {" | ".join(directors)}\n'

    synopsis = (f'*Sinopse:* {read_more()}{ma_synopsis}\n\n'
                f'*Synopsis(English):*{read_more()}{ma_synopsis_en}')

    s += f'{title}*{bar}*\n{data}\n*{bar}*\n{synopsis}'
    is_hentai = 'hentai' in get_formatted_list(ma_genre).lower()
    ma_image = search_result["image_url"]
    if is_hentai:
        s = 'Foto censurada por ser hentai\n' + s
        ma_image = 'http://i.imgur.com/CIVQZRd.png'
    return [s, ma_image]


def get_formatted_list(anime_list):
    names = []
    for d in anime_list:
        names.append(d['name'])
    return ', '.join(names) + '.'
