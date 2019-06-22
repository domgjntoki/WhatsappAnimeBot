import requests
from utils import read_more
import re


def character_resume(q_id):
    response = requests.get(f'https://api.jikan.moe/v3/character/{q_id}')
    character_info = response.json()
    name = character_info['name']
    name_kanji = character_info['name_kanji']
    nicknames = character_info['nicknames']
    nicknames_f = 'N/A' if len(nicknames) == 0 else ', '.join(nicknames)
    about = character_info['about']
    member_favorites = character_info['member_favorites']
    image_url = character_info['image_url']
    animeography = character_info['animeography']
    animes = []
    for anime in animeography:
        animes.append(anime['name'])
    voice_actors = character_info['voice_actors']
    japanese_va = ''
    for voice_actor in voice_actors:
        if voice_actor['language'].lower() == 'japanese':
            japanese_va = voice_actor['name']

    animes_formatted = f'*Animes:* '
    if len(animes) <= 4:  # If has up to 4 elements, do this
        animes_formatted += ' *|* ' .join(animes)
    else:  # If not, put a read_more string between the forth and fifth element
        animes_formatted += " *|* ".join(animes[:4]) + read_more() + " *|* " \
                            " *|* ".join(animes[:4])
    about = re.sub('\n([^:(\n]+:)', r'*\1*', '\n' + about)
    s = f'*{name} [{name_kanji}]* ({member_favorites} favorites)\n' \
        f'*Nicknames:* {nicknames_f}\n' \
        f'*Voice Actor:* {japanese_va}\n' \
        + animes_formatted + '\n' +\
        f'*About:* {read_more()} \n{about}'
    return [s, image_url]

