Design, Browsing and Automation of Digital Knowledge and Traces
===================

Through my research, I have been searching a way to conceptualize digital knowledge in an innovative way.  That led me to work on a Rhythm Network, that is a fundamental structure, connecting objects using temporal metrics. Here, one can find all ressources related to my PhD: a Rhythm Network application (build and browse), developped in Python/rpy2 and all materials from the 5 experiments supporting the solution.  

----------

Abstract 

----------


Rhythm Network
-------------

#### <i class="icon-folder-open"></i>RhythmNetwork 
This folder contains the source code of the Rhythm Network Application. One can build his own Rhythm Network structure using the method creerTimeGraph in TimeGraph.py file. Input is a CSV file containing triples (timestamp, itemid, userid) ordered by timestamp.

WS.py contains recommender methods. Once the structure is created, it is possible to ask for recommendations based on rhythm. Giving a triple as an input, the algorithm walks on the Rhythm Network, and output the most similar item depending on time. 

> **Note:**

> - The data structure is fully configurable using Singularity Threshold and Cycle Threshold
> - rpy2 must be installed (see documentation [here](https://rpy2.bitbucket.io/))
> - Graph data are stored on your machine, please make sure you change all local paths and set all related permissions.

#### <i class="icon-folder-open"></i> Experiments
This folder contains the 5 experiments materials. Each experiment has its specific space/folder, in which there are at most three folders: <i class="icon-folder"></i> **process**, <i class="icon-folder"></i> **dataset** and <i class="icon-folder"></i> **results**.

----------
#### <i class="icon-star"></i> The Rhythm of Knowledge

This work deals with user behaviors in an E-learning system. Processing Moodle log files, we analyze how learners make connections between pieces of Knowledge. We measure these connections with an interval of time. As a result the Rhythm Network helps to understand the rhythm of Knowledge both on a meta-level (e-learning course) and on a micro-level (learner). Path discovering techniques are not new, but here we make it in a time-based fashion: an e-learning resource has not the same impact at the start or at the end of a course. Our method might serve as a Learning Analytics feature and could also have other benefits such as a recommender engine. Here, using three real-life datasets, we present general techniques and we also unveil two new mechanisms to track cycles of items and singular patterns.

>Pattern Discovery in E-learning Courses: a Time-based Approach Guillaume Blot, Francis Rousseaux and Pierre Saurel - CODIT2014, Metz, nov 2014.
><i class="icon-award"></i> [Award of the Best paper IT CoDIT14](http://codit2014.event.univ-lorraine.fr/)

> <i class="icon-folder-open"></i> Experiments/RhytmOfKnowledge

> - Original dataset is provided by a french educational institution called [GRETA Champagne-Ardennes](http://moodgreta.eu/Site_GIP_FC), extracted from Moodle courses. It is composed with 3 files (610.csv, 614.csv and 809.csv). All data have been anonymized. More details about these data are available in the related article.
> - Results are various GEXF graph files structuring learners trajectories and learning rhythms. 

----------
#### <i class="icon-star"></i> How recommender Engines Manipulate Human Cognition? Toward an Iterative Behavior Shift

On the Internet, are we our own master? Is the Web an enemy of the free will? Nowadays, everyone possesses a tool giving an immediate and infinite access to a growing set of items. But, browsing these unlimited resources happens to be too complicated for a human brain. To help us in our choices, we rely on features such as recommender engines, which try to understand our profile and suggest us directions on this basis. These are machine learning tools relying on user activities. But human brain is subject to natural biases, such as confirmation bias and information cascades. We associate to our natural cognition, an artificial cognition, which is composed with a form of our self biased cognition. These two systems coexist and apply mutual influences. Here we are, shipping in an infinite loop toward an iterative behavior shift, with some foreseen dangers: conformism, plural ignorance and extremism.

> <i class="icon-folder-open"></i> Experiments/RecommenderConfirmation

> - Original dataset is available here: https://www.kaggle.com/c/outbrain-click-prediction
> - Each step produces an output file. If you wish to go through the whole process, please follow the exact order listed bellow. The full process is explained in my PhD manuscript. Don’t forget to set your input/output folder at the top of each script.
> - <i class="icon-file"> datasetSample.cs </i>: get a sample of the dataset. Produces nodes.csv, edges.csv and categories.csv
> - <i class="icon-file"> recommandationEngines.cs </i>: get recommandations. Produces similarities/Sim_XX.csv, where XX is the recommender surname (AA = Adamic/Adar, CN = Common Neighbors, COS = Cosine-Based and COR = Correlation-Based)
> - <i class="icon-file"> confirmationSimilarities.cs </i>: get recommandations by categories. Produces similarities/CatSim_XX.csv 
> - <i class="icon-file"> confirmationResults.cs </i>: get confirmation results. Produces confirmation/finalStats.csv
> - <i class="icon-file"> popularityResults.cs </i>: get popularity results. Produces distribution/XX.csv

----------
#### <i class="icon-star"></i> Recommendation Engines Under the Influence of Popularity

One often thinks that the use of Information Technologies brings an infinity of choices. However, Popularity still influences people in our free, pervasive and connected world. It is a reality: popular items keep power and weak items tend to be forgotten. Several studies demonstrated that this natural phenomenon is accentuated today with recommender engines. In this article we present a comparative study of 8 recommendation techniques. We also present a personal recommendation approach, based on items timeline. We unveil a Popularity Influence index, which evaluates the way recommender engines are influenced by the phenomenon. This experiment is led by a pool of interdisciplinary researchers, either or both epistemologists and computer scientists. It includes diverse examples and references from e-business, cultural studies or participatory democracy along with others. We believe that Popularity belongs to a wide set of fields. Therefore, we chose to run this experiment in an E-learning context, where we observe pieces of knowledge popularity. 

> Recommender Engines Under the Influence of Popularity. Guillaume Blot, Pierre Saurel, Francis Rousseaux - MCETECH 2015: 138-152, Montreal, may 2015
> 
> <i class="icon-folder-open"></i> Experiments/RecommenderPopularity

> - This experiment relies on the e-learning dataset, already presented here 
> - <i class="icon-file"> full_distrib.csv</i>: all distributions ordered following the original distribution
> - <i class="icon-file"> results_xx.csv</i>: all methods ordered following their specific distribution. xx is the method (aa = Adar/Adamic, cn = common neighbors, pa = preferential attachment, ra = resource allocation and tg = Rhythm Network, originaly called Time Graph). 

----------
#### <i class="icon-star"></i> An Experimentation of VANETs for Traffic Management

Nowadays, wireless communication technologies have high influence on our daily lives. The vehicular ad hoc networks (VANETs) is now evolving quickly and attract attention from road operators, car manufacturers and governments. We unveil a fine traffic flow optimization method with VANETs. On the macroscopic level, our model identifies road segment profiles. On the microscopic level, vehicles send and receive alerts using low-level-of-details data. This paper gives workflows for both vehicle and infrastructure sides.


> An Experimentation of VANETs for Traffic Management. Guillaume Blot, Hacène Fouchal, Francis Rousseaux and Pierre Saurel. Communications (ICC), 2016 IEEE International Conference on Communications, Kuala Lumpur (2016).

> <i class="icon-folder-open"></i> Experiments/TrafficFlowVanet

> - Dataset is provided by the [Mobile Millenium Team (UC Berkley)](http://traffic.berkeley.edu/project/downloads/mobilecenturydata)
> - Source code presents vehicle and infrastructure sides. Infrastructure side produces a RData file in folder results, containing current thresholds.  Vehicle side uses it as an input. Run first infrastructure part.
> - Run source code in a R environment
> - Please change dataset file path in the scripts
> - <i class="icon-file">infrastructure_side.R</i>: produces RData file, and print statistics in results folder
> - <i class="icon-file">vehicle_side.R</i>:  print alerts chart and statistics as an output

----------
#### <i class="icon-star"></i> Visualizing interval patterns in pitch constellation

Halfway between music analysis and graph visualization, we propose tonal pitch representations from the chromatic scale. On the first part of the experiment, a 12-node graph is connected as a Rhythm Network and visualized with a Circular Layout, commonly known as Pitch constellation. This particular graph topology focuses on node structure and gives strength to weak edges. At this occasion, we unveil the Singularity Threshold, giving an opportunity to isolate structure from singular parts of melodies. Where usual Pitch constellations focus on chords, we focus on successive pitch intervals. On the second part, we propose a rhythm representation using a Force-Directed layout. In addition to structural information, our second technique shows proximal and peripheral elements. This experiment features 6 melodies that we propose to visualize using Gephi.



> Visualizing interval patterns in pitch constellation. Guillaume Blot, Pierre Saurel, Francis Rousseaux - CMMR 2016 - Bridging People and Sounds, Sao Paulo (2016).

> <i class="icon-folder-open"></i> Experiments/Visualisation

> - All melodies have been dowloaded from [MidiWorld.com](http://www.midiworld.com/files/)
> - Dataset folder contains melodies at each step of the experiment. Starting from a MIDI file, it is translated in CSV, then the melody is a GEXF file built following Rhythm Network techniques. GEXF file are visualizable using Gephi.
> - <i class="icon-folder">source/organize</i>: php scripts (refering to Figure 1 in the article).
> - <i class="icon-folder">data/n</i>: n is the id of the song. Here are data at all stages of the experiment.
	
