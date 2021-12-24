# Dịch lại sang câu tiếng việt
def translation_en_vi(sentence_list, en_vi_model, en_vi_tokenizer, device):
    output_list = []
    for sentence in sentence_list:
        # print("check: ", sentence)
        tokenized_text = en_vi_tokenizer.encode(sentence, return_tensors="pt").to(device)
        en_vi_model.eval()
        summary_ids = en_vi_model.generate(
                            tokenized_text,
                            max_length=128, 
                            num_beams=1,
                            repetition_penalty=2.5, 
                            length_penalty=1.0, 
                            early_stopping=True
                        )
        output = en_vi_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        # print(output)
        output_list.append(output)
    return output_list

# Translate câu sang tiếng anh
def translation_vi_en(sentence, translation_model, translation_tokenizer, device):
    tokenized_text = translation_tokenizer.encode(sentence, return_tensors="pt").to(device)
    translation_model.eval()
    summary_ids = translation_model.generate(
                        tokenized_text,
                        max_length=256, 
                        num_beams=5,
                        repetition_penalty=2.5, 
                        length_penalty=1.0, 
                        early_stopping=True
                    )
    output = translation_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    # print(output)
    return output

def en_paraphrase(sentence, para_tokenizer, para_model, device):
    text =  "paraphrase: " + sentence + " </s>"

    max_len = 256

    encoding = para_tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)


    # set top_k = 50 and set top_p = 0.95 and num_return_sequences = 3
    beam_outputs = para_model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        do_sample=True,
        max_length=256,
        top_k=120,
        top_p=0.98,
        early_stopping=True,
        num_return_sequences=10
    )


    # print ("\nOriginal Question ::")
    # print (sentence)
    # print ("\n")
    # print ("Paraphrased Questions :: ")
    final_outputs =[]
    for beam_output in beam_outputs:
        sent = para_tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        if sent.lower() != sentence.lower() and sent not in final_outputs:
            final_outputs.append(sent)

    # for i, final_output in enumerate(final_outputs):
    #     print("{}: {}".format(i, final_output))

    return final_outputs

def model2_inference(sentence, translation_model, translation_tokenizer, en_vi_model, en_vi_tokenizer, para_model, para_tokenizer, device):
    en_sent = translation_vi_en(sentence, translation_model, translation_tokenizer, device)
    en_para_lst = en_paraphrase(en_sent, para_tokenizer, para_model, device)
    vi_sent_lst = translation_en_vi(en_para_lst, en_vi_model, en_vi_tokenizer, device)
    return vi_sent_lst[0]