from flask import Flask, request, jsonify
from threading import Thread
from libretranslatepy import LibreTranslateAPI

app = Flask("LibreTranslateServer")

lt = LibreTranslateAPI("https://libretranslate.de")  # initial server (can be offline, fallback will work locally)

@app.route("/translate", methods=["POST"])
def translate():
    try:
        text = request.form.get("q")
        source = request.form.get("source", "auto")
        target = request.form.get("target", "fr")
        if not text:
            return jsonify({"error": "No text provided"}), 400
        translated = lt.translate(text, source, target)
        return jsonify({"translatedText": translated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run():
    app.run(host="0.0.0.0", port=5000)

# Run server in a thread
Thread(target=run).start()
