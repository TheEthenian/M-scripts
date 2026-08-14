yt-dlp -f "bv[height<=720]+ba/b[height>=480]" \
       --external-downloader aria2c \
       --external-downloader-args "aria2c:-j 16 -x 16 -s 16 -k 1M" \
       -o "%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s" \
       --ignore-errors \
  	"https://youtube.com/playlist?list=PL9kOpGJcHGmnSMrrYYLvNDWGU_tyow2Bk&si=LY59oQyn0SSxTJB8"
