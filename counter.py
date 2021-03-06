import re


def count_unique_words(text):
    """
    This function counts unique words in string ignoring case,
    i.e. 'Word', 'WORD', 'word' represent the same word
    :param text: str
    :return: int
    """
    if not text:  # None or ''
        raise ValueError('Note should contain text!')

    # there W means [^a-zA-Z0-9_]  + UNICODE, so strings like
    # '___', 'one_two_three' will be calculated as only one word
    words = re.split('\W+', text)

    # words list may contain empty string only at the begin or/and
    # at the end if text has leading or trailing spaces
    # the fastest way to delete empty string is to check only
    # first and last element of the list directly by index
    # splitting of spaces-string (' ') return ['', ''], splitting of
    # non-spaces-string return list with at least one non-space value
    # so conditions below should not crash program

    # first
    if not words[0]:
        del words[0]

    # last
    if not words[-1]:
        del words[-1]

    # set contain only unique values (we use lower() to ignore case)
    # it is easy and really fast way to count unique values
    unique_words = set(word.lower() for word in words)

    return len(unique_words)
