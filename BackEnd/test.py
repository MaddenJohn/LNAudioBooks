import json

s = {"test" : "data"}
s2 = '{"test" : "data"}'



def test(s): 
	if (type(s) == dict):
		j = s
	elif (type (s) == str):
		j = json.loads(s)
	print (j["test"])

test(s)
test(s2)