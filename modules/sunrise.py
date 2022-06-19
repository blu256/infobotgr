TEXT = "Και μια ηλιόλουστη μέρα ξεκινάει!"
PSTR = "sunrise_last_post_id"

def get(statusfile):
    post = {
        "text":         TEXT,
        "store_id":     PSTR,
        "media":
        {
            "file":     "modules/media/sunrise.mp4",
            "mime":     "video/mp4",
            "desc":     TEXT
        }
    }

    # Πρέπει να διαγράψουμε το προηγούμενο ποστ
    last_post = statusfile.get(PSTR)
    if last_post is not None:
        post["delete"] = [last_post]

    return [post]