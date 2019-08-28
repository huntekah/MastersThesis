# run this script in order to download 40GB of raw text data from the web
# source: https://skylion007.github.io/OpenWebTextCorpus/

show_help(){
    echo "$(basename "$0") [-s, --small] [-b, --big, -f, --full] [-h, --help]"
    echo "this script will download corpora that this project was trained on."
    echo ""
    exit 0
}


google_drive_download () {
    echo "Attempting to download OpenWebText data from googledrive with id $1"
    CONFIRM=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=$1" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$CONFIRM&id=$1" -O $2
    rm -rf /tmp/cookies.txt
}

get_small_sample(){
    google_drive_download "1gFU2UXCnVRPfd0YB6K9-4ARMLONJRhOE" subset.tar
}

get_full_corpus() {
    google_drive_download "1EA5V0oetDCOke7afsktL_JDQ-ETtNOvx" openwebtext.tar.xz
}

main() {
    for i in "$@"; do
        case $i in
            -s|--small)
                get_small_sample
                shift
                ;;
            -f|--full|-b|--big)
                get_full_corpus
                shift
                ;;
            -h|--help|*)
                show_help
                shift
                ;;
         esac
    done
}

main "$@"

