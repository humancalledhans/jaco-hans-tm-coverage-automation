# 	# JALAN	CANTIK 7	TAMAN PELANGI INDAH	2	RUMAH PANGSA ZON 1F3 BLOK U	ULU TIRAM	JOHOR	81800
# from thefuzz import fuzz
# # from thefuzz import process
# from Levenshtein import distance

# # actual data for 1369
# a_db1 = "RUMAH PANGSA TAMAN PELANGI INDAH"
# a_web1 = "RUMAH PANGSA ZON 1F3 BLOK U"

# # mock data with section repositioned
# a_db2 = "TAMAN PELANGI INDAH RUMAH PANGSA"
# a_web2 = "RUMAH PANGSA TAMAN PELANGI INDAH"

# # actual concat data for 1369 (sec & bld)
# a_db3 = "RUMAH PANGSA TAMAN PELANGI INDAH"
# a_web3 = "RUMAH PANGSA ZON 1F3 BLOK U TAMAN PELANGI INDAH"

# # spelling variation
# x1 = "RUMAH PANGSA"
# x2 = "ROMAH PANGSA"

# # placement of symbols
# y1 = "C-11-01"
# y2 = "C/11 01"

# # spelling mistake
# z1 = "RUMAH PANGSA"
# z2 = "RUMA PANGSER"

# a_db = a_db3
# a_web = a_web3

# print("levenshtein:", distance(a_db, a_web))
# print("ratio:", fuzz.ratio(a_db, a_web))
# print("partial_ratio:", fuzz.partial_ratio(a_db, a_web))
# print("token_sort_ratio:", fuzz.token_sort_ratio(a_db, a_web))
# print("token_set_ratio:", fuzz.token_set_ratio(a_db, a_web))

# def get_variations(token:str):
# 	"""Generates possible variations of an address token

# 	Args:
# 		token (string): address token

# 	Returns:
# 		[string]: an array of token variations, empty if token is ''
# 	"""
# 	# token doesn't exist
# 	if not token:
# 		return []

# 	# TODO: generate variations
# 	token_split = token.split(' ')
# 	_helper(token_split)

# 	return [token]

# def _helper(word_list, level=0):
# 	# map of words and all their possible variations as a list
# 	variation_map = {
# 		'Commercial': ['Commercial', 'Komersial'],
# 		'Residency': ['Residency', 'Residensi'],
# 		'Tower': ['Tower', 'Menara'],
# 		'Complex': ['Complex', 'Kompleks'],
# 		'Bagian': ['Bagian', 'BHG'],
# 		'Bukit': ['Bukit', 'BKT'],
# 		'Jabatan': ['Jabatan', 'JAB'],
# 		'Jalan': ['Jalan', 'JLN'],
# 		'Kawasan': ['Kawasan', 'KAW'],
# 		'Kementerian': ['Kementerian', 'KEM'],
# 		'Ladang': ['Ladang', 'LDG'],
# 		'Lembaga': ['Lembaga', 'LEM'],
# 		'Lorong': ['Lorong', 'LRG'],
# 		'Padang': ['Padang', 'PDG'],
# 		'Persiaran': ['Persiaran', 'PSN'],
# 		'Sungai': ['Sungai', 'SG'],
# 		'Simpang': ['Simpang', 'SPG'],
# 		'Tanjung': ['Tanjung', 'TG'],
# 		'Teluk': ['Teluk', 'TK'],
# 		'Taman': ['Taman', 'TMN'],
# 		'Jalan': ['Jalan', 'JLN'],
# 		'Komersial': ['Komersial', 'Commercial'],
# 		'Residensi': ['Residensi', 'Residency'],
# 		'Menara': ['Menara', 'Tower'],
# 		'Kompleks': ['Kompleks', 'Complex'],
# 		'BHG': ['BHG', 'Bagian'],
# 		'BKT': ['BKT', 'Bukit'],
# 		'JAB': ['JAB', 'Jabatan'],
# 		'JLN': ['JLN', 'Jalan'],
# 		'KAW': ['KAW', 'Kawasan'],
# 		'KEM': ['KEM', 'Kementerian'],
# 		'LDG': ['LDG', 'Ladang'],
# 		'LEM': ['LEM', 'Lembaga'],
# 		'LRG': ['LRG', 'Lorong'],
# 		'PDG': ['PDG', 'Padang'],
# 		'PSN': ['PSN', 'Persiaran'],
# 		'SG': ['SG', 'Sungai'],
# 		'SPG': ['SPG', 'Simpang'],
# 		'TG': ['TG', 'Tanjung'],
# 		'TK': ['TK', 'Teluk'],
# 		'TMN': ['TMN', 'Taman'],
# 		'JLN': ['JLN', 'Jalan'],
# 		'Block': ['Block', 'Blok', 'Blk'],
# 		'Blok': ['Blok', 'Block', 'Blk'],
# 		'Blk': ['Blk', 'Block', 'Blok'],
# 		'Appartment': ['Appartment', 'Apt', 'Appt'],
# 		'Apt': ['Apt', 'Appartment', 'Appt'],
# 		'Appt': ['Appt', 'Appartment', 'Apt'],
# 		'Kampung': ['Kampung', 'Kampong', 'KG'],
# 		'Kampong': ['Kampong', 'Kampung', 'KG'],
# 		'KG': ['KG', 'Kampung', 'Kampong'],
# 		'Leboh': ['Leboh', 'Lebuh', 'LBH'],
# 		'Lebuh': ['Lebuh', 'Leboh', 'LBH'],
# 		'LBH': ['LBH', 'Leboh', 'Lebuh'],
# 		'Condominium': ['Condominium', 'Kondo', 'Condo', 'Kondominium'],
# 		'Kondo': ['Kondo', 'Condominium', 'Condo', 'Kondominium'],
# 		'Condo': ['Condo', 'Condominium', 'Kondo', 'Kondominium'],
# 		'Kondominium': ['Kondominium', 'Condominium', 'Condo', 'Kondo'],
# 	}

# 	if len(word_list) == 0:
# 		return ''

# 	word = word_list[0]
# 	remaining = word_list[1:]
# 	possible_strs = []
# 	if word in variation_map:
# 		for variation in variation_map[word]:
# 			possible_str = variation + _helper(remaining, level+1)
		
# 			if level == 0:
# 				possible_strs.append(possible_str)
		
# 			return possible_strs

# 		return possible_str 
# 	else:
# 		return word

# print(get_variations('JLN BKT VISTA'))

# variation_map = {
# 	'Commercial': ['Commercial', 'Komersial'],
# 	'Residency': ['Residency', 'Residensi'],
# 	'Tower': ['Tower', 'Menara'],
# 	'Complex': ['Complex', 'Kompleks'],
# 	'Bagian': ['Bagian', 'BHG'],
# 	'Bukit': ['Bukit', 'BKT'],
# 	'Jabatan': ['Jabatan', 'JAB'],
# 	'Jalan': ['Jalan', 'JLN'],
# 	'Kawasan': ['Kawasan', 'KAW'],
# 	'Kementerian': ['Kementerian', 'KEM'],
# 	'Ladang': ['Ladang', 'LDG'],
# 	'Lembaga': ['Lembaga', 'LEM'],
# 	'Lorong': ['Lorong', 'LRG'],
# 	'Padang': ['Padang', 'PDG'],
# 	'Persiaran': ['Persiaran', 'PSN'],
# 	'Sungai': ['Sungai', 'SG'],
# 	'Simpang': ['Simpang', 'SPG'],
# 	'Tanjung': ['Tanjung', 'TG'],
# 	'Teluk': ['Teluk', 'TK'],
# 	'Taman': ['Taman', 'TMN'],
# 	'Jalan': ['Jalan', 'JLN'],
# 	'Komersial': ['Komersial', 'Commercial'],
# 	'Residensi': ['Residensi', 'Residency'],
# 	'Menara': ['Menara', 'Tower'],
# 	'Kompleks': ['Kompleks', 'Complex'],
# 	'BHG': ['BHG', 'Bagian'],
# 	'BKT': ['BKT', 'Bukit'],
# 	'JAB': ['JAB', 'Jabatan'],
# 	'JLN': ['JLN', 'Jalan'],
# 	'KAW': ['KAW', 'Kawasan'],
# 	'KEM': ['KEM', 'Kementerian'],
# 	'LDG': ['LDG', 'Ladang'],
# 	'LEM': ['LEM', 'Lembaga'],
# 	'LRG': ['LRG', 'Lorong'],
# 	'PDG': ['PDG', 'Padang'],
# 	'PSN': ['PSN', 'Persiaran'],
# 	'SG': ['SG', 'Sungai'],
# 	'SPG': ['SPG', 'Simpang'],
# 	'TG': ['TG', 'Tanjung'],
# 	'TK': ['TK', 'Teluk'],
# 	'TMN': ['TMN', 'Taman'],
# 	'JLN': ['JLN', 'Jalan'],
# 	'Block': ['Block', 'Blok', 'Blk'],
# 	'Blok': ['Blok', 'Block', 'Blk'],
# 	'Blk': ['Blk', 'Block', 'Blok'],
# 	'Appartment': ['Appartment', 'Apt', 'Appt'],
# 	'Apt': ['Apt', 'Appartment', 'Appt'],
# 	'Appt': ['Appt', 'Appartment', 'Apt'],
# 	'Kampung': ['Kampung', 'Kampong', 'KG'],
# 	'Kampong': ['Kampong', 'Kampung', 'KG'],
# 	'KG': ['KG', 'Kampung', 'Kampong'],
# 	'Leboh': ['Leboh', 'Lebuh', 'LBH'],
# 	'Lebuh': ['Lebuh', 'Leboh', 'LBH'],
# 	'LBH': ['LBH', 'Leboh', 'Lebuh'],
# 	'Condominium': ['Condominium', 'Kondo', 'Condo', 'Kondominium'],
# 	'Kondo': ['Kondo', 'Condominium', 'Condo', 'Kondominium'],
# 	'Condo': ['Condo', 'Condominium', 'Kondo', 'Kondominium'],
# 	'Kondominium': ['Kondominium', 'Condominium', 'Condo', 'Kondo'],
# }

# token = 'JLN BKT VISTA'
# token_split = token.split(' ')
# result = token.split(' ')

# for word in token_split:
# 	if word in variation_map:
# 		for variation in variation_map[word]:
# 			result.append(variation)

# print(" ".join(result))

# variation_map = {
#             'COMMERCIAL': ['KOMERSIAL'],
#             'RESIDENCY': ['RESIDENSI'],
#             'TOWER': ['MENARA'],
#             'COMPLEX': ['KOMPLEKS'],
#             'BAGIAN': ['BHG'],
#             'BUKIT': ['BKT'],
#             'JABATAN': ['JAB'],
#             'JALAN': ['JLN'],
#             'KAWASAN': ['KAW'],
#             'KEMENTERIAN': ['KEM'],
#             'LADANG': ['LDG'],
#             'LEMBAGA': ['LEM'],
#             'LORONG': ['LRG'],
#             'PADANG': ['PDG'],
#             'PERSIARAN': ['PSN'],
#             'SUNGAI': ['SG'],
#             'SIMPANG': ['SPG'],
#             'TANJUNG': ['TG'],
#             'TELUK': ['TK'],
#             'TAMAN': ['TMN'],
#             'JALAN': ['JLN'],
#             'KOMERSIAL': ['COMMERCIAL'],
#             'RESIDENSI': ['RESIDENCY'],
#             'MENARA': ['TOWER'],
#             'KOMPLEKS': ['COMPLEX'],
#             'BHG': ['BAGIAN'],
#             'BKT': ['BUKIT'],
#             'JAB': ['JABATAN'],
#             'JLN': ['JALAN'],
#             'KAW': ['KAWASAN'],
#             'KEM': ['KEMENTERIAN'],
#             'LDG': ['LADANG'],
#             'LEM': ['LEMBAGA'],
#             'LRG': ['LORONG'],
#             'PDG': ['PADANG'],
#             'PSN': ['PERSIARAN'],
#             'SG': ['SUNGAI'],
#             'SPG': ['SIMPANG'],
#             'TG': ['TANJUNG'],
#             'TK': ['TELUK'],
#             'TMN': ['TAMAN'],
#             'JLN': ['JALAN'],
#             'BLOCK': ['BLOK', 'BLK'],
#             'BLOK': ['BLOCK', 'BLK'],
#             'BLK': ['BLOCK', 'BLOK'],
#             'APPARTMENT': ['APT', 'APPT'],
#             'APT': ['APPARTMENT', 'APPT'],
#             'APPT': ['APPARTMENT', 'APT'],
#             'KAMPUNG': ['KAMPONG', 'KG'],
#             'KAMPONG': ['KAMPUNG', 'KG'],
#             'KG': ['KAMPUNG', 'KAMPONG'],
#             'LEBOH': ['LEBUH', 'LBH'],
#             'LEBUH': ['LEBOH', 'LBH'],
#             'LBH': ['LEBOH', 'LEBUH'],
#             'CONDOMINIUM': ['KONDO', 'CONDO', 'KONDOMINIUM'],
#             'KONDO': ['CONDOMINIUM', 'CONDO', 'KONDOMINIUM'],
#             'CONDO': ['CONDOMINIUM', 'KONDO', 'KONDOMINIUM'],
#             'KONDOMINIUM': ['CONDOMINIUM', 'CONDO', 'KONDO'],
#         }

# # token = 'JLN BKT VISTA'
# token = 'JLN CONDO VISTA' # bug

# possible_keywords = [token]
# token_list = token.split(' ')
# for i, word in enumerate(token_list):
# 	if word in variation_map:
# 		possible_keywords_before_new_variation = [i for i in possible_keywords]
# 		for variation in variation_map[word]:
# 			# possible_keywords_helper = [i for i in possible_keywords_before_new_variation]
# 			for possibilities in possible_keywords_before_new_variation:
# 				keyword = possibilities.split(' ')
# 				keyword[i] = variation
# 				possible_keywords.append(' '.join(keyword))

# for x in possible_keywords: 
# 	print(x)

def test():
	return 1, 2, 3

x, y = test()
print(x , y)