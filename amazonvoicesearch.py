import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
from selenium import webdriver  
import time  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait  


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif  hour>=12 and hour <18:
        speak("Good Afternoon!") 
    else:
        speak("Good Night!")               
    speak("Hi . How can I help you?")

def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recogonizing...")
        query = r.recognize_google(audio, language='en-in') #hi-IN en-in
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)

        print("Say that again please....")
        return "None"  
    return query          


if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'amazon' in query:   
            try:
                speak("opening amazon.in on chrome")
                driver = webdriver.Chrome("chromedriver.exe")# chromedriver path
                driver.maximize_window()  
                driver.get("https://www.amazon.in/") 
                speak("Logging in to your amazon account, dont worry, i have your login credentials") 
                elem = driver.find_element_by_id("nav-link-accountList")
                elem.click()
                time.sleep(2)

                email = driver.find_element_by_id("ap_email")
                email.send_keys("email") #enter email
                submit = driver.find_element_by_id("continue")
                submit.click()
                time.sleep(2)

                password = driver.find_element_by_id("ap_password")
                password.send_keys("password") # enter password
                login = driver.find_element_by_id("signInSubmit")
                login.click()
                time.sleep(2)

                speak("what should I search")
                content = takeCommand() 
                searchbar = driver.find_element_by_name("field-keywords")  
                searchbar.send_keys(content)
                searchbar.submit()
                speak("Here are the results, I would recomend you to add the best seller in your cart")
                time.sleep(2)  

                selectproduct = driver.find_element_by_xpath("//*[@class= 'a-row a-badge-region']")
                selectproduct.click()
                time.sleep(2)  

                speak("would you like to add this item in your cart? or should i proceed with the buy now option?")
                query = takeCommand().lower()
                if 'add to cart' in query:
                    speak('adding to cart')
                    atc = driver.find_element_by_id("add-to-cart-button")
                    atc.click() 
                    speak("Item added to your cart , minimising the chrome ")
                    time.sleep(2)
                    driver.minimize_window()
                elif 'now' in query:
                    try:
                        speak('proceeding to buy now')
                        buynow = driver.find_element_by_id("buy-now-button")
                        buynow.click()
                        speak("As this is a payment page ,i would recommend you to fill the payment details")
                        time.sleep(2)

                    except Exception as e:
                        print(e)
                        speak("sorry could not proceed")    

                 
                
            except Exception as e:
                print(e)
                speak("sorry could not shop")        
                                 
            

                           