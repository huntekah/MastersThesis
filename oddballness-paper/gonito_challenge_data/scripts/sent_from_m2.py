#!/usr/bin/env python
import argparse
import difflib
from indices_from_parallel import get_indices
from tqdm import tqdm

# Apply the edits of a single annotator to generate the corrected sentences.
# Also generate file with original sentences.
def open_diffs(args):
    #create new file
    if args.out_deletions is not None:
        with open(args.out_deletions,"w") as _:
            pass
    if args.out_additions is not None:
        with open(args.out_additions,"w") as _:
            pass

def append_diffs(fh, a, b):
    diffs = []
    for token in difflib.ndiff(a,b):
        if token[0] == "+" and token[2:].isalpha():
            diffs.append(token[2:])
    fh.write(" ".join(diffs)+"\n")


def append_indices(fh,a,b):
    #diffs = [token[2:] if token[2:].isalpha() and (token[0] == "+" or token[0] == "-") for token in difflib.ndiff(a,b)]
    #print(a,"\t",b)
    indices = get_indices(a,b, policy="damerau-levenshtein")
#    diffs = [token for token in difflib.ndiff(a,b)]
#    index_a=0
#    import ipdb; ipdb.set_trace()
#    for word in diffs:
#        if word[0] == "-":
#            if len(indices) == 0 or indices[-1] != index_a:
#                index_a+=1 
#                indices.append(index_a)
#            continue
#        elif word[0] == " ":
#            index_a+=1 
#            continue
#        elif word[0] == "+":
#            if len(indices) == 0 or indices[-1] != index_a:
#                indices.append(index_a)
#            continue
#        else:
#            continue
#    ipdb.set_trace()
    #print([a[i] for i in indices])
    fh.write(" ".join([str(i) for i in indices])+"\n")
            
def handle_diffs(args, cor, orig):
    if args.out_deletions is not None:
        with open(args.out_deletions,"a") as file_handle:
            append_diffs(file_handle, cor, orig)

    if args.out_additions is not None:
        with open(args.out_additions,"a") as file_handle:
            append_diffs(file_handle, orig, cor)
#niedokończone
    if args.out_indices is not None:
        with open(args.out_indices,"a") as file_handle:
            append_indices(file_handle, orig, cor)

def main(args):
    m2 = open(args.m2_file).read().strip().split("\n\n")
    out_cor = open(args.out_cor, "w")
    out_orig = open(args.out_orig, "w")
    open_diffs(args)
    # Do not apply edits with these error types
    skip = {"noop", "UNK", "Um"}
    
    for sent in tqdm(m2):
        sent = sent.split("\n")
        orig_sent = sent[0].split()[1:] # Ignore "S "
        cor_sent = sent[0].split()[1:] # Ignore "S "
        if len(orig_sent) == 0 or len(cor_sent) == 0:
            continue
        edits = sent[1:]
        offset = 0
        for edit in edits:
            edit = edit.split("|||")
            if edit[1] in skip: continue # Ignore certain edits
            coder = int(edit[-1])
            if coder != args.id: continue # Ignore other coders
            span = edit[0].split()[1:] # Ignore "A "
            start = int(span[0])
            end = int(span[1])
            cor = edit[2].split()
            cor_sent[start+offset:end+offset] = cor
            offset = offset-(end-start)+len(cor)

        if args.only_alpha:
            cor_sent = [x for x in cor_sent if x.isalpha()]
            orig_sent = [x for x in orig_sent if x.isalpha()]
        if len(orig_sent) == 0 or len(cor_sent) == 0:
            continue
        out_cor.write(" ".join(cor_sent)+"\n")
        out_orig.write(" ".join(orig_sent)+"\n")
        handle_diffs(args, cor_sent, orig_sent)
                
if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("m2_file", help="The path to an input m2 file.")
    parser.add_argument("-out_orig", help="A path to where we save the output original text file.", required=True)
    parser.add_argument("-out_cor", help="A path to where we save the output corrected text file.", required=True)
    parser.add_argument("-id", help="The id of the target annotator in the m2 file.", type=int, default=0)    


    parser.add_argument("-out_deletions", help="A path to where we save the file with .tsv deletion differences", required=False)
    parser.add_argument("-out_additions", help="A path to where we save the file with .tsv addition differences", required=False)
    parser.add_argument("-out_indices", help="A path to where we save the file with indices representing additions and deletions", required=False)
    parser.add_argument("-only_alpha", help="If present, the output will only contain alphanumerical characters.", required=False, action='store_true')
    args = parser.parse_args()
    main(args)
