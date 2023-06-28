import telegram
import os
import logging
import telebot
import time
import math
import datetime
import requests
import json
from datetime import date
import pytz

BOT_TOKEN = ""
channel_id = '-1001934424799'
text = "<a href='a.com'> meme </a>"
url = "https://www.census.gov/popclock/data/population.php/us"

bot = telebot.TeleBot(BOT_TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CAGR = 0.0794
initialDebt = 30928910000000
perSecondGrowthRate = math.pow(1 + CAGR, 1 / (365 * 24 * 60 * 60)) - 1

def updateDebtClock():
    currentTime = datetime.datetime.now()
    startOf2023 = datetime.datetime(2023, 1, 1, 0, 0, 0)
    secondsSince2023 = (currentTime - startOf2023).total_seconds()
    currentDebt = initialDebt * math.pow(1 + perSecondGrowthRate, secondsSince2023)
    # set the timezone you want to display

    return currentDebt
def getTodayPopulation():
    day = date.today()
    tday = day.strftime("%Y%m%d")
    
    params = {
        "date": tday,
        "_": "1687237185721"
    }
    response = requests.get(url, params=params)
    data = json.loads(response.content)
    population = data["us"]["population"]
    return population
    
    
def getCurBitcoinprice():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    data = response.json()
    bitcoin_price = data["bitcoin"]["usd"]
    return bitcoin_price

def main():
    
    # bot.infinity_polling()   
    while True:

        tpopulation = getTodayPopulation()
        print("today us poplulation =", tpopulation)
        curbitcoin = getCurBitcoinprice()       
        print("curbitcoin prince = ", curbitcoin)
        curDebt = int(updateDebtClock())
        str_curdebt = format(curDebt, ',')
        print("curDebt = ", format(curDebt, ','))

        per_debt = int(curDebt/tpopulation)
        str_perdebt = format(per_debt, ',')
        per_bitcoin = 21000000/tpopulation
        str_perbitcoin = format(per_bitcoin, ',.4f')
        print("perdet", per_debt)
        print("per_bitcoin", per_bitcoin)
        print("################################")
        
        debturl = ""
        websiteurl = ""
        bitcoinurl = ""
        usdebturl = ""
        memecoinurl = ""
        cryptourl = ""
        # debturl = "https://twitter.com/hashtag/nationaldebt?src=hashtag_click"
        # websiteurl = "https://twitter.com/hashtag/ITONLYGOESUP?src=hashtag_click"
        # bitcoinurl = "https://twitter.com/hashtag/Bitcoin?src=hashtag_click"
        # usdebturl = "https://twitter.com/search?q=%24USDEBT&src=cashtag_click"
        # memecoinurl = "https://twitter.com/hashtag/memecoins?src=hashtag_click"
        # cryptourl = "https://twitter.com/hashtag/Crypto?src=hashtag_click"
    
        timezone = pytz.timezone('US/Pacific')

        # get the current date time in the desired format
        current_time = datetime.datetime.now(timezone).strftime('%B %d, %Y, %I:%M %p %Z').replace("PDT", "PST")

        # print the current date time with timezone
        

        caption = "\n"+ f"\n🇺🇲 <a href='{debturl}'>#NationalDebt: </a>${str_curdebt} \n \nDebt per person: ${str_perdebt} 👀\n<a href='{bitcoinurl}'>#Bitcoin</a> per U.S. person: {str_perbitcoin} 🚀 \n\nSpread Awareness. Get in <a href='{usdebturl}'>$USDEBT</a>. Fuel the crypto Bull Run!\n<a href='{websiteurl}'> #ITONLYGOESUP</a>\n \nSource: USDEBT Meme Coin({current_time})\n<a href='{cryptourl}'>#Crypto</a><a href = '{memecoinurl}'> #memecoins </a>"
        # caption = f"\n🇺🇲 <a href='{debturl}'>#nationaldebt:</a> {curDebt} \n \n Debt per person: ${per_debt} \n <a href='{bitcoinurl}'>#Bitcoin</a> per person: {per_bitcoin} \n <a href={websiteurl}></a>\n Meme-ing our way into a Bull Run in Crypto! \n \n Source: USDEBTMEMECOIN(June)\n <a href = {websiteurl}>#Crypto #memecoins </a>"
        # bot.send_message(chat_id=channel_id, text=text)
        bot.send_photo(chat_id=channel_id, photo=open("msg.png", 'rb'), caption=caption,  parse_mode='HTML')
        time.sleep(60 * 60)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    print("bot received message")
    bot.reply_to(message, message.text)
    print(message.chat.id)
if __name__ == '__main__':
    main()

