dir="../oddballness-paper/gonito_challenge_data/challenge/dev-100/";
LC_NUMERIC=C
for thr in 0.5 0.2 0.1 0.01 0.001 0.0008 0.0006 0.0004 0.00035 0.0003 0.00025 \
0.00024 0.00023 0.00022 0.00021 0.0002 0.00019 0.00018 0.00017 0.00016 0.00015 \
0.0001 0.00008 0.00006 0.00004 0.00002 0.00001 0.000001 0.0000001 0.00000001 0.000000001;
do
    thr=$(echo $thr | tr "," ".")
    python gonito_infer_gpt2_probability_baseline.py --threshold $thr --file ${dir}in.tsv  --out ${dir}out.tsv ;
    score=$(geval -t $dir --metric MultiLabel-F0.5 --metric MultiLabel-F2 --precision 6 | tr "\n" "\t")
    echo -e "$score\t\tthreshold=$thr" | tee -a results_baseline.tmp
done
