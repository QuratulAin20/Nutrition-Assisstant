import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type ,
                "data"  : bytes_data
            }
        ] 
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

st.set_page_config(page_title= "Nutritionist Advisor")

st.header("Calories Calculator")
uploaded_file = st.file_uploader("Choose an Image..." , type = ["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image , caption="Uploaded Image." , use_column_width=True)

submit = st.button("Tell me about the total calories")

input_prompt = """

You are an expert nutritionist where you need to see the food items from the image and calculate the total nutrients ue in that food
                also calculate the calories and provide the details of every food item with calories in take in below format
                1. Item 1 - No. of calories
                2. Item 2 - No. of vitamins
        Finally you can also mention whether the food is healthy or not , if food is not healthy what option can we use 
        instead of it.
        Also mention the percentage of Carbohydrates,Fats, Proteins,Fiber , Suagar and other important thing we required in our diet. 

"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt , image_data)
    st.header("The response is")
    st.write(response)

