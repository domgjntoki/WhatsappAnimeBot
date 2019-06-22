import os
from js_caller import send_message
def command_measure_temp(chat):
	temp = os.popen('vcgencmd measure_temp').readline()
	temp = temp.replace('temp=', '')
	temp = temp.replace("'", "º")
	send_message(chat['id'], 
                 f'A temperatura do bot no momento é {temp}')
