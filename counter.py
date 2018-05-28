import re


def count_unique_words(text):
    """
    This function counts unique words in string ignoring case,
    i.e. 'Word', 'WORD', 'word' represent the same word
    :param text: str
    :return: int
    """

    words = re.split('\W+', text)
    print(words)
    # words list may contain empty string only at the begin or/and
    # at the end if text has leading or trailing spaces
    # the fastest way to delete empty string is to check only
    # first and last element of the list directly by index
    # words list will contain at least one non-empty string
    # so conditions below should not crash program

    # first
    if not words[0]:
        del words[0]

    # last
    if not words[-1]:
        del words[-1]

    # set contain only unique values (we use lower() to ignore case)
    # it is easy and really fast way to count unique values
    unique_words = set(
        # there W means [^a-zA-Z0-9_]  + UNICODE, so strings like
        # '___', 'one_two_three' will be calculated as only one word
        # also we use generator expression to save more memory
        (word.lower() for word in words)
    )

    return len(unique_words)


# print(count_unique_words('lol kek'))
# print(count_unique_words(',. &'))
# print(count_unique_words('lol, kekos, kek, lul, lol?'))
# print(count_unique_words('lol kek kek kek , kek, lol'))
# print(count_unique_words('Як тобі таке, Ілон_Маск __?___'))
