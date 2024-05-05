import streamlit as st
from random import choice, shuffle
from streamlit_option_menu import option_menu
import pandas as pd
from PIL import Image

# --- SETUP PAGE AND NAVIGATION MENU ---
# Page setup
page_title = "Password Generator"
page_icon = ":lock:"
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# Setup navigation menu
selected = option_menu(
    menu_title=None,
    options=["Password", "Settings", "About"],
    icons=["lock-fill", "gear", "app-indicator"],  # https://icons.getbootstrap.com
    orientation="horizontal",
)

# Display log in sidebar
image = Image.open('password_logo.jpg')
st.sidebar.image(image, width=300)

# --- SETTINGS ---

# HTML tags to print different color bars. Use to display the password strength indicator
red = '<div style = "display: inline-block;"> <div style="background-color: red; width: 20px; height: 10px;"></div> </div>'
coral = '<div style = "display: inline-block;"> <div style="background-color: coral; width: 20px; height: 10px;"></div> </div>'
orange = '<div style = "display: inline-block;"> <div style="background-color: orange; width: 20px; height: 10px;"></div> </div>'
khaki = '<div style = "display: inline-block;"> <div style="background-color: khaki; width: 20px; height: 10px;"></div> </div>'
yellowgreen = '<div style = "display: inline-block;"> <div style="background-color: yellowgreen; width: 20px; height: 10px;"></div> </div>'
green = '<div style = "display: inline-block;"> <div style="background-color: green; width: 20px; height: 10px;"></div> </div>'

# Color list for password strength indicator
colors = [red, coral, orange, khaki, yellowgreen, green]

# Text for password strength
strength_list = ['Very Weak', 'Weak', 'Medium', 'OK', 'Strong', 'Very Strong']

# Font color of password strength text
font_color = ['red', 'red', 'orange', 'orange', 'green', 'green']


# --- FUNCTIONS ---
# Gather input feature for Password generation
def user_input_features():
    st.sidebar.title("Configure Settings")
    st.sidebar.subheader("Password Length")
    pwd_length = st.sidebar.slider('Length', 10, 25, 15)
    st.sidebar.subheader("Use Numbers/Symbols")
    pwd_symbols = st.sidebar.checkbox("Use Symbols")
    pwd_numbers = st.sidebar.checkbox("Use Numbers")
    st.sidebar.subheader("Use Upper/Lowercase")
    ch_option = st.sidebar.radio('Character Type', ['Lowercase', 'Uppercase', 'Both'],
                                 captions=['Such as abc', 'Such as ABC', 'such as aBC'])
    data = {'password_length': pwd_length,
            'use_symbols': bool(pwd_symbols),
            'use_numbers': bool(pwd_numbers),
            'ch_option': ch_option
            }
    features = pd.DataFrame(data, index=[0])
    return features


# Generate random password based on input provided by the user
def generate_password(p_df):
    ul_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lower_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z']
    upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    if p_df['ch_option'][0] == 'Lowercase':
        letters = lower_letters
    elif p_df['ch_option'][0] == 'Uppercase':
        letters = upper_letters
    else:
        letters = ul_letters
    password_length = p_df['password_length'][0] - p_df['use_symbols'][0] * 4 - p_df['use_numbers'][0] * 4
    password_list = [choice(letters) for _ in range(password_length)]
    if p_df['use_symbols'][0]:
        password_list += [choice(symbols) for _ in range(4)]
    if p_df['use_numbers'][0]:
        password_list += [choice(numbers) for _ in range(4)]

    shuffle(password_list)
    random_password = "".join(password_list)

    return random_password


# Function to calculate the strength of the password
def password_strength(p_df):
    if p_df['ch_option'][0] == 'Both':
        ul_option = 1
    else:
        ul_option = 0

    pwd_strength = p_df['password_length'][0] // 7 + p_df['use_symbols'][0] + p_df['use_numbers'][0] + ul_option

    # Subtracting one for array indexing
    return pwd_strength - 1


# Get user features in a data frame
pwd_df = user_input_features()

# ------ SETUP PASSWORD MENU ------
if selected == "Password":
    st.title("Strong Password Generator")
    st.markdown('Use this app to generate strong passwords and protect your digital identity from potential '
                'threats and attacks :lock::+1:. Configure password parameters from left pane. Once done, click '
                'the *Generate Password* button')

    press = st.button("Generate Password", type="primary")

    # Generate password when button is pressed
    if press:
        password = generate_password(pwd_df)
        length = len(password)
        st.subheader('Generated Password')
        st.code(password, language="python")
        # Change the color to blue and make it bold
        st.write(f"Password length is: **:blue[{length}]**")

        strength = password_strength(pwd_df)
        content = ""
        for s_id, color in enumerate(colors):
            content += color + " "
            if s_id == strength:
                break

        st.subheader('Password Strength')
        st.write(f''' {content} ''', unsafe_allow_html=True)
        st.write(f'**:{font_color[strength]}[{strength_list[strength]}]**')

# ------ SETUP SETTINGS MENU ------
if selected == "Settings":
    st.subheader('Password Settings')
    # Display the input features in tabular format
    st.write(f'''
    | Password Length        | Use Symbols           | Use Numbers | Use Upper/Lowercase | 
    | :-------------: |:-------------:|:-----:| :-----------: |
    | {pwd_df['password_length'][0]} | {pwd_df['use_symbols'][0]} | {pwd_df['use_numbers'][0]} | {pwd_df['ch_option'][0]} |
    ''')
    st.write('')

# ------ SETUP ABOUT MENU ------
if selected == "About":
    st.subheader('About')
    with st.expander('**Why to use this app?**'):
        st.markdown(''' Using a strong password is essential to maintain the security of your online accounts and personal information.
                        Here are some benefits of using strong password:
        
    - Increased Security
    - Protection Against Hacking
    - Prevention of Identity Theft
    - Compliance with Security Policies
    - Peace of Mind
        ''')
    with st.expander('**What are the features of this app?**'):
        st.markdown(''' This app has following features:
        
    - Generate password of varying length
    - Include Symbols, numbers  and upper/lower case letters in the password
    - Display the strength of the password 
        ''')
    with st.expander('**How long will it take for super computer to crack  password generated from this app**'):
        st.markdown(''' Dont' worry, it will not happen in your life time.:smiley: For a very strong password,
        it will take billion of years for super computer to crack the password :astonished:. 
        ''')
    with st.expander('**Who developed this app**'):
        st.markdown(''' Developed with love by [Zeeshan Altaf](zeeshan.altaf@gmail.com) 
        ''')
