import getpass
import time
import codecs

#SETTING UP THE INTRODUCTION OF THE FILE AND REPORTING THE STATEMENTS TO THE ATTRIBUTE LIST
def intro(objectlist, name):
	nid = 0
	header = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\">\n"
	date = u"    <meta lastmodifieddate=\"" + unicode(time.strftime("%Y/%m/%d")) + u"\">\n"
	author = u"        <creator>" + unicode(getpass.getuser()) + u"</creator>\n"
	desc = u"        <description>" + unicode(name) + u"</description>\n"
	compl = u"    </meta>\n    <graph mode=\"static\" defaultedgetype=\"directed\">\n"
	attributelist = u""
	if str(objectlist[0].__class__.__name__) == "Profile":
		compl += u"    	<attributes class=\"node\">\n"
		baseitem = objectlist[0]
		for statement in baseitem.statement:
			nid +=1
			newattribute = u"           <attribute id=\"" + unicode(nid) + u"\" title=\"" + unicode(statement[0]) + u"\" type=\"string\"/>\n"
			attributelist += newattribute
		attributelist += u"        </attributes>\n"
	attributelist += u"    	<attributes class=\"edge\">\n           <attribute id=\"0\" title=\"source\" type=\"integer\"/>\n    	</attributes>\n        <nodes>\n"
	intro = header + date + author + desc + compl + attributelist
	return intro

def intonode(profile):
	nid = 0
	id = profile.id
	name = profile.name
	if str(profile.__class__.__name__) == "Profile": #check if the object contains a list of statements or not
		node = u"             <node id=\"" + unicode(id) + u"\" label=\"" + unicode(name) + u"\">\n"
		for statement in profile.statement:
			nid +=1
			attribute = u"                <attvalue for=\"" + unicode(nid) + u"\" value=\"" + unicode(statement[2]) + u"\"/>\n"
			node += attribute
		node += u"             </node>\n"
	else:
		node = u"             <node id=\"" + unicode(id) + u"\" label=\"" + unicode(name) + u"\"/>\n"
	return node

def intoedge(id, relation, x, objectlist, accuracy):
	propid = x
	firstid = id
	newid = relation[1]
	if checkidrelation(newid, objectlist) is True:
		if accuracy == "yes":
			if relation[2]=="desc":
				firstedge = u"             <edge id=\"" + unicode(propid) + u"\" source=\"" + unicode(firstid) + u"\" target=\"" + unicode(newid) + u"\">\n"
				attribute = u"                <attvalue for=\"0\" value=\"" + unicode(relation[0]) + u"\"/>\n             </edge>\n"
				edge = firstedge + attribute
				return edge
			if relation[2]=="asc":
				firstedge = u"             <edge id=\"" + unicode(propid) + u"\" source=\"" + unicode(newid) + u"\" target=\"" + unicode(firstid) + u"\">\n"
				attribute = u"                <attvalue for=\"0\" value=\"" + unicode(relation[0]) + u"\"/>\n             </edge>\n"
				edge = firstedge + attribute
				return edge
		else:
			if relation[2]=="desc":
				edge = u"             <edge id=\"" + unicode(propid) + u"\" source=\"" + unicode(firstid) + u"\" target=\"" + unicode(newid) + u"\"/>\n"
				return edge
			if relation[2]=="asc":
				edge = u"             <edge id=\"" + unicode(propid) + u"\" source=\"" + unicode(newid) + u"\" target=\"" + unicode(firstid) + u"\"/>\n"
				return edge

def checkidrelation(newid, objectlist):
	check = False
	for item in objectlist:
		if str(item.id) == str(newid):
			check = True
	return check

def export(objectlist, accuracy, filename):
	idattribute = 0
	opening = intro(objectlist, filename)
	storerelation = []
	entracte = u"         </nodes>\n         <edges>\n"
	end = u"        </edges>\n    </graph>\n</gexf>"
	nodes = u""
	edges = u""
	for iom in objectlist :
		opening += intonode(iom)
	opening += entracte
	for iom in objectlist:
		for rel in iom.relation:
			if [str(iom.id), str(rel[1])] not in storerelation:
				if [str(rel[1]), str(iom.id)] not in storerelation:
					idattribute+=1
					newedge = intoedge(iom.id, rel, idattribute, objectlist, accuracy)
					if isinstance(newedge, basestring):
						opening += newedge
						storerelation.append([str(iom.id), str(rel[1])])
	opening+=end
	finaltext = filename + ".gexf"
	closing = codecs.open(finaltext, 'w', "utf-8")
	closing.write(opening)
	closing.close()
