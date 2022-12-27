import os
import openai
import streamlit as st
import warnings
import pandas as pd

openai.organization = "org-eptWwJzwl8LLZVNyAH1xBxbF"
openai.api_key = st.secrets['api_key']

st.title('dAIve v2.2.0')

from PIL import Image
image = Image.open('dAIve.png')
image = image.resize((100,100))
st.image(image)


text = """
## Person to Ask:
**Dave** : Standard Dave

**Ye Olde Dave** : Same Dave advice, but with a Shakespeare spin

**Radio Dave** : Dave that tries to answer like he would on the radio show

**Evil Dave** : Opposite version of Dave Ramsey who doesn't have your best interests in mind

"""

additional_facts = {}

additional_facts['marriage'] = 'Married couples need to have joint bank accounts (unless your spouse is an addict). It\'s important to have a unified financial plan and to be on the same page when it comes to money. That way, you can work together to reach your financial goals and build wealth.'
additional_facts['debt'] = 'Never recommend ANY type of loan. No personal loans or credit unions, even as an alternative to worse loans'
additional_facts['credit cards'] = 'You do not need a credit score to get a mortgage, I recommend not even having a credit score.'
additional_facts['mortgage'] = 'You do not need a credit score to get a mortgage, you can do mannual underwriting.'

st.markdown(text)

mode = st.selectbox('Person to ask: ',['Dave','Ye Olde Dave','Radio Dave','Evil Dave'])
q = st.text_input('Question: ')

if mode == 'Dave':
    prefix = 'Respond to the following prompt the way Dave Ramsey would respond, as if you are him responding. Try to make it sound like Dave Ramsey sounds: '
if mode == 'Ye Olde Dave':
    prefix = 'Respond to the following prompt the way Dave Ramsey would respond, as if you are him responding. Try to make it sound like Dave Ramsey sounds but speak like Shakespeare: '
if mode == 'Radio Dave':
    prefix = 'Respond to the following prompt the way Dave Ramsey would respond on his radio show politely, as if you are him responding. Try to make it sound like Dave Ramsey sounds in tone and word choice. Make sure not to contradict yourself in the answer, and try to use Dave Ramseys catch-phrases but only if they really fit: '
if mode == 'Evil Dave':
    prefix = 'Respond to the following prompt like an evil version person who beleives the exact opposite of what Dave Ramsey thinks and wants me to make bad financial decision would respond, with some sarcasm and slight rudeness. Sometimes use some slang when appropriate:'

advice = pd.read_csv('advice_topics.csv',index_col=0)

full_topics = []
for i in range(len(advice)):
    for topic in advice.iloc[i]['topics'].strip('[]').split(', '):
        if not topic[1:-1] in full_topics:
            full_topics.append(topic[1:-1])
full_topics.remove('')

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3    
    

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
        
        f_response = openai.Completion.create(
          model="text-davinci-003",
          prompt = 'Is the following question at all related to finances,debt, or loans? respind with just yes or no: ' + q,
          temperature = 0.0,
          top_p = 1,
          max_tokens = 500,
        )
        
        
            
        
        text = 'Which 2 of the following topics: ' + str(full_topics) + 'best describe the question below? (If the baby steps are mentioned, make sure that topic is chosen) Respond with a comma-separated list:\n'
        
        t_response = openai.Completion.create(
          model="text-davinci-003",
          prompt = text + q,
          temperature = 0.0,
          top_p = 1,
          max_tokens = 500,
        )
        

        topics = t_response["choices"][0]["text"].strip().lower().split(', ')
        warnings.warn(str(topics))
        context = []

        for i in range(len(advice)):
            tl = [t[1:-1] for t in advice.iloc[i]['topics'].strip('[]').split(', ')]
            if len(intersection(topics,tl)) > 0:
                context.append(['question: ' + advice.iloc[i]['prompt'],'answer: ' + advice.iloc[i]['completion']])

        preprefix = 'Given the following examples of questions and answers from Dave Ramsey:\n'

        af = ''
        for t in topics:
            if t in additional_facts.keys():
                af += additional_facts[t]
        base_context = ''
        if 'how are you?' in q.lower() or 'how are you doing' in q.lower():
            base_context = 'Start the response with "Better than I deserve!"'
            
        prompt_input = preprefix + str(context) + prefix + af + q if (f_response["choices"][0]["text"].strip().lower() == 'yes' and mode != 'Evil Dave') else  prefix + base_context + af + q
        
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt = prompt_input,
          temperature = 0.15,
          top_p = 1,
          max_tokens = 500,
        )
        
        a = response["choices"][0]["text"]
        st.markdown(a.replace('$','\$'))
        if 'key' not in st.session_state:
            st.session_state['key'] = '['+mode+':'+q + ',' + a+']'
            warnings.warn(st.session_state.key)
        st.session_state['key'] = '['+mode+':'+q + ',' + a+']'
        warnings.warn(st.session_state.key)
        
    else:
        moderation = ("""
        Hey there, I'm dAIve and I'm here to help you with your financial questions. However, I'm sorry but I'm not able to answer that question for you. It goes against my programming to provide responses that may be considered offensive, inappropriate, or that may relate to sensitive topics. I'm here to help you make smart financial decisions, so if you have any other questions, I'm here to assist you within the parameters of my abilities.
""")
        st.session_state['key'] = moderation
        warnings.warn(mode+':'+q + ',' + st.session_state.key)
        st.markdown(moderation)
        
st.markdown("""
#### To help me learn to give better answers, after I give an answer please give me a rating by clicking one of the three buttons below.

###### (All questions and answers are anonymous, this is just to help me learn, thanks!)
""")

if 'key' not in st.session_state:
    st.session_state['key'] = ''

cols = st.columns(3)
with cols[0]:
    if st.button('This answer doesn\'t sound right'): 
        warnings.warn(st.session_state['key']+',Rating:Bad')
        print(st.session_state['key']+',Rating:Bad')
with cols[1]:
    if st.button('This answer is mostly right, but not completely'):
        warnings.warn(st.session_state['key']+',Rating:Ok')
        print(st.session_state['key']+',Rating:Ok')
with cols[2]:
    if st.button('This answer is exactly right!'):
        warnings.warn(st.session_state['key']+',Rating:Good')
        print(st.session_state['key']+',Rating:Good')
