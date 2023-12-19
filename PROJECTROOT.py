from tkinter import *
import requests
from googletrans import Translator
from PIL import Image
from PIL import ImageTk
import time


def request():
    """does a url-request for api weather site to get information, using global city value

    Returns:
        dict: dictionary with weather data from api weather site for selected city
    
    Examples:
        >>> city = "Las Vegas"
        >>>request()
        {'coord': {'lon': -115.1372, 'lat': 36.175}, 
        'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}],
        'base': 'stations',
        'main': {'temp': 9.54, 'feels_like': 8.47, 'temp_min': 8.4, 'temp_max': 10.45, 'pressure': 1013, 'humidity': 39}, 
        'visibility': 10000,
        'wind': {'speed': 2.24, 'deg': 50, 'gust': 0},
        'clouds': {'all': 75}, 'dt': 1702984255,
        'sys': {'type': 2, 'id': 2083590, 'country': 'US', 'sunrise': 1702997204, 'sunset': 1703032109},
        'timezone': -28800, 'id': 5506956, 'name': 'Las Vegas', 'cod': 200}
        
    """
    global city
    try:
        appid = "буквенно-цифровой APPID"
        key = '05be92c5b3657364acdabfd54e68fb0f'
        url =  'https://api.openweathermap.org/data/2.5/weather'
        params = {'APPID':key,'q': city, 'units':'metric'}
        result = requests.get(url, params = params, timeout = 5)
        weather = result.json()
    except Exception as e:
        print("Exception (find):", e)
        pass
    return weather

def utc_to_regular(utc_time: str):
    """converts utc time format to regular representation

    Args:
        utc_time (str): variable in utc format from data of request

    Returns:
        str: time in regular represetation
    """
    regularTime = time.ctime(int(utc_time))
    regularTime = regularTime.split()
    return regularTime[3]
    
def change_values(results):
    """sets new interface for GUI - shows weather, values of wind speed
    humidity, temerature, time of sunrise and sunset

    Args:
        results (dict): dictionary with weather data from api weather site for selected city
    """
    global counter_of_image_replace
    try:
        if counter_of_image_replace > 0:
            weather_value.delete("all")
        match results['weather'][0]['main']:
            case "Snow":
                image = weather_value.create_image(0, 0, anchor='nw',
                                                   image=photo_snow)
                counter_of_image_replace += 1
            case "Rain":
                image = weather_value.create_image(0, 0, anchor='nw',
                                                   image=photo_rain)
                counter_of_image_replace += 1
            case "Haze":
                image = weather_value.create_image(0, 0, anchor='nw',
                                                   image=photo_haze)
                counter_of_image_replace += 1
            case "Fog":
                image = weather_value.create_image(0, 0, anchor='nw',
                                                   image=photo_haze)
                counter_of_image_replace += 1
            case "Clear":
                image = weather_value.create_image(0, 0, anchor='nw',
                                                   image=photo_clear)
                counter_of_image_replace += 1
            case 'Clouds':
                image = weather_value.create_image(0, 0, anchor='nw',
                                                   image=photo_clouds)
                counter_of_image_replace += 1
        temperature_value.config(text = f'{results['main']['temp']}C')
        temperature.config(text = 'Temperature')
        wind.config(text = 'Wind')
        humidity.config(text = 'Humidity')
        weather.config(text = 'Weather')       
        wind_value.config(text= f'{results['wind']['speed']}m/s') 
        humidity_value.config(text = f'{results['main']['humidity']}%')
        sunrise.config(text = 'Sunrise')
        sunset.config(text = 'Sunset')
        sunrise_value.config(text = str(utc_to_regular(results['sys']['sunrise'])))
        sunset_value.config(text = str(utc_to_regular(results['sys']['sunset'])))
    except:
        introductory_label.config(text = f'There is no city {city},try again')
           
def web_parcing():
    """includes several instructions which functions to launch after asserting "city" is 
    correct variable
    """
    results = request()
    change_introductory()
    change_values(results)

def translation(city: str):
    """translates city from russian to english

    Args:
        city (str): city that user entered

    Returns:
        str: _description_
    """
    text = city
    a = translator.translate(text, dest = 'en')
    return a.text

def input_check(city, is_english):
    """checks global variable city for forbidden symbols and calls for translation
    if city is written in russian

    Args:
        city (str): string which is beeing checked
        is_english(boolean): flag if city is in russian or not
    
    Returns:
        tuple: correct or not correct input and changed city (if it was in russian)
    
    Examples:
        >>>city = "Москва"
        >>>input_check(city)
        True, "Moscow"
    """
    correct_input = True
    if not is_english:
        city = translation(city)
    arr = city.split(' ')
    for n in arr:
        for i in range(len(n)):
            letter_ind = ord(n[i])
            if not (65 <= letter_ind <= 90 
                    or 97 <= letter_ind <= 122 
                    or n[i] == '-'):
                correct_input = False
                break
    return (correct_input, city)

def clear_the_entry_field():
    """clears the entry field for future input
    
    """
    global city
    entry_field.delete(0,len(city))

def change_introductory():
    """configurates introductory label
    
    """
    global city
    introductory_label.config(text = f"Here is your weather in {city} for now")

def submission():
    """launches main algorithm, when "submit" button was pressed (checks input, 
    calls for request and web parsing)
    
    """
    global city 
    city = entry_field.get()
    flag = True
    is_english = english.get()
    flag , city = input_check(city, is_english)
    if flag:
        clear_the_entry_field()
        web_parcing()
    else:
        clear_the_entry_field()
        introductory_label.config(text='Please try to enter city again')
    
def backspace(event):
    """delets one symbol when backspace is pressed

    Args:
        event: represents that certain event (backspace pressed) occured
    """
    temp = entry_field.get()
    entry_field.delete(len(temp)-1, len(temp)-1)

counter_of_image_replace= 0
city = ''
root = Tk()
root.title("Simple Weather App")
root.resizable(False, False)
root.geometry("350x500")
bg_color = '#8BC2FF'
secondbg_color = '#0050AB'
image_snow = Image.open('free-icon-snowfall-5620248 (1).png')
photo_snow = ImageTk.PhotoImage(image_snow)
image_rain = Image.open('free-icon-rain-8722103.png')
photo_rain = ImageTk.PhotoImage(image_rain)
image_haze = Image.open('free-icon-foggy-day-4089256.png')
photo_haze = ImageTk.PhotoImage(image_haze)
image_clear = Image.open('free-icon-sun-5367718.png')
photo_clear = ImageTk.PhotoImage(image_clear)
image_clouds = Image.open('free-icon-clouds-414927.png')
photo_clouds = ImageTk.PhotoImage(image_clouds)
icon =  PhotoImage(file = '3721962.png')
root.iconphoto(False, icon )
root.config(bg = bg_color)
upper_frame = Frame(root, pady = 1, height=1, bg = bg_color)
upper_frame.place(relheight=0.15, relwidth=1)
introductory_label = Label(upper_frame,anchor = 'n', font = ("Arial", 14),
                           text = "Enter your city please", bg = bg_color)
introductory_label.pack()
entry_frame = Frame(root,height = 10,bg = bg_color )
entry_frame.place(relwidth=1, rely = 0.94, relheight=0.06)
entry_frame.grid_columnconfigure(0, minsize = 250)
entry_frame.grid_columnconfigure(1, minsize = 100)
entry_field = Entry(entry_frame)
entry_field.grid(row = 0 , column= 0, sticky = 'wesn')
entry_field.bind('<BackSpace>', backspace)
SubmitButton = Button(entry_frame, bg = secondbg_color, fg = '#FF3333',
                      text = 'Submit', command =lambda: submission())
SubmitButton.grid(row = 0 , column =1, sticky = 'wesn')
english = BooleanVar(value = True)
english_check = Radiobutton(master = upper_frame, text = 'English',
                            variable = english, value = True,
                            bg=bg_color, fg= '#FF3333')
russian_check = Radiobutton(master = upper_frame, text = 'Russian',
                            variable= english , value = False,
                            bg=bg_color, fg= '#FF3333')
english_check.pack(anchor = W)
russian_check.pack(anchor = W)
translator = Translator()
central_frame = Frame(root, bg = bg_color)
central_frame.place(rely = 0.15, relheight=0.79, relwidth=1)
central_frame.grid_columnconfigure(0,minsize = 200)
central_frame.grid_columnconfigure(1,minsize = 200)
central_frame.grid_rowconfigure(0, minsize = 55)
central_frame.grid_rowconfigure(1, minsize = 55)
central_frame.grid_rowconfigure(2, minsize = 55)
central_frame.grid_rowconfigure(3, minsize = 55)
central_frame.grid_rowconfigure(4, minsize = 55)
central_frame.grid_rowconfigure(4, minsize = 55)
temperature = Label(central_frame,anchor = 'w', font = ('Arial', 14),
                bg = bg_color, fg = '#FF3333', justify = 'left')
humidity = Label(central_frame, anchor = 'w', font = ('Arial', 14),
                bg = bg_color, fg = '#FF3333', justify = 'left')
weather = Label(central_frame, anchor = 'w' , font = ('Arial', 14),
                bg = bg_color, fg = '#FF3333', justify = 'left')
wind = Label(central_frame, anchor = 'w' , font = ('Arial', 14),
                bg = bg_color, fg = '#FF3333', justify = 'left')
sunset = Label(central_frame, anchor= 'w', font = ('Arial', 14),
                bg = bg_color, fg = '#FF3333', justify = 'left')
sunrise = Label(central_frame, anchor= 'w', font = ('Arial', 14),
                bg = bg_color, fg = '#FF3333', justify = 'left')
temperature.grid(column=0, row=0)
weather.grid(column=0, row = 1)
wind.grid(column=0,row =2)
humidity.grid(column = 0, row = 3)
sunset.grid(column=0, row = 4)
sunrise.grid(column=0, row = 5)
weather_value = Label(central_frame, anchor='w',
                      font = ('Ariel', 14), bg = bg_color, fg = '#FF3333')
wind_value = Label(central_frame, anchor='w',
                   font = ('Ariel', 14), bg = bg_color, fg = '#FF3333')
humidity_value = Label(central_frame, anchor='w',
                       font = ('Ariel', 14), bg = bg_color, fg = '#FF3333')
weather_value = Canvas(central_frame, height = 60,
                       width = 60, bg = bg_color, highlightthickness = 0)
temperature_value = Label(central_frame, anchor='w', font = ('Ariel', 14),
                          bg = bg_color, fg = '#FF3333')
sunset_value = Label(central_frame, anchor='w', font = ('Ariel', 14),
                          bg = bg_color, fg = '#FF3333')
sunrise_value = Label(central_frame, anchor='w', font = ('Ariel', 14),
                          bg = bg_color, fg = '#FF3333')
temperature_value.grid(column=1, row=0)
wind_value.grid(column=1, row = 2)
weather_value.grid(column = 1, row = 1)
humidity_value.grid(column=1, row = 3)
weather_value.grid(column = 1, row = 1)
sunrise_value.grid(column=1, row = 5)
sunset_value.grid(column=1, row = 4)
mainloop()
