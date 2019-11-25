dir="../oddballness-paper/gonito_challenge_data/challenge/dev-100/";
LC_NUMERIC=C
for alpha in $(seq 0.5 0.13 5); do
    for thr in $(seq 0.05 0.03 0.99); do
        alpha=$(echo $alpha | tr "," ".")
        thr=$(echo $thr | tr "," ".")
        python gonito_infer_bert.py --alpha $alpha --threshold $thr --file ${dir}in.tsv  --out ${dir}out.tsv ; 
        score=$(geval -t $dir --metric MultiLabel-F0.5 --metric MultiLabel-F2 --precision 8 | tr "\n" "\t")
        echo -e "$score\talpha=$alpha\tthreshold=$thr" | tee -a results_bert_aprox.tmp
    done
done
