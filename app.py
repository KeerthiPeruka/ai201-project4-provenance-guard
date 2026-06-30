from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import uuid

from detection import groq_detection_score, stylometric_score
from scoring import combine_scores, get_attribution
from labels import get_label
import storage

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Provenance Guard API is running."
    })


@app.route("/submit", methods=["POST"])
@limiter.limit("10 per minute;100 per day")
def submit():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON request."}), 400

    if "creator_id" not in data or "text" not in data:
        return jsonify({"error": "creator_id and text are required."}), 400

    creator_id = data["creator_id"]
    text = data["text"]
    content_id = str(uuid.uuid4())

    groq_score = groq_detection_score(text)
    heuristic_score = stylometric_score(text)
    confidence = combine_scores(groq_score, heuristic_score)

    attribution = get_attribution(confidence)
    label = get_label(attribution)
    status = "classified"

    submission = {
        "content_id": content_id,
        "creator_id": creator_id,
        "text": text,
        "attribution": attribution,
        "confidence": confidence,
        "label": label,
        "status": status,
        "signals": {
            "groq_score": groq_score,
            "heuristic_score": heuristic_score
        }
    }

    storage.save_submission(content_id, submission)

    storage.create_audit_entry({
        "event_type": "classification",
        "content_id": content_id,
        "creator_id": creator_id,
        "attribution": attribution,
        "confidence": confidence,
        "label": label,
        "status": status,
        "signals": {
            "groq_score": groq_score,
            "heuristic_score": heuristic_score
        }
    })

    return jsonify(submission)


@app.route("/appeal", methods=["POST"])
def appeal():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON request."}), 400

    if "content_id" not in data or "creator_reasoning" not in data:
        return jsonify({
            "error": "content_id and creator_reasoning are required."
        }), 400

    content_id = data["content_id"]
    creator_reasoning = data["creator_reasoning"]

    submission = storage.get_submission(content_id)
    if submission is None:
        return jsonify({"error": "Content ID not found."}), 404

    submission["status"] = "under_review"
    submission["appeal_reasoning"] = creator_reasoning

    storage.create_audit_entry({
        "event_type": "appeal",
        "content_id": content_id,
        "creator_id": submission["creator_id"],
        "status": "under_review",
        "appeal_reasoning": creator_reasoning,
        "original_attribution": submission["attribution"],
        "confidence": submission["confidence"],
        "signals": submission["signals"]
    })

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Appeal received and content marked as under review."
    })


@app.route("/log", methods=["GET"])
def log():
    return jsonify({
        "entries": storage.get_log()
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)