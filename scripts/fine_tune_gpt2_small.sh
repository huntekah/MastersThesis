#dir="../oddballness-paper/gonito_challenge_data/challenge/dev-0/";
dir="../oddballness-paper/challenge_v6/dev-small/";
LC_NUMERIC=C
#echo -e "threshold\tMean/Multilabel-F2.0\tMean/Multilabel-F2.0\talpha" | tee -a results_gpt2.tmp

echo -e "threshold\talpha\tMean/MultiLabel-F0.5\tMean/MultiLabel-F2\tF0.5\tF2\tAccFstError\tAccAnyError" | tee -a results_gpt2_small.tmp
for alpha in $(seq 0.95 0.10 7.0); do
  alpha=$(echo $alpha | tr "," ".")
  result=$(python gonito_infer_gpt2_2.py --file ${dir}in.tsv --out ${dir}out.tsv --alpha $alpha --detokenized ${dir}in_detokenized.tsv --expected ${dir}expected.tsv)
  echo -e "${result}" | tee -a results_gpt2_small.tmp
done
