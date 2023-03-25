def decomposition(paragraph):
    sentences = paragraph.split('.')
    output_list = []
    for s_k, sent in enumerate(sentences):
        words = sent.split(' ')
        output_dict = {}
        output = {}
        for w_k, word in enumerate(words):
            make_key = str(w_k) #+ '_' + word
            output[make_key] = word
        output_dict[s_k] = output
        output_list.append(output_dict)
    return sentences, output_list


import re
def classification(form):
    s_keys = []
    key_list = []
    point_list = []
    
    for k in form.keys():
        s_keys.append(k)
        
    for s_k in s_keys:
        value = form[s_k]
        
        md = re.sub('\n', '', value)
        md = re.sub('\r', '', md)
        
        k_p = re.compile(f'(?<=\"KeyHighlight_{s_k}">)(.*?)(?=<\/span>)')
        p_p = re.compile(f'(?<=\"PointHighlight_{s_k}">)(.*?)(?=<\/span>)')
        
        key_list = k_p.findall(md)
        point_list = p_p.findall(md)
        
    return key_list, point_list

# Load KoGPT Tokenizer
# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained(
#     'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',  # or float32 version: revision=KoGPT6B-ryan1.5b
#     bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
#     )

# Deconposition : paragraph -> token
# def decomposition(paragraph):
#     sentences = paragraph.split('.')
#     output_list = []
#     for s_k, sent in enumerate(sentences):
#         input_idx = tokenizer.encode(sent)
#         output = {}
#         for w_k, i in enumerate(input_idx):
#             out = tokenizer.decode(i)
#             make_key = str(s_k) + '_' + str(w_k) + '_' + out
#             output[make_key] = out
#         output_list.append(output)
#     return output_list


# KoBERT Tokenizer
# from kobert.utils import get_tokenizer
# from kobert.pytorch_kobert import get_pytorch_kobert_model

# import gluonnlp as nlp

# bertmodel, vocab = get_pytorch_kobert_model()
# tokenizer = get_tokenizer()
# tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)