import streamlit as st
from plagiarism_detector.check_with_search_engine import double_check
import pickle
import torch
from Generator.load_model2 import load_model_2
from Generator.model2_inference import model2_inference
from Generator.load_model1 import load_model_1
# from Generator.model1_inference import model1_inference


#load generator model 1
# chk_pt_path = r'Generator\ckpt_seq2seq\seq2seq_237.pt'
# model_best, tokenize_vi, SRC_saved, TRG_saved, spacy_vi, device = load_model_1(chk_pt_path)
# #load generator model 2
# translation_model, translation_tokenizer, para_model, para_tokenizer, en_vi_model, en_vi_tokenizer, device = load_model_2()

#session_state init
if 'expander_1_open' not in st.session_state:
    st.session_state["expander_1_open"] = True
if 'expander_2_open' not in st.session_state:
    st.session_state["expander_2_open"] = False
if 'expander_3_open' not in st.session_state:
    st.session_state["expander_3_open"] = False
if 'expander_4_open' not in st.session_state:
    st.session_state["expander_4_open"] = False
if 'original' not in st.session_state:
    st.session_state["original"] = None
if 'own' not in st.session_state:
    st.session_state["own"] = None
st.session_state["choosing"] = [st.write('1')]*2
if 'detector_output' not in st.session_state:
    st.session_state["detector_output"] = []
if 'generated' not in st.session_state:
    st.session_state["generated"] = []

def plagiarism_detector():#(original, own_para):
    st.session_state["expander_1_open"] = False
    st.session_state["expander_2_open"] = True
    st.session_state["expander_3_open"] = False
    st.session_state["expander_4_open"] = False
    st.session_state["detector_output"] = double_check(st.session_state["original"], st.session_state["own"])



##############################111111111111111111111########################################################################################
with st.expander("Input your text right down here", expanded=st.session_state["expander_1_open"]):
    st.session_state["original"] = st.text_area(label="Original text")#, on_change, placeholder=)
    st.session_state["own"] = st.text_area(label="Your own paraphrased text")#, on_change, placeholder=)
    st.button('Detector', on_click=plagiarism_detector)
######################################################################################################################


def combine_inferences():
    generated_list =  []
    if st.session_state["detector_output"] is not None:
        i = 0
        while i < len(st.session_state["detector_output"]):
            if st.session_state["detector_output"][i][1]:
                generatet_sent_1 = model2_inference(st.session_state["detector_output"][i][0])
                generatet_sent_2 = model2_inference(st.session_state["detector_output"][i][0], translation_model, translation_tokenizer, para_model, para_tokenizer, en_vi_model, en_vi_tokenizer, device)
                generated_list.append(generatet_sent)
                generated_list.append((st.session_state["detector_output"][i][0]), generatet_sent_1+generatet_sent_2) 
            else:
                continue
            i += 1
    return generated_list


def paraphrase_generator():#(original, own_para):
    #todo: implement plagiarism detection
    st.session_state["expander_1_open"] = False
    st.session_state["expander_2_open"] = False
    st.session_state["expander_3_open"] = True
    st.session_state["expander_4_open"] = False
    #TODO: implement paraphrase generator
    
    


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

def save_result():#(original, own_para):
    #todo: implement plagiarism detection
    st.session_state["expander_1_open"] = False
    st.session_state["expander_2_open"] = False
    st.session_state["expander_3_open"] = False
    st.session_state["expander_4_open"] = True
    st.session_state["generated"] = combine_inferences()


########################33333333333333333333333333333##############################################################################################
with st.expander("Final result", expanded=st.session_state["expander_3_open"]):
    if st.session_state["generated"] is not None:
        i = 0
        while i < len(st.session_state["generated"]):
            st.write(st.session_state["generated"][i][0])
            st.radio(st.session_state["generated"][i][1][:3])
    st.button('Save', on_click=save_result)
######################################################################################################################

def save_result():#(original, own_para):
    #todo: implement plagiarism detection
    st.session_state["expander_1_open"] = True
    st.session_state["expander_2_open"] = False
    st.session_state["expander_3_open"] = False
    st.session_state["expander_4_open"] = False


##############################111111111111111111111########################################################################################
with st.expander("Final result", expanded=st.session_state["expander_4_open"]):
    # st.session_state["original"] = st.text_area(label="Original text")#, on_change, placeholder=)
    # st.session_state["own"] = st.text_area(label="Your own paraphrased text")#, on_change, placeholder=)
    st.button('Another example', on_click=save_result)
######################################################################################################################