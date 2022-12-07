import os
import openai
import streamlit as st

openai.organization = "org-eptWwJzwl8LLZVNyAH1xBxbF"
openai.api_key = st.secrets['api_key']

st.title('dAIve')

from PIL import Image
image = Image.open('dAIve.png')
image = image.resize((100,100))
st.image(image)


text = """
## Person to Ask:
**Dave** : Standard Dave

**Radio Dave** : Dave that tries to answer like he would on the radio show

**Evil Dave** : Opposite version of Dave Ramsey who doesn't have your best interests in mind

"""
st.markdown(text)

mode = st.selectbox('Person to ask: ',['Dave','Radio Dave','Evil Dave'])
q = st.text_input('Question: ')

if mode == 'Dave':
    prefix = 'Respond to the following prompt the way Dave Ramsey would respond, as if you are him responding. Try to make it sound like Dave Ramsey sounds: '
    
if mode == 'Radio Dave':
    prefix = 'Respond to the following prompt the way Dave Ramsey would respond on his radio show politely, as if you are him responding. Try to make it sound like Dave Ramsey sounds in tone and word choice. Make sure not to contradict yourself in the answer, and try to use Dave Ramseys catch-phrases but only if they really fit: '
if mode == 'Evil Dave':
    prefix = 'Respond to the following prompt like an evil version person who beleives the exact opposite of what Dave Ramsey thinks and wants me to make bad financial decision would respond, with some sarcasm and slight rudeness: '

if st.button('Get answer'): 
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt = prefix + q,
      temperature = 0.15,
      top_p = 1,
      max_tokens = 500
    )
    st.markdown(response["choices"][0]["text"])
