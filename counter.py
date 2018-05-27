import re


def count_unique_words(text):
    """
    This function counts unique words in string ignoring case,
    i.e. 'Word', 'WORD', 'word' represent the same word
    :param text: str
    :return: int
    """

    # set contain only unique values
    # it is easy and really fast way to count unique values
    unique_words = set(
        # there W means [^a-zA-Z0-9_]  + UNICODE, so strings like
        # '___', 'one_two_three' will be calculated as only one word
        (word for word in re.split('\W+', text) if word)
    )

    print(re.split('\W+', text))

    return len(unique_words)


# print(count_unique_words('lol kek'))
# print(count_unique_words(',. &'))
# print(count_unique_words('lol, kekos, kek, lul, lol?'))
# print(count_unique_words('lol kek kek kek , kek, lol'))
# print(count_unique_words('Як тобі таке, Ілон_Маск __?___'))
