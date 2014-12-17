from urllib2 import Request, urlopen, URLError
import json
import pickle
import codecs
from gexfmaker import *


class Profile:
	"""A class to store profile data with statement"""

	def __init__(self, id, name, relation, statement):
		self.id = id
		self.name = name
		self.relation = relation
		self.statement = statement
		
class ProfileStateless:
	"""A class to store profile data without statement"""
	
	def __init__(self, id, name, relation):
		self.id = id
		self.name = name
		self.relation = relation


def wikidaesthetics (id, relationship, attributes, accuracy, searchmode, maxima, lang, dataviz, filename):
	"""main function"""
	
	unknown = str(getslabelbyid("400506", lang)).lower()
	tupleidprop = correctnames(id, relationship)
	id = tupleidprop[0]
	relationship = tupleidprop[1]
	if not attributes: #checking if the user wants to get additional statements
		attributesname = "none"
	else: 
		attributesname = getattributesname(attributes, lang) #getting properties name at the very beginning to save loading time
	dataresult = crawling(id, relationship, attributesname, accuracy, searchmode, lang, unknown, maxima)
	if dataviz == "network": #checking the dataviz mode
		export(dataresult, accuracy, filename)
	elif dataviz == "none":
		return dataresult
	else:
		return dataresult
		print "No known value. Defaulting to \"none\""

def correctnames(id, relationship):
	if isinstance(id, basestring):
		if id[0] == "Q":
			id = id[1:len(id)]
			id = int(id)
		else:
			id = int(id)
	if isinstance(relationship, basestring):
		if relationship[0] == "P":
			relationship = relationship[1:len(relationship)]
			relationship = int(relationship)
		else:
			relationship = int(relationship)
	return (id, relationship)


#IDENTIFICATION OF ID AND PROPERTIES

def getattributesname(attributes, lang):
	"""get properties names"""

	attributescoll = []
	for att in attributes:
		request = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=P" + str(att) + "&format=json&languages=" + str(lang) + "&props=labels"
		try:
			response = urlopen(request)
			kittens = response.read()
			kittens = json.loads(kittens)
			fullid = "P" + str(att)
			dictoflabels = kittens["entities"][fullid]
			if 'labels' in dictoflabels:	#Check if the item exists in this tongue
				kittens = dictoflabels["labels"][str(lang)]["value"]
				kittens = (kittens, att)
				attributescoll.append(kittens)
			else:
				return "(P" + str(id) + ")"
		except URLError, e:
			print 'No API. Got an error code:', e
	return attributescoll


def getslabelbyid(id, lang):
	"""get id name"""
	
	request = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q" + str(id) + "&format=json&languages=" + str(lang) + "&props=labels"
	try:
		response = urlopen(request)
		kittens = response.read()
		kittens = json.loads(kittens)
		fullid = "Q" + str(id)
		dictoflabels = kittens["entities"][fullid]
		if 'labels' in dictoflabels:	#Check if the item exists in this tongue
			return dictoflabels["labels"][str(lang)]["value"]
		else:
			return "(Q" + str(id) + ")"
	except URLError, e:
		print 'No API. Got an error code:', e


#SOME FUNCTIONS TO GET RELATIONS AND THE DEGREE OF CERTAINTY (1 = hypothetically, 2 = presumably, 3 = near-certainty)

def getrelation(property, id, accuracy):
	request = "http://wdq.wmflabs.org/api?q=claim[" + str(property) + ":" + str(id) + "]"
	try:
		response = urlopen(request)
		kittens = response.read()
		kittens = json.loads(kittens)
		if accuracy == "yes":
			return kittens["items"]
		else:
			allresults = []
			for item in kittens["items"]:
				item = ("3", item, "desc")
				allresults.append(item)
			return allresults
	except URLError, e:
		print 'No kittez. Got an error code:', e

def getrelationhypo(property, id):
	request = "http://wdq.wmflabs.org/api?q=claim[" + str(property) + ":" + str(id) + "]{claim[1480:18603603]}"
	try:
		response = urlopen(request)
		kittens = response.read()
		kittens = json.loads(kittens)
		kittens = kittens["items"]
		hyporesult = []
		for item in kittens:
			item = ("1", item, "desc")
			hyporesult.append(item)
		return hyporesult
	except URLError, e:
		print 'No kittez. Got an error code:', e
		
def getrelationprob(property, id):
	request = "http://wdq.wmflabs.org/api?q=claim[" + str(property) + ":" + str(id) + "]{claim[1480:18122778]}"
	try:
		response = urlopen(request)
		kittens = response.read()
		kittens = json.loads(kittens)
		kittens = kittens["items"]
		probresult = []
		for item in kittens:
			item = ("2", item, "desc")
			probresult.append(item)
		return probresult
	except URLError, e:
		print 'No kittez. Got an error code:', e

def mergerelation(relation, relationprob, relationhypo): #merge all the certain, prob and hypo relations while keeping the accuracy information
	finallist = []
	for elm in relation:
		for prob in relationprob:
			if elm == prob[1]:
				relation.remove(elm)
		for hypo in relationhypo:
			if elm == hypo[1]:
				relation.remove(elm)
	for elm in relation:
		elm = ("3", elm, "desc")
		finallist.append(elm)
	finallist.extend(relationprob)
	finallist.extend(relationhypo)
	return finallist

def relationascend(property, id, accuracy):
	relationwhole = []
	request = "https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q" + str(id) + "&property=P" + str(property) + "&format=json"
	try:
		response = urlopen(request)
		kittens = response.read()
		kittens = json.loads(kittens)
		fullproperty = "P" + str(property)
		if fullproperty in kittens["claims"]:
			relationlist = kittens["claims"][fullproperty]
			for elm in relationlist:
				item = str(elm["mainsnak"]["datavalue"]["value"]["numeric-id"])
				if ("qualifiers" in elm.keys() and accuracy == "yes"):
					try:
						if elm["qualifiers"]["P1480"][0]["datavalue"]["value"]["numeric-id"] == 18122778:
							relationwhole.append(("2", item, "asc"))
						elif elm["qualifiers"]["P1480"][0]["datavalue"]["value"]["numeric-id"] == 18603603:
							relationwhole.append(("1", item, "asc"))
						else:
							relationwhole.append(("3", item, "asc"))
					except:
						relationwhole.append(("3", item, "asc"))
				else:
					relationwhole.append(("3", item, "asc"))
		return relationwhole
	except URLError, e:
		print 'No API. Got an error code:', e




def getsstatement(id, attributes, lang, unknown):
	"""get a list of statements from the list of attributes"""
	
	finalproplist = []
	for att in attributes:
		properties = att[1]
		request = "https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=Q" + str(id) + "&property=P" + str(properties) + "&format=json"
		try:
			response = urlopen(request)
			kittens = response.read()
			kittens = json.loads(kittens)
			fullid = "Q" + str(id)
			fullprop = "P" + str(properties)
			if not kittens["claims"]:
				resultid = (att[0], "0", unknown)
			else:
				resultid = kittens["claims"][fullprop][0]["mainsnak"]["datavalue"]["value"]["numeric-id"]
				resultidname = getslabelbyid(resultid, lang)
				resultid = (att[0], resultid, resultidname)
			finalproplist.append(resultid)
		except URLError, e:
			print 'No API. Got an error code:', e
	return finalproplist


def check(id, profilerecord):
	"""check if the id is not already on the list"""
	check = True
	for elm in profilerecord:
		if id == elm.id:
			check = False
	return check


def cleanup(fulllist, newlist):
	"""Remove duplicates on the list (in case the web is switched)"""
	
#	indexcounter = -1
	for elm in fulllist:
#		indexcounter +=1
		for item in newlist:
			if elm == item:
				newlist.remove(item)
	return newlist


def getprofile(id, relationship, attributes, accuracy, searchmode, lang, unknown):
	"""Get the profile of a Wikidata id (which includes id, name and relations)"""
	
	name = getslabelbyid(id, lang)
	if accuracy == "yes":
		if searchmode == "ascending":
			relation = relationascend(relationship, id, accuracy)
		if searchmode == "descending":
			relation = getrelation(relationship, id, accuracy)
			relationprob = getrelationprob(relationship, id)
			relationhypo = getrelationhypo(relationship, id)
			relation = mergerelation(relation, relationprob, relationhypo)
		if searchmode == "web":
			relationdescall = getrelation(relationship, id, accuracy)
			relationprob = getrelationprob(relationship, id)
			relationhypo = getrelationhypo(relationship, id)
			relationdesc = mergerelation(relationdescall, relationprob, relationhypo)
			relationasc = relationascend(relationship, id, accuracy)
			relation = relationasc + relationdesc
	else:
		if searchmode == "ascending":
			relation = relationascend(relationship, id, accuracy)
		if searchmode == "descending":
			relation = getrelation(relationship, id, accuracy)
		if searchmode == "web":
			relationdesc = getrelation(relationship, id, accuracy)
			relationasc = relationascend(relationship, id, accuracy)
			relation = relationasc + relationdesc
	if attributes == "none":
		profile = ProfileStateless(id, name, relation)
	else:
		statement = getsstatement(id, attributes, lang, unknown)
		profile = Profile(id, name, relation, statement)
	return profile

def crawling(id, relationship, attributes, accuracy, searchmode, lang, unknown, maxima):
	"""get all the profile of the connected id in a descending order"""

	profilerecord = []
	lastlist = [id]
	x = 0
	fulllist = [str(id)]
	if isinstance (maxima, int):
		while (len(lastlist)>0) and (len(profilerecord) < (maxima+1)) :
			newlist = []
			for id in lastlist:
				if (check(id, profilerecord)) == True and (len(profilerecord) < (maxima)) :
					newprofile = getprofile(id, relationship, attributes, accuracy, searchmode, lang, unknown)
					profilerecord.append(newprofile)
					for name in newprofile.relation:
						newlist.append(str(name[1]))
			if searchmode == "web": 		#enhanced cleaning for the "web" searchmode
				newlist = list(set(newlist))
				duplicate = [i for i in newlist if i in fulllist]
				for elm in duplicate:
					newlist.remove(elm)
				fulllist += newlist
				lastlist = newlist
				x+=1
			else:
				lastlist = newlist
				x+=1
	else:
		while len(lastlist)>0 :
			newlist = []
			for id in lastlist:
				if check(id, profilerecord) == True:
					newprofile = getprofile(id, relationship, attributes, accuracy, searchmode, lang, unknown)
					profilerecord.append(newprofile)
					for name in newprofile.relation:
						newlist.append(str(name[1]))
			if searchmode == "web": 		#enhanced cleaning for the "web" searchmode
				newlist = list(set(newlist))
				duplicate = [i for i in newlist if i in fulllist]
				for elm in duplicate:
					newlist.remove(elm)
				fulllist += newlist
				lastlist = newlist
				x+=1
			else:
				lastlist = newlist
				x+=1
	return profilerecord
