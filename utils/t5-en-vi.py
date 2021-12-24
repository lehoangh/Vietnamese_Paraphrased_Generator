import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import pandas as pd
from tqdm import tqdm
import csv
import os.path
import pandas as pd



def load_checkpoint_index():
    if os.path.isfile('checkpoint_index.txt'):
        print ("output file File exist")
    else:
        print ("File not exist, create new data file")
        f = open("checkpoint_index.txt", "w")
        f.write(f'0')
        f.close()
        
    f = open("checkpoint_index.txt", "r")
    index = int(f.read())
    f.close()
    return index

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

if os.path.isfile('train_vi.csv'):
    print ("output file File exist")
else:
    print ("File not exist, create new data file")
    new_df = pd.DataFrame(columns = ['index','sentence1','sentence2'])
    new_df.to_csv('train_vi.csv',index = False)

resume_extract_index = load_checkpoint_index()
    
src_path = 'train_ready.csv'
if resume_extract_index != 0:
    resume_extract_index += 1
df = pd.read_csv(src_path)[resume_extract_index:]
df_output = pd.DataFrame(df['annotator_labels'])
sentence1_list = []
sentence2_list = []
df_output_iter = pd.DataFrame(columns = ['index','sentence1','sentence2'])
for index, row in tqdm(df.iterrows()):
    sentence1 = row['sentence1']
    sentence2 = row['sentence2']

    tokenized_text = tokenizer.encode(sentence1, return_tensors="pt").to(device)
    model.eval()
    try:
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
    except:
        f = open("errors_log.txt", "a")
        f.write(f'{str(index)}---{sentence1},{sentence2}')
        f.close()
#     sentence1_list.append(output1)
#     sentence2_list.append(output2)
    df_output_iter['index'] = [index]
    df_output_iter['sentence1'] = [str(output1)]
    df_output_iter['sentence2'] = [str(output2)]
    df_output_iter.to_csv('train_vi.csv', mode='a', header=False, index = False)
    f = open("checkpoint_index.txt", "w")
    f.write(f'{str(index)}')
    f.close()
    
# df_output['sentence1'] = sentence1_list
# df_output['sentence2'] = sentence2_list
# df_output.to_csv('train_vi.csv', index=False)