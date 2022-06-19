from idebug import color

ERROR_PREFIXES = {
    "error": color("error", "Σφάλμα:"),
    "warn":  color("warn",  "Προειδοποίηση:")
}

def error(msg, exit = 0):
    global ERROR_PREFIXES
    if exit:
        prefix = ERROR_PREFIXES["error"]
    else:
        prefix = ERROR_PREFIXES["warn"]

    print("{} {}".format(prefix, msg))
    if exit:
        quit(exit)