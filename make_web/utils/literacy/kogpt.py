def decomposition(paragraph):
    sentences = paragraph.split('.')
    output_list = []
    sent_dic = {}
    for s_k, sent in enumerate(sentences):
        words = sent.split(' ')
        output = {}
        for w_k, word in enumerate(words):
            make_key = str(s_k) + '_' + str(w_k) #+ '_' + word
            output[make_key] = word
        output_list.append(output)
    return sentences, output_list

# from transformers import AutoTokenizer

# Load KOGPT Tokenizer
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
