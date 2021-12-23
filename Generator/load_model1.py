import random
import torch
import torchtext
import torch.nn as nn
import pickle
from pyvi import ViTokenizer
import spacy



def tokenize_vi(text, spacy_vi):
    """
    Tokenizes Vietnamese text from a string into a list of strings (tokens)
    """
    return [tok.text for tok in spacy_vi.tokenizer(text)]

class Encoder(nn.Module):
    def __init__(self, input_dim, emb_dim, enc_hid_dim,n_layers, dropout, SRC_saved):
        super().__init__()

        self.emb_dim = emb_dim
        self.enc_hid_dim = enc_hid_dim
        self.dropout = dropout
        self.n_layers = n_layers

        # self.embedding = nn.Embedding(input_dim, emb_dim)
        # further you can now make use of your pretrained embeddings inside your model by passing them in
        # as a parameter or loading the handy pickle file mentioned above - a much better design pattern
        # indeed than relying on TEXT.build_vocab() in order to define the embedding layer of your model
        self.embedding = nn.Embedding.from_pretrained(SRC_saved.vocab.vectors, freeze=False)
        # freeze=True <-> self.embedding.requires_grad = False, not learn in training
        # SRC.vocab.vectors, freeze=False

        self.lstm = nn.LSTM(emb_dim, enc_hid_dim, n_layers, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, src):
        
        #src = [src len, batch size]
        
        embedded = self.dropout(self.embedding(src))
        
        #embedded = [src len, batch size, emb dim]
        
        outputs, (hidden, cell) = self.lstm(embedded)
        
        return hidden, cell

class Decoder(nn.Module):
    def __init__(self, output_dim, emb_dim, dec_hid_dim, n_layers, dropout, TRG_saved):
        super().__init__()

        self.emb_dim = emb_dim
        self.output_dim = output_dim
        self.dec_hid_dim = dec_hid_dim
        self.n_layers = n_layers
        self.dropout = dropout

        # self.embedding = nn.Embedding(output_dim, emb_dim)
        self.embedding = nn.Embedding.from_pretrained(TRG_saved.vocab.vectors, freeze=False)
        # self.embedding.requires_grad = False
        self.lstm = nn.LSTM(emb_dim, dec_hid_dim, n_layers, dropout=dropout)
        self.fc_out = nn.Linear(dec_hid_dim, output_dim)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, input, hidden, cell):
        
        input = input.unsqueeze(0)
        
        embedded = self.dropout(self.embedding(input))
        
        #embedded = [1, batch size, emb dim]    
        output, (hidden, cell) = self.lstm(embedded, (hidden, cell))
        
        # predicted shape is [batch_size, output_dim]
        prediction = self.fc_out(hidden.squeeze(0))
        
        return prediction, hidden, cell

class Seq2Seq(nn.Module):
    ''' 
    Args:
        encoder: A Encoder class instance.
        decoder: A Decoder class instance.
    '''
    def __init__(self, encoder, decoder, device):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device

    def forward(self, src, trg, teacher_forcing_ratio=0.5):
        batch_size = trg.shape[1]
        max_len = trg.shape[0]
        trg_vocab_size = self.decoder.output_dim

        # to store the outputs of the decoder
        outputs = torch.zeros(max_len, batch_size, trg_vocab_size).to(self.device)

        hidden, cell = self.encoder(src)

        # first input to the decoder is the <sos> tokens
        input = trg[0, :]

        for t in range(1, max_len):
            output, hidden, cell = self.decoder(input, hidden, cell)
            outputs[t] = output
            use_teacher_force = random.random() < teacher_forcing_ratio
            top1 = output.max(1)[1]
            input = (trg[t] if use_teacher_force else top1)

        # outputs is of shape [sequence_len, batch_size, output_dim]
        return outputs



def load_model_1(CHECK_POINT_PATH, src_field="TRG.Field", trg_field="SRC.Field"):

    '''
    load fields saved during preprocessing
    '''
    with open(src_field,"rb") as f:
        TRG_saved = pickle.load(f)

    with open(trg_field,"rb") as f:
        SRC_saved = pickle.load(f)

    '''
    hyperparameters (ensure the following hyperparameters match with those used during training of the best model)
    '''
    
    INPUT_DIM = len(SRC_saved.vocab)
    OUTPUT_DIM = len(TRG_saved.vocab)
    ENC_EMB_DIM = 300
    DEC_EMB_DIM = 300
    ENC_HID_DIM = 512
    DEC_HID_DIM = 512
    ENC_DROPOUT = 0.5
    DEC_DROPOUT = 0.5
    N_LAYERS = 1
    # CHECK_POINT_PATH = f'ckpt_seq2seq/seq2seq_{n_ckpt}.pt'

    # set the device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    '''
    tokenization code
    '''

    spacy_vi = spacy.load('vi_core_news_lg')
    '''
    instantiate the model
    '''
    enc = Encoder(INPUT_DIM, ENC_EMB_DIM, ENC_HID_DIM, N_LAYERS, ENC_DROPOUT, SRC_saved)
    dec = Decoder(OUTPUT_DIM, DEC_EMB_DIM, DEC_HID_DIM, N_LAYERS, DEC_DROPOUT, TRG_saved)
    model_best = Seq2Seq(enc, dec, device).to(device)
    
    model_best.load_state_dict(torch.load(CHECK_POINT_PATH)['state_dict'])
    model_best = model_best.to(device)
    
    return model_best, tokenize_vi, SRC_saved, TRG_saved, spacy_vi, device

