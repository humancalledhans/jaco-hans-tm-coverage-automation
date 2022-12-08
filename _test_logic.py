	# JALAN	CANTIK 7	TAMAN PELANGI INDAH	2	RUMAH PANGSA ZON 1F3 BLOK U	ULU TIRAM	JOHOR	81800
from thefuzz import fuzz
# from thefuzz import process
from Levenshtein import distance

# actual data for 1369
a_db1 = "RUMAH PANGSA TAMAN PELANGI INDAH"
a_web1 = "RUMAH PANGSA ZON 1F3 BLOK U"

# mock data with section repositioned
a_db2 = "TAMAN PELANGI INDAH RUMAH PANGSA"
a_web2 = "RUMAH PANGSA TAMAN PELANGI INDAH"

# actual concat data for 1369 (sec & bld)
a_db3 = "RUMAH PANGSA TAMAN PELANGI INDAH"
a_web3 = "RUMAH PANGSA ZON 1F3 BLOK U TAMAN PELANGI INDAH"

# spelling variation
x1 = "RUMAH PANGSA"
x2 = "ROMAH PANGSA"

# placement of symbols
y1 = "C-11-01"
y2 = "C/11 01"

# spelling mistake
z1 = "RUMAH PANGSA"
z2 = "RUMA PANGSER"

a_db = a_db3
a_web = a_web3

print("levenshtein:", distance(a_db, a_web))
print("ratio:", fuzz.ratio(a_db, a_web))
print("partial_ratio:", fuzz.partial_ratio(a_db, a_web))
print("token_sort_ratio:", fuzz.token_sort_ratio(a_db, a_web))
print("token_set_ratio:", fuzz.token_set_ratio(a_db, a_web))

