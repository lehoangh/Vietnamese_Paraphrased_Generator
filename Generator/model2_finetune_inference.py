from time import time
from vi_tokenizer import tokenize_vi
from load_model2_finetune import model, tokenizer, device


def generate_paraphrase(sentence):
    # Tokenize Vietnamese language
    tokenized_sent = " ".join(tokenize_vi(sentence))

    max_len = 256

    start_time = time()
    encoding = tokenizer.encode_plus(tokenized_sent,pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)

    # set top_k = 50 and set top_p = 0.95 and num_return_sequences = 3
    beam_outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        do_sample=True,
        max_length=256,
        top_k=120,
        top_p=0.98,
        # early_stopping_callback=False,
        num_return_sequences=5
    )

    print ("\nOriginal sentence: ")
    print (sentence)
    print ("\n")
    print ("Paraphrased sentences: ")
    final_outputs =[]
    for beam_output in beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        if sent.lower() != sentence.lower() and sent not in final_outputs:
            final_outputs.append(sent)  

    for i, final_output in enumerate(final_outputs):
        print("{}: {}".format(i, final_output))
    print(time()-start_time)