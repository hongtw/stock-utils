import telegram
import json
from datetime import datetime

config = json.load(open('telegram.json'))
bot = telegram.Bot(token=config['token'])
bot.send_message(chat_id=config['chat_id'], text=f"[{datetime.now()}] Test~~")

# show all chat id
import requests
res = requests.get(f"https://api.telegram.org/bot{config['token']}/getUpdates")
print(json.dumps(res.json(), indent=4, ensure_ascii=False))
