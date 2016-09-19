import json
import codecs
import string

f = open("stations_copy.json")
d = f.read()
newjson = json.loads(d)
for itor in newjson[u'stations']:
	itor[u'lat'] = unicode(str(string.atof(itor[u'lat'])+0.003591), "utf-8")
	itor[u'lng'] = unicode(str(string.atof(itor[u'lng'])+0.010108), "utf-8")



