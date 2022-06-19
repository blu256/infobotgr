COLORS = {
    "reset":         "\033[0m",
    "error":         "\033[91m",
    "warn":          "\033[93m",
    "preview_media": "\033[104m",
    "preview_cw":    "\033[103m\033[30m"
}

def color(col, txt):
    return COLORS[col] + txt + COLORS['reset']

def ruler(stop = 40, char = '-'):
    return char * stop

class DebugClient:
    def status_post(self, text, **kwargs):
        print("\n" + ruler(10) + " ΠΡΟΕΠΙΣΚΟΠΙΣΗ ΑΝΑΡΤΗΣΗΣ " + ruler(10))

        if 'spoiler_text' in kwargs.keys() and kwargs['spoiler_text'] is not None:
            print(color("preview_cw", "CW: {}").format(kwargs['spoiler_text']))

        if 'media_ids' in kwargs.keys() and kwargs['media_ids'] is not None:
            print(color("preview_media", "Συνημμένα πολυμέσα"))

        print(text)
        print(ruler(45))


    def media_post(self, filename, **kwargs):
        print("(υποβολή πολυμέσου: {})".format(filename))