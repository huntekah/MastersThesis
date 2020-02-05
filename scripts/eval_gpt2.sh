LC_NUMERIC=C
#alpha=1.15
#threshold=0.909
thresholds=(	0.234375	0.375	0.421875	0.8125	0.828125)
alphas=(	1.15	1.25	1.25	1.05	1.05)

#thresholds=(	0.8125)
#alphas=(	1.05)

challenge_dir="../oddballness-paper/challenge_v6.2/";

for idx in "${!thresholds[@]}";do
	alpha=${alphas[$idx]}
	threshold=${thresholds[$idx]}
	echo threshold $threshold alpha $alpha

	results_dir="${challenge_dir}/gpt2-oddballness-a${alpha}-t${threshold}"
	mkdir -p $results_dir

	for folder in dev-0 test-A; do
		dir="${challenge_dir}/${folder}/"
		mkdir -p $results_dir/$folder
		python gonito_infer_gpt2.py --file ${dir}in.tsv --out ${results_dir}/${folder}/out.tsv --alpha $alpha --threshold $threshold --detokenized ${dir}in_detokenized.tsv
		echo Result for "${folder}" saved to "${results_dir}"
	done

done

