#!/usr/bin/env python

from detokenize import Detokenizer
import sys
from indices_from_parallel import get_indices 
from tqdm import tqdm
import string

def get_diffs(a, b):
    for i in max(len(a),len(b)):
        i = 0
        j = 0
        res = []
        while True:
            if a[i] == b[j]:
                i+=1
                j+=1
            else:
                k = 0
                if j+1 > len(b):
                    k = len(a) - i
                else: 
                    while a[i+k] != b[j+1] and i+k < len(a):
                        k+=1
                res.append((" ".join(a[i:i+k-1]),b[j]))
                i+=k
                j+=1
    return res 

#a = [1,23,4,5,678]
#b = [1,2,3,4,5,6,7,8]
#print(get_diffs(a,b))


#a = [1,234,56]
#b = [1,2,3,4,5,6,7,8,9,10,11,12]
#print(get_diffs(a,b))      


if __name__ == "__main__":
    detokenizer = Detokenizer()
    #changes = []
    lines = sys.stdin.readlines()
    for line in tqdm(lines):
        orig = line.split()
        changed = detokenizer(orig)
        if orig != changed : 
            indices = get_indices(orig,changed)
            orig_words = [orig[i] for i in indices]
            indices = get_indices(changed,orig)
            changed_words = [changed[i] for i in indices]
            i = 0
            l = 0
            orig_sent = ""
            for word in orig_words:
                l+=len(word)
                orig_sent += f" {word}"
                if l == len(changed_words[i]):
                    if len(orig_sent.split()) == 2 and orig_sent.split()[1] in string.punctuation:
                        continue
                    print(orig_sent,"\t->\t",changed_words[i], flush=True) 
                    i+=1
                    l=0
                    orig_sent = ""
            #print(orig[indices])
            #print(changed[indices])

