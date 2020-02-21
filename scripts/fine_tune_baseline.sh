#dir="../oddballness-paper/gonito_challenge_data/challenge/dev-0/";
dir="../oddballness-paper/challenge_v6.2/dev-0/";
LC_NUMERIC=C
#Mean/MultiLabel-F0.5 Mean/MultiLabel-F2 F0.5 F2 AccFstError AccAnyError
echo -e "threshold\tMean/MultiLabel-F0.5\tMean/MultiLabel-F2\tF0.5\tF2\tAccFstError\tAccAnyError\talpha" | tee -a results_baseline_mean_probability.tmp2
result=$(python gonito_infer_gpt2_probability_baseline.py --file ${dir}in.tsv  --out ${dir}out.tsv --detokenized ${dir}in_detokenized.tsv --expected ${dir}expected.tsv );
#python gonito_infer_gpt2_probability_baseline.py --file ${dir}in.tsv  --out ${dir}out.tsv --expected ${dir}expected.tsv
#score=$(geval -t $dir --metric MultiLabel-F0.5 --metric MultiLabel-F2 --precision 6 | tr "\n" "\t")
echo -e "$result" | tee -a results_baseline_mean_probability.tmp2
