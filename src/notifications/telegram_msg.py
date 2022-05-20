import requests

def send_message(msg):
	TOKEN = "5323726107:AAEanyYt-JvKiZdopd_m19OK5TelvjFC5sc"
	chat_id = "-1001653472294"
	# text = "JacoHansCABot speaks"
	text = msg
	url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
	# url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
	r = requests.get(url)
	return r.json()

# if __name__ == '__main__':
# 	print(send_message(''))