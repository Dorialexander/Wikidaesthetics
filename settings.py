from wikidatamine import *


#SETTINGS

#Unless you're willing to hack this code (and you're welcome to it), this is the only document where your feedback is needed.

wikid = 15790		 			#The id of the departure of the network (for instance, the painter Cimabue is 15790)
relationship = 1066 			#the type of relationship that will define the "links" of the network. It must be the ID of a Wikidata property. For instance "student of" is 1066
attributes = [106, 27]			#an unlimited list of attributes that matches Wikidata properties (for instance, occupation, place of birth). For instance [106, 27] matches occupation and country of citizenship
accuracy = "yes"				#setting the accuracy to "yes" will retrieve the value of the "sourcing circumstances" qualifier. It is a good practice whenever dealing with hypothetical data, but can slow down the crawling process.
searchmode = "web"		 		#one of the three pre-defined types of search mode : "descending", "ascending" or "web" (both ascending and descending)
maxima = "none"					#maximum number of results. If you want to retrieve all results, set it to "none" (any strings will do, in fact...).
lang = "en"						#the language of the retrieved wikidata labels ("en" for English, "fr" for French and so on...). If there is no label in this language, the item will be marked by an id between brackets
dataviz = "network"	 			#a predefined dataviz. Currently, wikidaesthetics only includes a network maker (which ends with the production of a gexf file)
filename = "CimabueNetwork" 	#name of the gexf file at the end. Will not have any effect if dataviz is set to "none"


#FUNCTION

wikidaesthetics(wikid, relationship, attributes, accuracy, searchmode, maxima, lang, dataviz, filename)
