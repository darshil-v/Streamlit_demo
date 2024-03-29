import streamlit #as st
import numpy as np
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Lemon','Watermelon'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruit_deets(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruitvice_normalised = pd.json_normalize(fruityvice_response.json())
    return fruitvice_normalised

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please enter valid fruit choice.')
  else:
    val_from_fruit_func = get_fruit_deets(fruit_choice)
    streamlit.dataframe(val_from_fruit_func)

except URLError as e:
  streamlit.error()
  
streamlit.header("The fruit load list contains:")

def fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
 
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_row)

    
def added_new_fruit(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO fruit_load_list values ('"+new_fruit+"')")
        return 'Thanks for adding ' + add_my_fruit
        
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit to list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_func = added_new_fruit(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_func)

streamlit.stop()
