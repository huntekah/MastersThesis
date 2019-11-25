dir="../oddballness-paper/gonito_challenge_data/challenge/dev-100/";
LC_NUMERIC=C
for alpha in $(seq 0.5 0.1 3); do
    for thr in $(seq 0.1 0.05 1); do
        alpha=$(echo $alpha | tr "," ".")
        thr=$(echo $thr | tr "," ".")
        python gonito_infer.py --alpha $alpha --threshold $thr --file ${dir}in.tsv  --out ${dir}out.tsv ; 
        score=$(geval -t $dir --metric MultiLabel-F0.5 --precision 4)
        echo -e "$score\talpha=$alpha\tthreshold=$thr" | tee -a results.tmp
    done
done
