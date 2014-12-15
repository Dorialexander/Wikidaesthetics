Wikidaesthetics
===============

Wikidaesthestics is a python 2.7 library that allows to retrieve and visualize network data from Wikidata. For instance, in the default program, you can get all the students of the italian painter Cimabue.

Currently, the program is very much alpha, with limited functions (e. g. it only creates a gexf file, and do not recognize specific Wikidata datatypes, like time or coordinates), and somes glitches (once in a while, Gephi would refuse to recognize the attributes, while they perfectly appears in the gexf file). It only requires the standard modules of Python 2.7.

The loading time can be long. The access to Wikidata data remains complicated. There is currently two different APIs: the Wikidata official API identifies all the properties and values stored in an item page; the Wikidata Query API from Magnus Manske works in reverse, and retrieves all the item corresponding to a property and a value. While I've tried to avoid any unnecessary connections, the extraction process may imply numerous calls to each API.

<h3>The inputs</h3>

Your inputs are only required in the "settings.py" file.

<b>wikid</b> = an id from Wikidata (that is, a number that matches an item : 15790 for Cimabue), that is the starting point of your network (for instance, here, the painter Cimabue). If you use the "web" searchmode (see below), the id can be any points in your network.

<b>relationship</b> = the "connection" property between each item of your network. It must be a property of Wikidata and, preferably, a property with a "network" quality. The default category in the example is 1066 for "student of".

<b>attributes</b> = a list of attributes appended to each items. They must also be properties from Wikidata and put into brackets (even if there's only one attribute). [106, 27] refers therefore to occupation (P106) and the country of citizenship (P27). The list can be as long as needed (even though, that will put an additional strain to the loading time). I you don't want to use any attribute, you can put a "none"

<b>accuracy</b> = either yes or no. If positive, it will retrieves the value of the "sourcing circumstances" qualifier of the relationship property, and append it to the edge of the network. This input is useful whenever you deal with uncertain data (e. g. the student-master relationship between two ancient philosophers may well be hypothetical).

<b>serchmode</b> = either "descending", "ascending" or "web". With "descending", the crawling function will only go down in the network (that is, retrieve the students of an item, then the students of these students, and so on…). "ascending" works in reverse (the persons the items has studied with, and so on…). "web" combines the two searchmodes and gets for each items, the "ascendants" and the "descendants". While "web" is probably the better function to map a network, the two other search modes are appropriate whenever dealing with genealogical relationships (and, additionally, they save up some loading time).

<b>maxima</b> = the maximum number of results. It is useful, whenever you run some initial tests and don't know the size of the network, of if the network is huge and you prefer to only select a sample. If you set the value to "none", the maxima does not apply.

<b>lang</b> = the language of the results ("en" for English, "fr" for French and so on…). Wikidata being a multilingual project, the data and the properties names can be easily translated. If they do not exist in this language, the ID of the item or the property will be retrieved (for instance, "(Q15790)" for Cimabue.

<b>dataviz</b> = the dataviz file, resulting from the extraction process. Currently, there's only one option, "network", that create a gexf file. If you set it to "none", you get a python object, that can be used to other purposes.

<b>filename</b> = the name of the dataviz file. It will not have any effect if dataviz is set to "none".

<h3>What's next?</h3>

The gexf file may be used as such with a javascript dataviz library. Yet, it is preferable to enhance it using Gephi. You will get the ability to define a modelization (force directed, ) and set the colours and the size of the items and the edge according to the attributes or the intensity of the relationship links. Gephi includes a sigma.js plugin that produces some very nice dataviz.

Using this working process, I have produced a network of ancient philosophers. A set of colours distinguished each philosopher according to their philosophical affiliation (red for Platonists, green for Stoicians…), and each edge according to their accuracy (red for hypothetical, green for near-certainty…).
