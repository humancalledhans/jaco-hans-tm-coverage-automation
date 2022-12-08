from thefuzz import fuzz
# from thefuzz import process
from Levenshtein import distance

input_address = {
    "unit": "C-05-01",
    "floor": "",
    "building": "RUMAH PANGSA TAMAN PELANGI INDAH",
    "street": "JALAN CANTIK 7",
    "section": "TAMAN PELANGI INDAH",
    "city": "ULU TIRAM",
    "state": "JOHOR",
    "postcode": 81800
}

search_results = [
    {
        "unit": "10",
        "building": "",
        "floor": "-",
        "street": "CANTIK 7",
        "section": "TAMAN PELANGI INDAH",
        "city": "ULU TIRAM",
        "state": "JOHOR",
        "postcode": 85200
    },
    {
        "unit": "U-02-04",
        "building": "RUMAH PANGSA ZON 1F3 BLOK U",
        "floor": "2",
        "street": "CANTIK 7",
        "section": "TAMAN PELANGI INDAH",
        "city": "ULU TIRAM",
        "state": "JOHOR",
        "postcode": 81800
    },
    {
        "unit": "V-05-01",
        "building": "RUMAH PANGSA ZON 1F3 BLOK V",
        "floor": "5",
        "street": "CANTIK 7",
        "section": "TAMAN PELANGI INDAH",
        "city": "ULU TIRAM",
        "state": "JOHOR",
        "postcode": 81800
    },
    {
        "unit": "X-04-01",
        "building": "RUMAH PANGSA ZON 1F3 BLOK X",
        "floor": "4",
        "street": "CANTIK 7",
        "section": "TAMAN PELANGI INDAH",
        "city": "ULU TIRAM",
        "state": "JOHOR",
        "postcode": 81800
    }
]

def get_similarity_score(a, b, key):
    '''
    Return a score:
        0 - Not similar
        1 - Similar
        2 - Match
    '''
    # TODO: Threshold should include 3 ranges and scores can vary based on priority
    threshold = {
        "unit": [3, 95],
        "floor": [0, 100],
        "building": [3, 80],
        "street": [3, 80],
        "section": [3, 80],
        "city": [3, 90],
        "state": [3, 90],
        "postcode": [0, 100]
    }
    
    # TODO: account for synonyms

    # for spelling variations, spelling mistakes & abbreviation 
    levenshtein_dist = distance(a, b)

    # for placement of symbols, ordering of words & substring matching
    set_ratio = fuzz.token_set_ratio(a, b)

    print('Levenshtein:', levenshtein_dist, '\tTheFuzz:', set_ratio, '\n')

    # TODO: Calculate score
    levenshtein_dist_threshold, set_ratio_threshold = threshold[key]
    score = 2 if levenshtein_dist <= levenshtein_dist_threshold or set_ratio >= set_ratio_threshold else 0

    return score

for result in search_results:
    score = 0
    for key in result:
        print(key)
        print('a)', input_address[key], '\nb)', result[key])
        score += get_similarity_score(str(input_address[key]), str(result[key]), key)
    print("Score: ", score)