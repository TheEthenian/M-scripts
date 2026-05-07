yt-dlp -f "bestvideo[height<=480]+bestaudio/best[height<=480]" \
  --downloader aria2c \
  --downloader-args "aria2c:-x 16 -s 16 -k 1M" \
  -o "%(playlist_index)03d-%(title)s.%(ext)s" \
  "https://youtube.com/playlist?list=PL9kOpGJcHGmmbpiEQQc1fDDlWn6KJVxDb&si=S_-VmPP65SapdXIN"
