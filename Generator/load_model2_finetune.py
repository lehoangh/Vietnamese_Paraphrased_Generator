# Torch==1.5.0
import torch
from transformers import (
    T5ForConditionalGeneration,
    AutoTokenizer
)

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(42)

# Directory contains checkpoint model: save_check_point
best_model_path = "save_check_point"
model = T5ForConditionalGeneration.from_pretrained(best_model_path, 
                                                  #  output_attentions=True
                                                   )
tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base', 
                                            #  use_fast=False
                                             )

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device ",device)
model = model.to(device)