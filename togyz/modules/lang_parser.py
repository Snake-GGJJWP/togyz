MARK_TO_TAG = {
    '*': ('<b>', '</b>'),
    '`': ('<i>', '</i>')
}


def mdtext_to_HTML(s):
    # *sample* - bold text
    # `sample` - italic text
    # *`sample`* - bold + italic

    last = ''
    last_ind = -1
    for i in range(len(s)):
        if s[i] in MARK_TO_TAG:
            if not last:
                last = s[i]
                last_ind = i
            elif last == s[i]:
                s = s[:i] + MARK_TO_TAG[s[i]][1] + s[i + 1:]
                s = s[:last_ind] + MARK_TO_TAG[s[last_ind]][0] + s[last_ind + 1:]
                last = ''
                last_ind = -1
    return s


def format_data(data):
    for key, value in data.items():
        data[key] = mdtext_to_HTML(value)
    return data
