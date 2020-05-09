LC_NUMERIC=C
complexity=${1:-20}
threshold=${2:-0.98739}
alpha=${3:-1.3}
challenge_dir="../oddballness-paper/challenge_v6.2/";
results_dir="${challenge_dir}/gpt2-oddballness-exhaustive-XL-a${alpha}-t${threshold}-c${complexity}"
mkdir -p $results_dir

for folder in dev-0 test-A; do
	dir="${challenge_dir}/${folder}/"
	mkdir -p $results_dir/$folder
	$(python gonito_infer_gpt2_exhaustive.py --file ${dir}in.tsv --out ${results_dir}/${folder}/out.tsv --alpha $alpha --threshold $threshold --complexity ${complexity} --detokenized ${dir}in_detokenized.tsv )
	echo Result for "${folder}" saved to "${results_dir}"
done
