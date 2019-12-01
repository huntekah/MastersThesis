dir="../oddballness-paper/gonito_challenge_data/challenge/dev-100/"
LC_NUMERIC=C
echo -e "threshold\tMean/Multilabel-F2.0\tMean/Multilabel-F2.0\talpha" | tee -a results_gpt2.tmp
for alpha in $(seq 0.05 0.05 5.0); do
  alpha=$(echo $alpha | tr "," ".")
  result=$(python gonito_infer_gpt2.py --file ${dir}in.tsv --out ${dir}out.tsv --alpha $alpha --expected ${dir}expected.tsv)
  echo -e "${result}" | tee -a results_gpt2.tmp
done
