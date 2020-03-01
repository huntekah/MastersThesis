dir="../oddballness-paper/challenge_v6.2/dev-0/";

LC_NUMERIC=C

complexity=${1:-20}
file_name=results_gpt2_exhaustive_${complexity}.tmp
rm -f $file_name
START=${2:-0.75}
#STOP=2.0
STOP=${3:-1.25}
STEP=${4:-0.05}
#. ./CONFIG.exhaustive.sh
#dir="../oddballness-paper/challenge_v6.2/dev-1/";

echo -e "threshold\talpha\tMean/MultiLabel-F0.5\tMean/MultiLabel-F2\tF0.5\tF2\tAccFstError\tAccAnyError" | tee -a $file_name
for alpha in $(seq $START $STEP $STOP); do
  alpha=$(echo $alpha | tr "," ".")
  result=$(python gonito_infer_gpt2_exhaustive.py --file ${dir}in.tsv --out ${dir}out.tsv --alpha $alpha --detokenized ${dir}in_detokenized.tsv  --expected ${dir}expected.tsv --complexity ${complexity})
  echo -e "${result}" | tee -a $file_name
done

