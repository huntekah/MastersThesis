dir="../oddballness-paper/gonito_challenge_data/challenge/dev-0/";
LC_NUMERIC=C
python gonito_infer_gpt2_probability_baseline.py --file ${dir}in.tsv  --out ${dir}out.tsv --expected ${dir}expected.tsv ;
    score=$(geval -t $dir --metric MultiLabel-F0.5 --metric MultiLabel-F2 --precision 6 | tr "\n" "\t")
    echo -e "$thr\t$score" | tee -a results_baseline_mean.tmp
