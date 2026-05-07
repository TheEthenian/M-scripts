yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
    --merge-output-format mp4 \
    --external-downloader aria2c \
    --external-downloader-args "-c -j 4 -x 16 -s 16 -k 5M" \
    "https://youtu.be/iuYg6hVpkPs?si=4cpTqJoLBaVgsVEw"
