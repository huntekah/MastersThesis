transformers.GPT2Config has a parameter n_positions (and n_ctx) that defines how many positional embeddings may go into model. Usually set to 1024, mabey it should be adjusted according to the text length?

transformers.GPT2Tokenizer - Requires a space to start the input string => the encoding methods should be called with the add_prefix_space flag set to True. Otherwise, this tokenizer encode and decode method will not conserve the absence of a space at the beginning of a string: tokenizer.decode(tokenizer.encode(“Hello”)) = ” Hello”


special tokens:
	[DOCS]class GPT2Tokenizer(PreTrainedTokenizer):
    """
    GPT-2 BPE tokenizer. Peculiarities:
        - Byte-level Byte-Pair-Encoding
        - Requires a space to start the input string => the encoding methods should be called with the
          ``add_prefix_space`` flag set to ``True``.
          Otherwise, this tokenizer ``encode`` and ``decode`` method will not conserve
          the absence of a space at the beginning of a string: `tokenizer.decode(tokenizer.encode("Hello")) = " Hello"`
    """
    vocab_files_names = VOCAB_FILES_NAMES
    pretrained_vocab_files_map = PRETRAINED_VOCAB_FILES_MAP
    max_model_input_sizes = PRETRAINED_POSITIONAL_EMBEDDINGS_SIZES

    def __init__(self, vocab_file, merges_file, errors='replace', unk_token="<|endoftext|>",
                 bos_token="<|endoftext|>", eos_token="<|endoftext|>", **kwargs)

l:)


encode( add_special_tokens – if set to True, the sequences will be encoded with the special tokens relative to their model.


