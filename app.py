from flask import Flask, request, jsonify, send_from_directory
import threading
import time
import os

from backend.vault_service import create_vault, unlock_vault, lock_vault
from backend.session import VaultSession
from backend.policy import validate_password

app = Flask(__name__, static_folder="ui")

STATE = {
    "vault_path": None,
    "mount_point": None,
    "session": None
}

def session_watcher():
    while True:
        time.sleep(2)
        session = STATE.get("session")
        if session and session.expired():
            print("[*] Session expired. Auto-locking vault.")
            try:
                lock_vault(STATE["mount_point"])
            except Exception:
                pass
            STATE["session"] = None

threading.Thread(target=session_watcher, daemon=True).start()

@app.route("/")
def index():
    return send_from_directory("ui", "unlock.html")

@app.route("/ui/<path:path>")
def ui_files(path):
    return send_from_directory("ui", path)


@app.route("/api/create", methods=["POST"])
def api_create_vault():
    data = request.json
    vault_path = data.get("path")
    password = data.get("password")

    ok, msg = validate_password(password)
    if not ok:
        return jsonify({"error": msg}), 400

    try:
        create_vault(vault_path, password)
        return jsonify({"status": "created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/unlock", methods=["POST"])
def api_unlock_vault():
    data = request.json
    vault_path = data.get("vault")
    mount_point = data.get("mount")
    password = data.get("password")

    try:
        unlock_vault(vault_path, mount_point, password)
        STATE["vault_path"] = vault_path
        STATE["mount_point"] = mount_point
        STATE["session"] = VaultSession(timeout=300)

        return jsonify({"status": "unlocked"})
    except Exception:
        return jsonify({"error": "Invalid password or vault"}), 401


@app.route("/api/lock", methods=["POST"])
def api_lock_vault():
    try:
        lock_vault(STATE["mount_point"])
    except Exception:
        pass

    STATE["session"] = None
    return jsonify({"status": "locked"})


@app.route("/api/status", methods=["GET"])
def api_status():
    if STATE["session"]:
        return jsonify({
            "locked": False,
            "expires_in": int(
                STATE["session"].timeout -
                (time.time() - STATE["session"].start)
            )
        })
    return jsonify({"locked": True})


if __name__ == "__main__":
    print("[*] Vault application starting on http://127.0.0.1:8080")
    app.run(port=8080, debug=False)
