from collections import defaultdict
from configuration import *


def generate_misspells():
    """
    This Function will inverted index for correcting misspells.
    :return: Inverted Index will be written to 'misspell_inverted_index.string'
    """
    # english words that are sometime mixed up.
    # todo: build a common vocabulary
    not_allowed_variants = ["want", "kon"]
    keyword_misspells = {}

    # load all user defined mis-spells
    with open(misspell_keywords_file, "r") as o_file:
        lines = o_file.read().split("\n")
        for line in lines:  # line format:"balance: blnc, blance"
            keyword = line.split(":")[0]
            variations = line.split(":")[1].split(",")
            keyword_misspells[keyword] = variations

    # avoid swapping of original keywords as variant to others
    not_allowed_variants += keyword_misspells.keys()
    # add algorithm generated typos to dict
    for keyword in keyword_misspells.keys():
        print("processing: '{}'...".format(keyword))
        all_words = [keyword] + keyword_misspells[keyword]
        all_variations = []
        for word in all_words:
            all_variations += get_typos([word])
        keyword_misspells[keyword] = all_variations + keyword_misspells[keyword]

    # we don't need further variation for these words
    keyword_misspells['hello'] = ['hello', 'helo', 'helu', 'hallo', 'halo']

    # write inverted index to default_dict
    print("generating inverted index...")
    inverted_index = defaultdict(lambda: [])
    for keyword in keyword_misspells.keys():
        for variant in keyword_misspells[keyword]:
            if variant.lower().strip() not in not_allowed_variants:
                inverted_index[variant.lower().strip()] = keyword
            else:
                print("skipping variant ({}) for keyword ({})".format(variant, keyword))

    d = dict(inverted_index)
    file_handler = open(misspell_inverted_index_file, 'w')
    file_handler.write(str(d))
    file_handler.close()


if __name__ == "__main__":
    generate_misspells()
