#!/usr/bin/bash
corpora_dir="corpora"
wil_tgz="wil.tar.gz"
wil_dir=$corpora_dir/"wil"
fce_tgz="fce.tar.gz"
fce_dir=$corpora_dir/"fce"
challenge_dir="challenge"
scripts_dir="scripts"

function download_corpora(){
    mkdir $corpora_dir
    get_wi_lockness
    get_fce
}

function get_wi_lockness(){
    wget https://www.cl.cam.ac.uk/research/nl/bea2019st/data/wi+locness_v2.1.bea19.tar.gz -O $corpora_dir/$wil_tgz
    tar -xzvf $corpora_dir/$wil_tgz -C $corpora_dir --one-top-level=wil --strip-components 1
    rm -- $corpora_dir/$wil_tgz
}

function get_fce(){
    wget https://www.cl.cam.ac.uk/research/nl/bea2019st/data/fce_v2.1.bea19.tar.gz -O $corpora_dir/$fce_tgz
    tar -xzvf $corpora_dir/$fce_tgz -C $corpora_dir --one-top-level=fce --strip-components 1
    rm -- $corpora_dir/$fce_tgz
}

function combine_m2_files(){
 all_m2_files="all.m2"

 for m2_file in $corpora_dir/*/m2/*.m2; do
     cat $m2_file >> $all_m2_files
 done
 rm -rf -- $corpora_dir
}

function extract_text_from_m2(){
    local OUT_ORIG='original.txt'
    local OUT_COR='corrected.txt'
    local OUT_INDICES='indices.tsv'
    #local OUT_DELETIONS='deletions.tsv'
    #local OUT_ADDITIONS='additions.tsv' #
    echo sent_from_m2.py \
        -out_orig $OUT_ORIG \
        -out_cor $OUT_COR \
        -out_indices $OUT_INDICES \
        -only_alpha \
        $all_m2_files   # omit --only_alpha parameter to include punctuation marks.
    ./$scripts_dir/sent_from_m2.py \
        -out_orig $OUT_ORIG \
        -out_cor $OUT_COR \
        -out_indices $OUT_INDICES \
        -only_alpha \
        $all_m2_files 
    rm -f -- "$all_m2_files" "$OUT_COR"
}

function split_data(){
    local ORIG='original.txt'
    local INDICES='indices.tsv'

    ./$scripts_dir/split_data.sh $ORIG $INDICES
    rm -f -- "$ORIG" "$INDICES"
}

function move_data_to_new_directory(){
    local dir="$1"
    rm -rf $dir
    mkdir -p $dir
    for f in train dev-0 test-A ; do
        mv $f $dir/.
    done
}

function create_required_challenge_files(){
    local challenge_prefix="challenge_"
    #cp .README.md README.md
    echo "Creating gitignore, README.md and config.txt"
    for file in README.md .gitignore config.txt ; do
        cp $challenge_prefix$file $challenge_dir/$file
    done
    
}

function main(){
    download_corpora
    combine_m2_files
    extract_text_from_m2
    split_data
    move_data_to_new_directory $challenge_dir
    create_required_challenge_files
}

main
echo "All done, your challenge is ready in $challenge_dir"
