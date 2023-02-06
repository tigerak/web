from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    'kakaobrain/kogpt', revision='KoGPT6B-ryan1.5b-float16',  # or float32 version: revision=KoGPT6B-ryan1.5b
    bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
    )

def decomposition(sentence):
    input_idx = tokenizer.encode(sentence)
    output = []
    for i in input_idx:
        out = tokenizer.decode(i)
        output.append(out)
    return output