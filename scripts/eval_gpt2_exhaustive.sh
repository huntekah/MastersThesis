LC_NUMERIC=C
alpha=1.3
threshold=0.98739
complexity=20
challenge_dir="../oddballness-paper/gonito_challenge_data/challenge"
results_dir="${challenge_dir}/gpt2-oddballness-exhaustive-a${alpha}-t${threshold}"
mkdir -p $results_dir

for folder in dev-0 test-A; do
	dir="${challenge_dir}/${folder}/"
	mkdir -p $results_dir/$folder
	readlink -f .
	$(python gonito_infer_gpt2_exhaustive.py --file ${dir}in.tsv --out ${results_dir}/${folder}/out.tsv --alpha $alpha --threshold $threshold --complexity ${complexity})
	echo Result for "${folder}" saved to "${results_dir}"
done
