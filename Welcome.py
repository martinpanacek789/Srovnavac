import streamlit as st

from streamlit_option_menu import option_menu

st.title("Hello World")

st.write("Title page of the app")

st.write("Some text here")


selected2 = option_menu(None, ['Vlastní parametry', "Bydlení", "Auto", "Studium", "Zahraniční pobyt"],
                        icons=['gear', 'house', 'car-front', "book", "airplane"],
                        menu_icon="cast", default_index=0, orientation="horizontal")

st.write(selected2)
