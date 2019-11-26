dir="../oddballness-paper/gonito_challenge_data/challenge/dev-0/";
LC_NUMERIC=C
for alpha in $(seq 0.25 0.25 4); do
      alpha=$(echo $alpha | tr "," ".")
      thr=$(python gonito_infer_gpt2.py --file ${dir}in.tsv --out ${dir}out.tsv --alpha $alpha --expected ${dir}expected.tsv)
      #python gonito_infer_bert.py --alpha $alpha --threshold $thr --file ${dir}in.tsv  --out ${dir}out.tsv ;
      score=$(geval -t $dir --metric MultiLabel-F0.5 --metric MultiLabel-F2 --precision 8 | tr "\n" "\t")
      echo -e "threshold=$thr\t$score\talpha=$alpha" | tee -a results_gpt2.tmp
done
