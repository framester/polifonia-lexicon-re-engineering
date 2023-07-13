from nltk.corpus import wordnet as wn

def resolve_pos_full_from_short(pos_short):
    pos_short_to_pos_full = {
        "n": "noun",
        "v": "verb",
        "a": "adjective",
        "r": "adverb"
    }
    
    return pos_short_to_pos_full.get(pos_short, None)


def get_wn_synset_uri(wn_synset_id):
    pos = wn_synset_id[-1]
    offset = wn_synset_id[3:-1]
    synset = wn.synset_from_pos_and_offset(wn_synset_id[-1], int(wn_synset_id[3:-1]))
    name = synset.name().split(".")[0]
    pos = resolve_pos_full_from_short(pos)
    return f"synset-{name}-{pos}-{offset}"

