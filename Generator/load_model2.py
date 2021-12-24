from transformers import (
    T5Tokenizer,
    T5ForConditionalGeneration
)

import torch

def load_model_2():
    if torch.cuda.is_available():       
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    # Load module dịch vi-en
    translation_model = T5ForConditionalGeneration.from_pretrained("NlpHUST/t5-vi-en-base")
    translation_tokenizer = T5Tokenizer.from_pretrained("NlpHUST/t5-vi-en-base")
    translation_model.to(device)

    # Load mô hình en-paraphrase
    para_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_paraphraser')
    para_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_paraphraser')
    para_model = para_model.to(device)

    # Load mô hình dịch en-vi
    en_vi_model = T5ForConditionalGeneration.from_pretrained("NlpHUST/t5-en-vi-base")
    en_vi_tokenizer = T5Tokenizer.from_pretrained("NlpHUST/t5-en-vi-base")
    en_vi_model.to(device)
    return translation_model, translation_tokenizer, para_model, para_tokenizer, en_vi_model, en_vi_tokenizer, device