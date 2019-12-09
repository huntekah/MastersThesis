dir="../oddballness-paper/gonito_challenge_data/challenge/dev-0/"
LC_NUMERIC=C
complexity=20
file_name=results_gpt2_exhaustive_${complexity}.tmp
echo -e "threshold\tMean/Multilabel-F2.0\tMean/Multilabel-F2.0\talpha" | tee -a $file_name
for alpha in $(seq 3.75 0.05 10.0); do
  alpha=$(echo $alpha | tr "," ".")
  result=$(python gonito_infer_gpt2_exhaustive.py --file ${dir}in.tsv --out ${dir}out.tsv --alpha $alpha --expected ${dir}expected.tsv --complexity ${complexity})
  echo -e "${result}" | tee -a $file_name
done
