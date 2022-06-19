from os.path import isfile
import json

from ierror import error


_STATUSFILE=".infobot_status"
_DATA = {}

def load():
    global _STATUSFILE, _DATA

    # Δημιουργία αν δεν υπάρχει
    if not isfile(_STATUSFILE):
        h = open(_STATUSFILE, "a")
        h.close()
        return

    # Προσπαθούμε να ανοίξουμε το αρχείο
    try:
        h = open(_STATUSFILE, "r")
    except IOError as e:
        error("Κατά την ανάγνωση του αρχείου καταστάσεων: ".format(e.strerror),
                100 + e.errno)

    # Διαβάζουμε τα δεδομένα
    try:
        _DATA = json.loads(h.read())
    except ValueError as e:
        error("Κακώς δομημένα δεδομένα JSON: " + e.strerror, 3)

    h.close()
    del h

def write():
    global _STATUSFILE, _DATA
    try:
        h = open(_STATUSFILE, "w")
    except IOError as e:
        error("Κατά την εγγραφή του αρχείου καταστάσεων: ".format(e.strerror),
                100 + e.errno)

    h.write(json.dumps(_DATA))
    h.close()
    del h

def get(key):
    global _DATA
    if not key in _DATA.keys():
        return None
    return _DATA[key]

def set(key, value):
    global _DATA
    _DATA[key] = value