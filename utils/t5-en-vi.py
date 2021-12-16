import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pandas as pd
from tqdm import tqdm


if torch.cuda.is_available():       
    device = torch.device("cuda")

    print('There are %d GPU(s) available.' % torch.cuda.device_count())

    print('We will use the GPU:', torch.cuda.get_device_name(0))
else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")

model = T5ForConditionalGeneration.from_pretrained("NlpHUST/t5-en-vi-base")
tokenizer = T5Tokenizer.from_pretrained("NlpHUST/t5-en-vi-base")
model.to(device)
src_path = 'train_ready.csv'
df = pd.read_csv(src_path)
df_output = pd.DataFrame(df['annotator_labels'])
sentence1_list = []
sentence2_list = []
for _, row in tqdm(df.iterrows()):
    sentence1 = row['sentence1']
    sentence2 = row['sentence2']

    tokenized_text = tokenizer.encode(sentence1, return_tensors="pt").to(device)
    model.eval()
    summary_ids = model.generate(
                        tokenized_text,
                        max_length=128, 
                        num_beams=5,
                        repetition_penalty=2.5, 
                        length_penalty=1.0, 
                        early_stopping=True
                    )
    output1 = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    tokenized_text = tokenizer.encode(sentence2, return_tensors="pt").to(device)
    model.eval()
    summary_ids = model.generate(
                        tokenized_text,
                        max_length=128, 
                        num_beams=5,
                        repetition_penalty=2.5, 
                        length_penalty=1.0, 
                        early_stopping=True
                    )
    output2 = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    sentence1_list.append(output1)
    sentence2_list.append(output2)
df_output['sentence1'] = sentence1_list
df_output['sentence2'] = sentence2_list
df_output.to_csv('train_vi.csv', index=False)