from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/extract", methods=["GET"])
def extract():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {"quiet": True, "skip_download": True}
    formats_list = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get("title", "Unknown")
            thumbnail = info.get("thumbnail", "")

            for f in info.get("formats", []):
                if f.get("url"):
                    formats_list.append({
                        "quality": f.get("format_note"),
                        "ext": f.get("ext"),
                        "url": f.get("url")
                    })

        return jsonify({
            "title": title,
            "thumbnail": thumbnail,
            "formats": formats_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
