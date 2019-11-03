#!/usr/bin/bash
ORIG='orig.txt'
DELS='dels'
tmp_file=$(mktemp)
trap 'rm -f -- "$tmp_file"' INT TERM HUP EXIT

paste -d'\t' $ORIG $DELS | shuf -o $tmp_file

#split -l $[ $(wc -l $tmp_file|cut -d" " -f1) * 80 / 100 ] $tmp_file
cat $tmp_file | head -n 61049 > train.tmp
trap 'rm -f -- train.tmp' INT TERM HUP EXIT
cat $tmp_file | tail -n +61050 | head -n 7631  > dev-0.tmp
trap 'rm -f -- dev-0.tmp' INT TERM HUP EXIT
cat $tmp_file | tail -n +68681  > test-A.tmp
trap 'rm -f -- test-A.tmp' INT TERM HUP EXIT

for name in train dev-0 test-A ; do
    echo $name
    cat $name.tmp | cut -f1 > $name/in.txt
    cat $name.tmp | cut -f2- > $name/out.tsv
    rm -f -- "$name.tmp"
done

rm -f -- "$tmp_file"

