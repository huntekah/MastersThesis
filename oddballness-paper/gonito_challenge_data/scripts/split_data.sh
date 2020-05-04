#!/usr/bin/bash
ORIG="$1"
INDICES="$2"
tmp_file=$(mktemp)
trap 'rm -f -- "$tmp_file"' INT TERM HUP EXIT

paste -d'\t' $ORIG $INDICES | shuf -o $tmp_file


all_lines=$(wc -l $tmp_file | cut -d" " -f1)

train_lines=$[$all_lines * 80 / 100 ]
dev_lines=$[$all_lines * 10 / 100 ]
#test_lines=$[$all_lines * 10 / 100 ]

dev_start=$[0 + $train_lines + 1]
test_start=$[$dev_start + $dev_lines + 1  ]

cat $tmp_file | head -n $train_lines > train.tmp
trap 'rm -f -- train.tmp' INT TERM HUP EXIT
cat $tmp_file | tail -n +$dev_start | head -n $dev_lines  > dev-0.tmp
trap 'rm -f -- dev-0.tmp' INT TERM HUP EXIT
cat $tmp_file | tail -n +$test_start  > test-A.tmp
trap 'rm -f -- test-A.tmp' INT TERM HUP EXIT

for name in dev-0 test-A train ; do
    echo $name
    mkdir -p $name
    cat $name.tmp | cut -f1 > $name/in.tsv
    cat $name.tmp | cut -f2- > $name/expected.tsv
    rm -f -- "$name.tmp"
done

#cat train.tmp | cut -f1 > train.in.tmp
#cat train.tmp | cut -f2 > train.expected.tmp
#mkdir -p train
#paste train.expected.tmp train.in.tmp > train/train.tsv
rm -f -- "train.in.tmp" "train.expected.tmp" "train.tmp"

rm -f -- "$tmp_file"

