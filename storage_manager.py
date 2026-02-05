import os
import datetime
import json
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DB_PATH = os.path.join(BASE_DIR, "uploads_db.json")


def _load_uploads_db(path):
    """
    Safely load uploads_db.json
    Handles:
    - file not existing
    - empty file
    - corrupted JSON
    """
    if not os.path.exists(path):
        return {"users": []}

    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if not content:
                return {"users": []}
            return json.loads(content)
    except json.JSONDecodeError:
        return {"users": []}


def save_user_upload(user_id, username, image_file_path, geo_location,
                     uploads_db_path=UPLOADS_DB_PATH):

    print("✅ save_user_upload CALLED")
    print("📁 Saving uploads DB at:", os.path.abspath(uploads_db_path))

    # ---- Validate image path ----
    if not os.path.exists(image_file_path):
        print("❌ Image path does NOT exist:", image_file_path)
        return

    # ---- Create user upload folder ----
    user_dir = os.path.join(BASE_DIR, "uploads", username)
    os.makedirs(user_dir, exist_ok=True)

    filename = os.path.basename(image_file_path)
    saved_image_path = os.path.join(user_dir, filename)

    # ---- Copy image safely ----
    shutil.copy(image_file_path, saved_image_path)
    print("✅ Image copied to:", saved_image_path)

    # ---- Create upload entry ----
    upload_entry = {
        "image_id": f"{username}_{int(datetime.datetime.now().timestamp())}",
        "image_path": saved_image_path,
        "timestamp": datetime.datetime.now().isoformat(),
        "geo_location": geo_location,
        "status": "uploaded"
    }

    # ---- Load DB safely ----
    data = _load_uploads_db(uploads_db_path)

    # ---- Insert upload under correct user ----
    for user in data["users"]:
        if user["username"] == username:
            user.setdefault("uploads", []).append(upload_entry)
            break
    else:
        data["users"].append({
            "username": username,
            "user_id": user_id,
            "uploads": [upload_entry]
        })

    # ---- Save DB ----
    with open(uploads_db_path, "w") as f:
        json.dump(data, f, indent=4)

    print("✅ uploads_db.json UPDATED SUCCESSFULLY")


def get_user_uploads(username, uploads_db_path=UPLOADS_DB_PATH):
    """
    Fetch all uploads for a user safely.
    """
    data = _load_uploads_db(uploads_db_path)

    for user in data["users"]:
        if user["username"] == username:
            return user.get("uploads", [])

    return []
