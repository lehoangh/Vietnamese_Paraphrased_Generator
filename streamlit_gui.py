import streamlit as st

if 'expander_1_open' not in st.session_state:
    st.session_state["expander_1_open"] = True
if 'expander_2_open' not in st.session_state:
    st.session_state["expander_2_open"] = False
if 'expander_3_open' not in st.session_state:
    st.session_state["expander_3_open"] = False
if 'original' not in st.session_state:
    st.session_state["original"] = None
if 'own' not in st.session_state:
    st.session_state["own"] = None

def plagiarism_detector():#(original, own_para):
    #todo: implement plagiarism detection
    sent1 = 'The quick brown fox jumps over the lazy dog.'
    sent2 = 'The quick brown fox jumps over the lazy cog.'
    sent3 = 'The quick brown fox jumps over the lazy dog.'
    
    st.session_state["expander_1_open"] = False
    st.session_state["expander_2_open"] = True
    st.session_state["expander_3_open"] = False
    # return [(sent1, "+"), (sent2, "-")]#, (sent3, "+")]

######################################################################################################################
with st.expander("Input your text right down here", expanded=st.session_state["expander_1_open"]):
    st.session_state["original"] = st.text_area(label="Original text")#, on_change, placeholder=)
    st.session_state["own"] = st.text_area(label="Your own paraphrased text")#, on_change, placeholder=)
    st.button('Detector & generator', on_click=plagiarism_detector())
######################################################################################################################


sent1 = 'The quick brown fox jumps over the lazy dog.'
sent2 = 'The quick brown fox jumps over the lazy cog.'
output_1 = [(sent1, "+"), (sent2, "-")]#, (sent3, "+")]

def paraphrase_generator():#(original, own_para):
    #todo: implement plagiarism detection
    st.session_state["expander_1_open"] = False
    st.session_state["expander_2_open"] = False
    st.session_state["expander_3_open"] = True
    # return [(sent1, "+"), (sent2, "-")]#, (sent3, "+")]


######################################################################################################################
with st.expander("Choose your own paraphrased sentence", expanded=st.session_state["expander_2_open"]):
    # for i in output_1:
    #     sent = i[0]
    #     plag = i[1]
    #     if plag:
    #         st.radio(sent, ["+", "-", "="])
    st.button('Save', on_click=paraphrase_generator())
######################################################################################################################    

def another_example():#(original, own_para):
    #todo: implement plagiarism detection
    st.session_state["expander_1_open"] = True
    st.session_state["expander_2_open"] = False
    st.session_state["expander_3_open"] = False
    # return [(sent1, "+"), (sent2, "-")]#, (sent3, "+")]

output_2 = []

######################################################################################################################
with st.expander("Final result", expanded=st.session_state["expander_3_open"]):
    st.write('a')
    st.button('Another example', on_click=another_example())
    