from boltiot import Bolt
import requests,json
import configure.conf as conf

mybolt = Bolt(conf.bolt_api_key,conf.device_id)
mypin = 'A0'

def check_online():
    response = mybolt.isOnline()
    data = json.loads(response)
    print(response)
    if data['time']==None:
        return 0
    else:
        return 1

def get_sensor_value(pin):
    try:
        response = mybolt.analogRead(pin)
        data = json.loads(response)
        if data['success']!=1:
            print("Could Not get sensor value")
            return -999
        sensor_value = data['value']
        return int(sensor_value)
    except Exception as err:
        print("An ERROR Occured!")
        print(err)
        return -999

#SENDING A MESSAGE TO THE TELEGRAM CHANNEL
def telegram_message(message):
    url = "https://api.telegram.org/" + conf.telegram_bot_id + "/sendMessage"
    data = {
        "chat_id" : conf.telegram_chat_id,
        "text" : message
    }

    try:
        response = requests.request("POST",url,params=data)
        print(response.text)
        return json.loads(response.text)["ok"]
    except Exception as e:
        print ("An ERROR Occured!")
        print (e)
        return False
    
def run():
    lat = "28.6104389"
    lon = "77.2502572"
    url = "https://api.open-meteo.com/v1/forecast?latitude="+lat+"&longitude="+lon+"&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = requests.get(url)
    data = response.json()
    area_temp_int = data['current_weather']['temperature']
    area_temp = str(data['current_weather']['temperature'])+ " °C"
    sensor_value  = get_sensor_value(mypin)
    if(sensor_value == -999):
        message = "Couldn't read values"
        exit
    current_temp = (100*sensor_value)/1024
    current_temp_str = "{:.1f}".format((100*sensor_value)/1024)
    if(current_temp > area_temp_int):
        temp_diff = "{:.1f}".format(current_temp - area_temp_int)
        message = "Outside Temp : " + area_temp + "\nInside Temp : " + str(current_temp_str) + " °C\nRoom is Hotter than Outside by : \n" + str(temp_diff) + " °C"
    elif current_temp == area_temp_int:
        message = "Outside Temperature is same as Inside Temperature which is : \n" + str(current_temp_str) + " °C"
    else:
        temp_diff = "{:.1f}".format(area_temp_int - current_temp)
        message = "Outside Temp : " + area_temp + "\nInside Temp : " + str(current_temp_str) + " °C\nRoom is Colder than Outside by : \n" + str(temp_diff) + " °C"
    msg_status = telegram_message(message)
    print("This is the Telegram status : ",msg_status)

global flag 
flag = False
def final_run(flag):
    if check_online()==1:
        flag = True
        run()
    else:
        flag = False
        message = "Device is Offline. Couldn't fetch data."
        msg_status = telegram_message(message)
        print("This is the Telegram status : ",msg_status)

def define_msg():
    return flag
        