import streamlit as st
import pandas as pd
import openai
from faker import Faker
import requests
import json

import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key='YOUAPI',
)
        
user_input = st.text_input('Enter your request')
n =st.number_input("enter number of rows",min_value=1 ,value=10)
template_json ="""
{
    "columns": {
        "user_id": {
            "sdtype": "id",
        },
        "age": {
        "sdtype": "numerical",
        "compute_representation": "Int64"
},
    "paid_amt": {
        "sdtype": "numerical",
        "compute_representation": "Float"
    },
        "address": {
            "sdtype": "address",
            "pii": True
        }, 
        "tier": {
            "sdtype": "categorical"
        },
        "active": {
            "sdtype": "boolean"
        },
        "paid_amt": {
            "sdtype": "numerical"
        },
        "renew_date": {
            "sdtype": "datetime",
            "datetime_format": "%Y-%m-%d"
        }
    }
"""


if st.button('Generate Data'):
    with st.spinner('Generating data schema...'):
        messages = [
        {"role": "system" ,"content" : "Give me a JSON with the fields names and sdtype, pii flag and compute_representation .Reference :" + template_json},
        {"role": "user", "content" : user_input}
    ]
        print(messages)
        response = chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo"
        )
        #print(response)
        #print(fields)
        #df = generate_data(fields,n)
        #st.dataframe(df)
        # Assuming chat_completion variable is the response received from the OpenAI API

        # Access the first choice (if you have more than one, adjust the index accordingly)
        choice = response.choices[0]

        # Extract the generated message content
        generated_content = choice.message.content  # This is a string containing the JSON content

        # Output the generated content
        print(generated_content)
        json_content = json.loads(generated_content)
        st.success('Data schema generated!')
        df = pd.DataFrame(json_content)
        st.dataframe(df)
    with st.spinner('Generating Sample data...'):
        messages = [
        {"role": "system" ,"content" : "Give me JSON " + str(n) + "synthetic rows fitting the schema Reference :" + str(json_content)},
        {"role": "user", "content" : "Provide only json dataset referencing the schema"  + str(json_content)}
    ]
        response_2 = chat_completion = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo"
        )
                # Access the first choice (if you have more than one, adjust the index accordingly)
        choice_2 = response_2.choices[0]

        # Extract the generated message content
        generated_content_2 = choice_2.message.content  # This is a string containing the JSON content

        # Output the generated content
        print(generated_content_2)
        json_content_2 = json.loads(generated_content_2)
        st.success('Data generated!')
        df_2 = pd.DataFrame(json_content_2)
        st.dataframe(json_content_2)
