import streamlit as st
from plagiarism_detector.check_with_search_engine import double_check

#session_state init
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
st.session_state["choosing"] = [st.write('1')]*2
if 'detector_output' not in st.session_state:
    st.session_state["detector_output"] = []

def plagiarism_detector():#(original, own_para):
    #todo: implement plagiarism detection
    # sent1 = 'The quick brown fox jumps over the lazy dog.'
    # sent2 = 'The quick brown fox jumps over the lazy cog.'
    # sent3 = 'The quick brown fox jumps over the lazy dog.'
    
    st.session_state["expander_1_open"] = False
    st.session_state["expander_2_open"] = True
    st.session_state["expander_3_open"] = False
    st.session_state["detector_output"] = double_check(st.session_state["original"], st.session_state["own"])
    st.success('Successfully detected plagiarism!')
    # return [(sent1, "+"), (sent2, "-")]#, (sent3, "+")]



##############################111111111111111111111########################################################################################
with st.expander("Input your text right down here", expanded=st.session_state["expander_1_open"]):
    st.session_state["original"] = st.text_area(label="Original text")#, on_change, placeholder=)
    st.session_state["own"] = st.text_area(label="Your own paraphrased text")#, on_change, placeholder=)
    st.button('Detector', on_click=plagiarism_detector)
######################################################################################################################





def paraphrase_generator():#(original, own_para):
    #todo: implement plagiarism detection
    st.session_state["expander_1_open"] = False
    st.session_state["expander_2_open"] = False
    st.session_state["expander_3_open"] = True
    st.session_state["detected"] = [st.session_state["own"], st.session_state["original"], st.write('2')]
    
    # return [(sent1, "+"), (sent2, "-")]#, (sent3, "+")]


##############################222222222222222222222########################################################################################
with st.expander("Choose your own paraphrased sentence", expanded=st.session_state["expander_2_open"]):
    if st.session_state["detector_output"] is not None:
        i = 0
        while i < len(st.session_state["detector_output"]):
            st.write(st.session_state["detector_output"][i][0])
            if st.session_state["detector_output"][i][1]:
                st.error('Successfully detected plagiarism!')
            else:
                st.success('Fine')
            i += 1
    st.button('Generator', on_click=paraphrase_generator)
    # st.button('Save', on_click=paraphrase_generator)
    
######################################################################################################################    

def another_example():#(original, own_para):
    #todo: implement plagiarism detection
    st.session_state["expander_1_open"] = True
    st.session_state["expander_2_open"] = False
    st.session_state["expander_3_open"] = False
    # return [(sent1, "+"), (sent2, "-")]#, (sent3, "+")]

output_2 = []

########################33333333333333333333333333333##############################################################################################
with st.expander("Final result", expanded=st.session_state["expander_3_open"]):
    st.write('a')
    st.button('Another example', on_click=another_example)
######################################################################################################################