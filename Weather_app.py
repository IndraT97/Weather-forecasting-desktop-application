import pandas as pd
import matplotlib.pyplot as plt
from pyowm import OWM
from sklearn import datasets
import streamlit as st
import seaborn as sns
import requests

header = st.container()
header2 = st.container()
datasets = st.container()
owm = OWM("b83286cbe60567928fcfd55f12aa585d")
mgr = owm.weather_manager()

with header:

    st.markdown("**Indrajeet Thakare**")
    st.title("Welcome to the Weather Forecast")
    City_name_st = st.text_input("Enter your city name in the below taskbar","City Name")
    #Unit_st = st.radio("Select the temperature unit",("Fahrenheit","celsius"))
    Graph_st = st.selectbox("Select the temperature unit",("BarGraph","LineGraph"))
    Radio = st.radio("Select Temp unit -",options=("Celsius","Fahrenheit"))


with datasets:
    api_key = "b83286cbe60567928fcfd55f12aa585d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={City_name_st}&appid={api_key}"
    req = requests.get(url)
    data = req.json()
    lon = (data["coord"]["lon"])
    lat = (data["coord"]["lat"])
    exclude = "minute,hourly"
    url2 = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}"
    req2 = requests.get(url2)
    data2 = req2.json()
    #st.dataframe(data2["daily"])
    a = pd.DataFrame(data2["daily"])
    a["F_temp"] = a["temp"][0]["day"]
    a["F_temp_max"] = a["temp"][0]["day"]
    a["F_temp_min"]= a["temp"][0]["day"]
    a["*C_temp"] = a["temp"][0]["day"]
    a["*C_temp_max"] = a["temp"][0]["day"]
    a["*C_temp_min"] = a["temp"][0]["day"]
    for i in range(len(a["temp"])):
        a["F_temp"][i] = a["temp"][i]["day"]
        a["F_temp_max"][i] = a["temp"][i]["max"]
        a["F_temp_min"][i] = a["temp"][i]["min"]
        a["temp"][i]["day"] = round(a["temp"][i]["day"] - 275.15,1)
        a["temp"][i]["min"] = round(a["temp"][i]["min"] - 275.15,1)
        a["temp"][i]["max"] = round(a["temp"][i]["max"] - 275.15,1)
        a["*C_temp"][i] = a["temp"][i]["day"]
        a["*C_temp_min"][i] = a["temp"][i]["min"]
        a["*C_temp_max"][i] = a["temp"][i]["max"]
    a.drop("feels_like",axis= 1)
    a.drop("temp",axis= 1)

    
with header2:
    if st.button("Submit") == True:
        st.subheader("Today's Weather Update")
        st.write("-- Temperature in *C :",round(data["main"]["temp"] - 275.15,2),"|F",data["main"]["temp"],"|Max *C : ",round(data["main"]["temp_max"] - 275.15,2),"|Min *C: ",round(data["main"]["temp_min"] - 275.15,2))
        st.write("-- Cloud :",data["weather"][0]['description'])
        st.write("-- Wind :","Speed : ",data["wind"]["speed"],"mph","|Deg : ",data["wind"]["deg"])
        st.write("-- Humidity :",data["main"]["humidity"])
        st.write("-- Sunrise :",data["sys"]["sunrise"])
        st.write("-- Sunset :",data["sys"]["sunset"])
        st.subheader("Temperature forecast for next 7 days - ")
        if Radio == "Celsius" and Graph_st == "LineGraph":
            st.line_chart(data = a[["*C_temp_min","*C_temp_max"]])
        if Radio == "Celsius" and Graph_st == "BarGraph":
            st.bar_chart(data = a[["*C_temp_min","*C_temp_max"]])
        if Radio == "Fahrenheit" and Graph_st == "LineGraph":
            st.line_chart(data = a[["F_temp_max","F_temp_min"]])
        if Radio == "Fahrenheit" and Graph_st == "BarGraph":
            st.bar_chart(data = a[["F_temp_max","F_temp_min"]])
        #
        st.subheader("Forecast Weather Updates")
        forecaster_3h = mgr.forecast_at_place(City_name_st, '3h')
        #forecaster_daily = mgr.forecast_at_place(City_name_st, 'daily')
        if forecaster_3h.will_have_rain() == True:
            st.info("**Rainy days ahead**")
        if forecaster_3h.will_have_fog() == True:
            st.info("**Expect Some Fog in upcomming day's**")
        if forecaster_3h.will_have_snow() == True:
            st.info("**Expect some Fog**")
        if forecaster_3h.will_have_snow() == False:
            st.info("**No snowy day's**")
        if forecaster_3h.will_have_storm() == True:
            st.info("**Expect some kind of storm in next 7 day's**")
        if forecaster_3h.will_have_tornado() == False:
            st.info("**No Indication's of tornado**")
        if forecaster_3h.will_have_hurricane() == False:
            st.info("**No Indication's of Hurricane**")
        if forecaster_3h.will_have_storm() == False:
            st.info("**No storm in next 7 day's**")
        #st.write("It will be clear weather in next : ",forecaster_daily.when_clear(),"day's")
        # generate date column r