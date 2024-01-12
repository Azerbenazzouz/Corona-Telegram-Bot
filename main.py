import os
import requests
from aiogram import Bot, Dispatcher, executor, types
from keep_alive import keep_alive
from gtts import gTTS 

bot = Bot(token = os.getenv("tg_token"))
dp = Dispatcher(bot)
url = "https://disease.sh/v3/covid-19/countries"
response = requests.request("GET", url)
res = []

keep_alive()

@dp.message_handler(commands = ['start', 'help'])
async def welcome(message: types.Message):
  await message.reply('Hello! Im Corona chat bot. Give me your Country')
  for i in range(len(response.json())):
    res.append({
        'country' :response.json()[i]['country'],     
        'continent' :response.json()[i]['continent'],     
        'flag' :response.json()[i]['countryInfo']['flag'],     
        'cases' :response.json()[i]['cases'],     
        'todayCases' :response.json()[i]['todayCases'],     
        'deaths' :response.json()[i]['deaths'],     
        'todayDeaths' :response.json()[i]['todayDeaths'],     
        'recovered' :response.json()[i]['recovered'],     
        'todayRecovered' :response.json()[i]['todayRecovered']   
    })



def sendImg(countryImgUrl):
  try:
    payload = {
      "chat_id": "-1309151933",
      "photo": countryImgUrl,
      "captions": "Country Image..."
    }

    to_url ='https://api.telegram.org/bot{}/sendPhoto'.format(os.getenv("tg_token"))
    requests.post(to_url, data=payload)
  except Exception as e:
    print(e)
    

@dp.message_handler()
async def getDataForContry(message: types.Message):
  filtered_data = list(filter(lambda x: x['country'] == message.text, res))
  try:
    sendImg(filtered_data[0]['flag'])
  
    await message.reply_photo(filtered_data[0]['flag'])
    
    await message.reply("Country : "+filtered_data[0]['country']
                       +"\nContinent : "+filtered_data[0]['continent']
                       +"\nCases : "+str(filtered_data[0]['cases'])
                       +"\nToday Cases : "+str(filtered_data[0]['todayCases'])
                       +"\nDeaths : "+str(filtered_data[0]['deaths'])
                       +"\nToday Deaths : "+str(filtered_data[0]['todayDeaths'])
                       +"\nRecovered : "+str(filtered_data[0]['recovered'])
                       +"\nToday Recovered : "+str(filtered_data[0]['todayRecovered']))
    
    
    myobj = gTTS(text="Country : "+filtered_data[0]['country']
                  +"\nContinent : "+filtered_data[0]['continent']
                  +"\nCases : "+str(filtered_data[0]['cases'])
                  +"\nToday Cases : "+str(filtered_data[0]['todayCases'])
                  +"\nDeaths : "+str(filtered_data[0]['deaths'])
                  +"\nToday Deaths : "+str(filtered_data[0]['todayDeaths'])
                  +"\nRecovered : "+str(filtered_data[0]['recovered'])
                  +"\nToday Recovered : "+str(filtered_data[0]['todayRecovered']),lang="en", slow=False) 
    myobj.save("covid.mp3")
    await message.reply_audio(audio=open("covid.mp3", 'rb'))
    os.remove("covid.mp3")
  except:
    await message.reply("Country not found")
  finally:
    await message.reply('Developed By @azerbenazzouz And @lamysksouri')

if __name__ == "__main__":
  executor.start_polling(dp)