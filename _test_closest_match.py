from thefuzz import fuzz
# from thefuzz import process
from Levenshtein import distance
import json

class ClosestMatch:

    def __init__(self, input_address, search_results) -> None:
        self.input_address = input_address
        self.search_results = search_results

    def get_closest_match(self, method=1):
        closest_match = None
        max_score = -1
        max_score_count = 0

        for result in self.search_results:
            score = 0

            if method == 1:
                for key in result:
                    # print(key)
                    # print('a)', input_address[key], '\nb)', result[key])
                    score += self._scoring_method_1(str(self.input_address[key]), str(result[key]), key)
            elif method == 2:
                score = self._scoring_method_2(self.input_address, result)
            else:
                raise ValueError("Invalid method request. Check your function call.")

            if score > max_score:
                closest_match = result
                max_score = score
                max_score_count = 1
            elif score == max_score:
                max_score_count += 1

        return closest_match, max_score_count

    def _scoring_method_1(self, a, b, key):
        '''
        Return a score:
            0 - Not similar
            1 - Similar
            2 - Match
        Uses thresholds with levenshtein distance and fuzzy logic
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

    def _scoring_method_2(self, input_address, comparison_address):
        '''
        Return a score.
        Uses a dictionary for matching individual words.
        '''
        occurence_map = {}

        # populate the dictionary with words from input address
        # TODO: consider spelling variations
        for key in input_address:
            token = str(input_address[key])
            for word in token.split(' '):
                if word and word not in occurence_map:
                    occurence_map[word] = 0
        
        # increment score for every word that appears in the comparison address
        for key in comparison_address:
            token = str(comparison_address[key])
            for word in token.split(' '):
                if word and word in occurence_map:
                    occurence_map[word] += 1
        
        return sum(occurence_map.values())

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

cm = ClosestMatch(input_address, search_results)
closest_address_match, score_repetitions = cm.get_closest_match(method=2)
print(score_repetitions, 'addresses had the same score/ \nHere is the closest match:\n', json.dumps(closest_address_match, indent=4))