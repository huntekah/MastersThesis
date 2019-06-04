# run this script in order to download 40GB of raw text data from the web
# source: https://skylion007.github.io/OpenWebTextCorpus/


google_drive_download () {
    echo "Attempting to download OpenWebText data from googledrive with id $1"
    CONFIRM=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=$1" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
    wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$CONFIRM&id=$1" -O $2
    rm -rf /tmp/cookies.txt
}

main() {
    #google_drive_download "1IaD_SIIB-K3Sij_-JjWoPy_UrWqQRdjx" openwebtext.tar.xz
    google_drive_download "1EA5V0oetDCOke7afsktL_JDQ-ETtNOvx" openwebtext.tar.xz

}

main

