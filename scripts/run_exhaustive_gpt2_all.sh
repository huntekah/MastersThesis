#!/bin/bash
#1. choose parameter of complexity
#2. for each complexity do:
#	3. create fine tune results
#	4. for each best result perform evaluation
#		5. copy over out.tsv files
#		6. prepare gonito.yaml file
#		7. commit and push to gonito

main() {

	clone_gonito_repo
	#1. choose parameter of complexity
	max_complexity="$1"

	#2. for each complexity do:
	for complexity in $(seq $max_complexity -1 2); do
		#3. create fine tune results
		./fine_tune_gpt2_exhaustive.sh $complexity 0.5 2.0 0.05 #0.5 2.0 0.05
		file_name=results_gpt2_exhaustive_${complexity}.tmp

		#4. for each best result perform evaluation
		for col in $(seq 3 8); do
			
			optimized_for=$(head -n1 "$file_name" | cut -f${col})
			read t a <<<"$(cat $file_name | sort -nr -k$col,$col | head -n1 | cut -f1,2)"
			./eval_gpt2_exhaustive.sh "$complexity" "$t" "$a"
			#5. copy over out.tsv files
			#6. prepare gonito.yaml file
			copy_out_files_to_gonito_challenge "$complexity" "$t" "$a" "$optimized_for"
			#7. commit and push to gonito
			commit_and_push_to_gonito "$optimized_for" "$complexity"
		done
	done
}

clone_gonito_repo() {
	wd=$(pwd)
	echo $HOME is home.
	repo=$HOME"/repos/GED_TASK"
	rm -rf $repo
	mkdir -p $HOME"/repos"
	git clone --single-branch -- ssh://gitolite@gonito.net/huntekah/grammatical-error-detection $repo;
	$(cd $repo;
	#git pull git://gonito.net/grammatical-error-detection

	git config user.name "anon-0654f8b176c00a8a"
	git config user.email "anon-0654f8b176c00a8a@wp.pl"
	git pull origin master
	git checkout -b automatic-submissions
)
	cd $wd
}

copy_out_files_to_gonito_challenge() {
	c="$1"
	t="$2"
	a="$3"
	optimized_for="$4"
	repo=$HOME"/repos/GED_TASK"
	wd=$(pwd)

	#5. copy over out.tsv files
	for folder in dev-0 test-A; do
		# TODO change after tests!
		cp "../oddballness-paper/challenge_v6.2/gpt2-oddballness-exhaustive-XL-a${a}-t${t}-c${c}/${folder}/out.tsv" ${repo}/${folder}/out.tsv
		#cp "../oddballness-paper/challenge_v6.2/gpt2-oddballness-exhaustive-XL-a${a}-t${t}-c${c}/dev-1/out.tsv" ${repo}/${folder}/out.tsv
		$(cd $repo; git add ${repo}/${folder}/out.tsv)
	done

	#6. prepare gonito.yaml file
	cat << EOF > ${repo}/gonito.yaml
description: gpt2 oddballness bidirectional
tags:
      - oddballness
      - bidirectional
      - gpt2-xl
params:
      - optimizedfor: ${optimized_for}
      - alpha: ${a}
      - threshold: ${t}
      - complexity: ${c}
EOF

	$(cd $repo; git add ${repo}/gonito.yaml)
}

commit_and_push_to_gonito() {
	optimized_for="$1"
	complexity="$2"
	repo=$HOME"/repos/GED_TASK"
	wd=$(pwd)
	cd $repo
	git commit -m "Automatic submission for gpt2-xl bidirectional (exhaustive) with $complexity complexity, optimized for $optimized_for" --allow-empty
	git push --dry-run origin automatic-submissions
	cd $wd
}

main "$@"
