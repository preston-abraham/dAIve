import os
import openai
import streamlit as st
import warnings

openai.organization = "org-eptWwJzwl8LLZVNyAH1xBxbF"
openai.api_key = st.secrets['api_key']

st.title('dAIve v1.1')

st.markdown('***New Features**: Content Moderation, More finely-tuned model for better responses,Logging of questions and answers for further training*')

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
    # Check if content is flaggable
    
    content_to_classify = q

    response_flag = openai.Completion.create(
      model="content-filter-alpha",
      prompt = "<|endoftext|>"+content_to_classify+"\n--\nLabel:",
      temperature=0,
      max_tokens=1,
      top_p=0,
      logprobs=10
    )
    
    output_label = response_flag["choices"][0]["text"]
    
    if str(output_label) == '0':
        
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt = prefix + q,
          temperature = 0.15,
          top_p = 1,
          max_tokens = 500
        )

        a = response["choices"][0]["text"]

        st.markdown(a)
        warnings.warn('['+mode+':'+q + ',' + a+']')
    else:
        st.markdown("""
        Hey there, I'm dAIve and I'm here to help you with your financial questions. However, I'm sorry but I'm not able to answer that question for you. It goes against my programming to provide responses that may be considered offensive or inappropriate. I'm here to help you make smart financial decisions, so if you have any other questions, I'm here to assist you within the parameters of my abilities.
""")
