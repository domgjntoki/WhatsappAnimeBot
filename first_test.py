import json
import os
import threading
from bot_message_related import change_messages_count_obj, save_messages
from selenium import webdriver
import sys
import js_caller
from Output import Output
from bot_caller import make_call
from BotRequests import ScriptsToExecute
import traceback

print('starting program...')
#directory = os.path.dirname(sys.argv[0])
#directory = r'/home/pi/Desktop/WppBot'
#os.chdir(directory)

messages_count = json.loads(open('fonts/messages_count.json').read(),
                            strict=False)

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument(r'user-data-dir=browser_data')
# Whatsapp requires chrome version to be 36+, 
# this user agent is only a workaround
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
driver = webdriver.Chrome(chrome_options=options)

print('driver done...')
driver.get(r'https://web.whatsapp.com/')
# input("If already done QR Code, hit enter: ")
print("loading functions...")
js_caller.load_functions(driver)


first_time = True

i = 1
while True:
    try:
        str_output = str(driver.execute_script('return getUnreadChats();'))
        Output.output = json.loads(str_output)
        # execute all requests, one after another, because selenium is not
        # thread safe.
        if len(ScriptsToExecute.scripts) > 0:
            js_caller.execute_scripts(driver)
        for chat, message in js_caller.messages_generator():
            change_messages_count_obj(chat, message, messages_count)
            if not first_time:
                threading.Thread(
                    target=make_call,
                    args=[driver, chat, message, messages_count]).start()
            else:
                first_time = False
        if i % 10_000 == 0:  # save messages after 10k loops
            i = 1
            threading.Thread(
                    target=save_messages, args=[messages_count]).start()

        i += 1
    except Exception as e:
        traceback.print_stack()
        js_caller.load_functions(driver)
        print('\n', e)
