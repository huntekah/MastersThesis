#dir="../oddballness-paper/gonito_challenge_data/challenge/dev-0/"
dir="../oddballness-paper/challenge_v6.2/dev-0/";
LC_NUMERIC=C
complexity=20
file_name=results_gpt2_exhaustive_${complexity}.tmp
. ./CONFIG.exhaustive.sh
echo -e "threshold\tMean/Multilabel-F2.0\tMean/Multilabel-F2.0\talpha" | tee -a $file_name
for alpha in $(seq $START $STEP $STOP); do
  alpha=$(echo $alpha | tr "," ".")
  result=$(python gonito_infer_gpt2_exhaustive.py --file ${dir}in.tsv --out ${dir}out.tsv --alpha $alpha --detokenized ${dir}in_detokenized.tsv  --expected ${dir}expected.tsv --complexity ${complexity})
  echo -e "${result}" | tee -a $file_name
done
