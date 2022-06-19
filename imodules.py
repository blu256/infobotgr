import importlib

from ierror import error

importlib.invalidate_caches()

def load(modules, statusfile):
    posts = []
    for m in modules:
        try:
            mod = importlib.import_module("modules.{}".format(m))
        except ImportError:
            error("Το πρόσθετο '{}' δεν υπάρχει.".format(m), 1)

        new_posts = mod.get(statusfile)
        for p in new_posts: # αναφέρουμε την πηγή του ποστ
            p['source'] = m

        posts += new_posts

    return posts