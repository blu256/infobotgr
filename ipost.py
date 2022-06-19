from os import environ, unlink

from ierror import error
from idebug import DebugClient

try:
    from mastodon import Mastodon, MastodonIllegalArgumentError
except ImportError:
    print("Σφάλμα: παρακαλώ εγκαταστήστε τη βιβλιοθήκη Mastodon.py")
    print("\n\t$ pip install Mastodon.py")
    exit(2)


_debug  = False
_client = None
_status = None

def init_client():
    try:
        access_token = environ['ACCESS_TOKEN']
    except KeyError:
        error("Χρειάζεστε ένα access token για πρόσβαση στο λογαριασμό.\n\
    \tΟρίστε τη μεταβλητή περιβάλλοντος ACCESS_TOKEN και ξαναπροσπαθήστε.", 4)

    return Mastodon(
        access_token = access_token,
        api_base_url = 'https://botsin.space'
    )

def set_debug(d):
    global _debug
    _debug = d

def set_statusfile(s):
    global _status
    _status = s

def post_all(pl):
    for p in pl:
        post(p)

def post(p):
    global _client, _debug, _status

    if _client is None:
        if not _debug:
            _client = init_client()
        else:
            _client = DebugClient()

    # Πρώτα πρώτα ανεβάζουμε τα πολυμέσα, αν υπάρχουν
    if 'media' in p.keys():
        media_id = post_media(p['media'])
        if media_id == None:
            error("Αδύνατη η υποβολή του αρχείου '{}', το ποστ δεν θα αναρτηθεί.".format(p['media']['file']))
            return
        p['media_ids'] = media_id
        del p['media']

    opts = {'cw': None, 'media_ids': None}
    for o in opts.keys():
        if o in p.keys():
            opts[o] = p[o]

    print("[{}] Υποβολή ανάρτησης...".format(p['source']))
    post = _client.status_post(p['text'],
        spoiler_text = opts['cw'],
        media_ids    = opts['media_ids'],
        language     = "gre",
        visibility   = "public",
        sensitive    = False
    )

    # Αν χρειάζεται, διαγράφουμε παλιές ειδοποιήσεις
    # Χρήσιμο αν ένα ποστ αντικαθιστά ένα άλλο και επιτρέπει επαναχρησιμοποίηση
    # των ίδιων πολυμέσων
    if 'delete' in p.keys() and not _debug:
        for i in p['delete']:
            print("[{}] Διαγραφή προηγούμενου ποστ...".format(p['source']))
            _client.status_delete(i)

    if 'store_id' in p.keys() and not _debug:
        _status.set(p['store_id'], post['id'])



def post_media(p):
    global _client, _debug, _status

    print("Υποβολή αρχείου: {}...".format(p['file']))

    opts = {'mime': None, 'desc': None}
    for o in opts.keys():
        if o in p.keys():
            opts[o] = p[o]

    try:
        m = _client.media_post(p['file'], opts['mime'], opts['desc'])
    except MastodonIllegalArgumentError as e:
        error("Σφάλμα κατά την υποβολή αρχείου: {}".format(e.errorstr), 10)
        return None

    return -1 if _debug else m['id']