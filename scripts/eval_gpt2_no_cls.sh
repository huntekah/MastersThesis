LC_NUMERIC=C
alpha=4.85
threshold=0.909
challenge_dir="../oddballness-paper/gonito_challenge_data/challenge"
results_dir="${challenge_dir}/gpt2-oddballness-no-bos-a${alpha}-t${threshold}"
mkdir -p $results_dir

for folder in dev-0 test-A; do
	dir="${challenge_dir}/${folder}/"
	mkdir -p $results_dir/$folder
	python gonito_infer_gpt2.py --file ${dir}in.tsv --out ${results_dir}/${folder}/out.tsv --alpha $alpha --threshold $threshold
	echo Result for "${folder}" saved to "${results_dir}"
done
