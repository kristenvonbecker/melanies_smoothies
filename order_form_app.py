import streamlit as st
from snowflake.snowpark.functions import col 
import requests

st.title(" :cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want to customize your smoothie...")

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    
    ingredient_string = ''
  
    for ingredient in ingredients_list:
        
        ingredient_string += ingredient + ', '
        
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + ingredient)
        json_data = fruityvice_response.json()
        fv_df = st.dataframe(data=json_data, use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredient_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered, {}!'.format(name_on_order), icon="✅")

