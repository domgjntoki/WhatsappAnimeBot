from js_caller import send_message, send_media
from utils import read_more


def command_help(driver, chat, wpp_message):
    """Return all the commands and their descriptions"""
    # get_help(driver, chat, '!help', wpp_message)
    send_message(chat['id'],
        'MyAnimeList bot help\n' +
        '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n' + read_more() + '\n' +
        bot_help() + help_anime() + help_manga() + help_personagem() +
        help_studio() + help_monogatari() +
        '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n'
        '*[ !contador* _help_ *]* – Mostra todos os comandos relacionados ao '
        'contador de mensagens e ranks.\n'
        '*[ !user ]* - Mostra comandos relacionados ao perfil do usuário'
        '\n*[ !favorite ]* - Mostra os comandos que mostra os favoritos de um '
        'usuário no MAL\n'
        '*[ !list ]* - Mostra comandos relacionados às listas de usuários do '
       'MAL\n'
        '*[ !semanal ]* - Mostra todos os comandos relacionados a '
       'lançamentos de animes na semana\n'
       '*[ !top ]* - Mostra todos os comandos que mostram os tops do '
        'MyAnimeList, inclusive os top animes da temporada\n')


def get_help(driver, chat, command, wpp_message):
    command_images = {'!help': 'https://i.imgur.com/z0jszVU.jpg',
                      '!anime': 'https://i.imgur.com/PKafjRh.jpg',
                      '!manga': 'https://i.imgur.com/PKafjRh.jpg',
                      '!personagem': 'https://i.imgur.com/PKafjRh.jpg',
                      '!user': 'https://i.imgur.com/ltn22CN.jpg',
                      '!favorite': 'https://i.imgur.com/Im9bfDv.jpg',
                      '!semanal': 'https://i.imgur.com/z49Y0Py.jpg',
                      '!semana': 'https://i.imgur.com/z49Y0Py.jpg',
                      '!lançamento': 'https://i.imgur.com/z49Y0Py.jpg',
                      '!top': 'https://i.imgur.com/3FenYzv.jpg',
                      '!list': 'https://i.imgur.com/fTmzOOA.jpg', 
                      '!contador help': 'https://i.imgur.com/aKmxapP.png'
                      }
    img = command_images[command]
    if command == '!help':
        send_media(chat['id'], '*Todos os comandos:*', img,
                   wpp_message['msg_id'])
    else:
        send_media(chat['id'], f'*Comandos do tipo {command}:*', img,
                   wpp_message['msg_id'])


def bot_help():
    return '*[ !help ]* - Mostra todos os comandos disponíveis no bot\n'



def help_anime_manga_personagem(q_type):
    return f'*[ !{q_type}* _título_ *]* - Busca por um {q_type} no MyAnimeList\n' \
           f'>> _!{q_type} ' \
           f'{"Shingeki no Kyojin" if q_type != "personagem" else "Rem"}_\n'


def help_studio():
    return ('*[ !estúdio* _nome_ *]* – Busca por um estúdio no AniList\n'
            '>> _!estúdio Kyoto Animation_\n')

def help_monogatari():
    return "*[ !monogatari ]* Mostra ordem das temporadas de monogatari\n"


def help_anime():
    return help_anime_manga_personagem('anime')


def help_manga():
    return help_anime_manga_personagem('manga')


def help_personagem():
    return help_anime_manga_personagem('personagem')


def help_user():
    return '*[ !user* _usuário_ *]* - Mostra o perfil do MAL do usuário\n' \
           '>> _!user AltrianZ_\n' \
           '*[ !user perfil* _usuário_ *]* - Mostra o perfil do MAL do usuário\n' \
           '>> _!user perfil AltrianZ_\n' \
           '*[ !user historico* _usuário_ *]* - Mostra histórico de update do usuário\n' \
           '>> _!user historico Yamashine_\n'


def help_favorite():
    return '*[ !favorite anime* _usuário_ *]* - Mostra os animes favoritos do usuário\n' + \
           '>> _!favorite anime DomGintoki_\n' \
           '*[ !favorite manga* _usuário_ *]* - Mostra os mangas favoritos do usuário\n' \
           '*[ !favorite personagem* _usuário_ *]* - Mostra os personagens favoritos do usuário\n'


def help_semanal():
    return '*[ !semanal hoje ]* - Mostra todos os animes que lançam hoje\n' \
           '*[ !semanal* dia *]* - Mostra todos animes lançados nesse dia\n' \
           '>> _!semanal segunda_\n' \
           '*[ !semanal* anime *]* - Mostra em que dia da semana e a data de ' \
           'lançamento do anime\n'


def help_top():
    return '\nComandos do tipo *!top*:\n' \
           '*Geral:* *[ !top* tipo *]*\n' \
           '\t*tipos =* _anime, manga, pessoa, personagem_\n' \
           '\t_>> !top anime, !top manga..._\n' \
           f'\t\n*Tops anime especificado:*\n{read_more()}' \
           '*[ !top anime* tipo *]*\n' \
           '\t*tipos =* _temporada, tv, filme, ova, pop, favorite_\n' \
           '\t_>> !top anime temporada, !top anime pop..._\n' \
           '\t\n*Top manga especificado:*\n' \
           '*[ !top manga* tipo *]*\n' \
           '\t*tipos =* _manga, novel, oneshot, manhwa, manhua, pop, favorite_\n' \
           '\t_>> !top manga manga, !top manga novel, !top manga manhwa..._\n'


def help_list():
    return 'Comandos do tipo *!list*:\n' \
           '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n' \
           f'{read_more()}\n' \
           '*Anime: ====================*\n' \
           '\t*[ !list anime tipo* usuário *]*\n' \
           '\t*tipos =* _watching, completed, onhold, dropped, ptw_\n' \
           '\t*EX:*' \
           '\t_>> !list anime dropped DomGintoki, !list anime ptw DomGintoki_\n' \
           '\t*_OBS: se não informar o tipo, a lista_*\n' \
           '\t*_"watching" é mostrada por padrão_* _(!list anime DomGintoki)_\n' \
           '\n*Manga: ====================*\n' \
           '\t*[ !list manga tipo* usuário *]*\n' \
           '\t*tipos =* _reading, completed, onhold, dropped, ptr_\n' \
           '\t*EX:*\n' \
           '\t_>> !list manga completed DomGintoki, !list manga ptr DomGintoki_\n' \
           '\t*_OBS: se não informar o tipo, a lista_*\n' \
           '\t*_"reading" é mostrada por padrão_* _(!list manga DomGintoki)_\n' \
           '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'

