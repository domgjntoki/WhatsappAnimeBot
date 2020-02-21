from js_caller import send_media


def command_monogatari_order(driver, chat, wpp_message):
    send_media(chat['id'], "*ORDEM DE LANÇAMENTO DE MONOGATARI* "
                                   "(Leia a nota embaixo)",
               "https://i.imgur.com/HCCSjix.jpg", wpp_message['msg_id'])
