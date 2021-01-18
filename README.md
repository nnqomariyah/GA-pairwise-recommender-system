# GA-pairwise-recommender-system

Created by: Nicholas Michael Halim, Nunung Nurul Qomariyah, Dimitar Kazakov (under journal publication review)


**USER MANUAL**



1. This program can only be run with the following requirements:
  * CPU architecture must be x86\_64 (or AMD64)
  * Python 3.7 is installed
  * Ortoolsversion 7.7.7810 module is installed in the Python environment.
 This module can be installed with pipin Windows, macOS, and Linux. More details on how to install can be found in: _https://developers.google.com/optimization/install/python_

2. Run the program by calling $ python main.py

3. This software can take arguments:

--genePool = this parameter is used to specify the attractions list in specific country/city that we want to visit. The format should follow the example in: jsonAttraction.txt

--dList = this parameter is used to specify the distance matrix between one place to another place. The format should follow the example in:distanceMatrix.csv

--durList =this parameter is used to specify the duration matrix from one place to another place. The format should follow the example in: durationMatrix.csv

--nPeople = this parameter is used to specify the number of people in the group who wants to travel. The default value is 2

--budget = this parameter is used to specify the budget that we want to spend for travel for the given day. The default value is 3000000

--duration = this parameter is used to specify the number of days of overall trips. For example, if we want to visit Jakarta only for 3 days, we can specify 3. The default value is 3

--epochs = this parameter is used to specify how many iteration we want the algorithm to run. The default value is 400

--tags = this parameter is used to specify the favorite type of places we want to visit. We may specify more than one value, separated with a coma (&quot;,&quot;). Possible options are kids-friendly, art-and-culture, museum, outdoors, history, amusement-park, history. The default value is: museum,beach,kids-friendly

4. To use the arguments, we can simply type the value-key pairs after calling the main.py, as the following example:

  `$ python main.py --genePool jsonAttraction.txt --dList distanceMatrix.csv --durList durationMatrix.csv --nPeople 2 --budget 3000000 --duration 3 --epochs 400 –tags museum,beach,kids-friendly`

5. Upon a successful execution, the program will show message:

  `Process finished in 0.284162 seconds`

  `Result can be found in: newresults.txt`

6. The result of the algorithm can be found in newresults.txt

`{ "fitness"	: 0.26807415526855083, `

`  "spots"	: ["Pancasila Sakti Monument", `

`"Indonesia Museum",` 

`"Pelabuhan Perikanan Samudera Nizam Zachman",`

`"Taman Dadap Merah",` 

`	"Taman Prasasti Museum",` 

`	"Marunda Beach",` 

`	"Waterpark Transera",` 

`	"Sea World Ancol", `

`	"Benteng Heritage Museum", `

`	"SnowBay Waterpark TMII", `

`	"Nurul Iman Mosque Blok M Square", `

`	"Palm Bay Water Park", `

`	"Jakarta Planetarium"], `

`"HTM"	: 1074000, `

`"travelExpenses": 1555580.0, `

`"totalExpenses": 2629580.0, `

`"totalDuration": 30.02611111111111, `

`"travelDuration": 7.8261111111111115,` 

`"totalDist": 173266, `

`"route": " Pancasila Sakti Monument -> Indonesia Museum -> SnowBay Waterpark TMII -> Taman Dadap Merah -> Nurul Iman Mosque Blok M Square -> Jakarta Planetarium -> Taman Prasasti Museum -> Benteng Heritage Museum -> Palm Bay Water Park -> Pelabuhan Perikanan Samudera Nizam Zachman -> Sea World Ancol -> Marunda Beach -> Waterpark Transera ->",` 

`"route-by-index": [0, 1, 9, 3, 10, 12, 4, 8, 11, 2, 7, 5, 6],`

`"per-day-route": [["Pancasila Sakti Monument", "Indonesia Museum", "SnowBay Waterpark TMII", "Taman Dadap Merah", "Nurul Iman Mosque Blok M Square", "Jakarta Planetarium", "Taman Prasasti Museum"], 
["Benteng Heritage Museum", "Palm Bay Water Park", "Pelabuhan Perikanan Samudera Nizam Zachman", "Sea World Ancol"], ["Marunda Beach", "Waterpark Transera"]
]}`

7. Based the result above, we can see clearly that the most effective route for visit Jakarta, given the budget, duration and number of people in the group is as follow:

  * This algorithm is based on Genetic Algorithm, so fitness here means the goodness of the result. We can see the score in the argument &quot;fitness&quot; : 0.26807415526855083

  * If we want to see what are the places the good to be visited, we can examine them in the argument &quot;spots&quot;. In the above example, we can see clearly that the list of places we can visit is as the following:

    - Pancasila Sakti Monument,
    - Indonesia Museum,
    - Pelabuhan Perikanan Samudera Nizam Zachman,
    - Taman Dadap Merah,
    - Taman Prasasti Museum,
    - Marunda Beach,
    - Waterpark Transera,
    - Sea World Ancol,
    - Benteng Heritage Museum,
    - SnowBay Waterpark TMII,
    - Nurul Iman Mosque Blok M Square,
    - Palm Bay Water Park,
    - Jakarta Planetarium


  * The total entrance fees for the whole trip can be found in argument &quot;HTM&quot;. In the above example, we can see that the entrance fees we need to pay isIDR 1,074,000

  * The travel expenses for the whole trip can be seen in argument &quot;travelExpenses&quot;. In this algorithm we use estimate taxi fare per km. In the above example we can see the travel expense is IDR 1,555,580

  * Total expense, which is the sum of travel expenses and entrance fee altogether, can be found in argument &quot;totalExpenses&quot;. In the above example is IDR 2,629,580. This number is quite close to the budget that we want to spend for the trip which is 3 million rupiahs (see parameter budget in point 7).

  * Total duration of the whole trip can be found in argument &quot;totalDuration&quot;. In the above example it is 30.02611111111111hours, which can be round down to 30 hours (assuming we only want to travel 10 hours per day, so in total this recommendation is good for 3 days trip)

  * Travel duration, which only calculating the times that we need to spend for travel from one place to another place can be found in argument `travelDuration`. In the above example, it is estimated as 7.8261111111111115 hours for the whole trip.

  * Total distance from first place to last place can be found in argument &quot;totalDist&quot;. In the result above, it is 173,266 km.

  * Overall route from all places can be found in argument &quot;route&quot;. In the above example the best recommendation to sort the places is as follows:

`Pancasila Sakti Monument -> Indonesia Museum -> SnowBay Waterpark TMII -> Taman Dadap Merah -> Nurul Iman Mosque Blok M Square -> Jakarta Planetarium -> Taman Prasasti Museum -> Benteng Heritage Museum -> Palm Bay Water Park -> Pelabuhan Perikanan Samudera Nizam Zachman -> Sea World Ancol -> Marunda Beach -> Waterpark Transera `


  * The best route we can follow the result in argument per-day-route:

Day 1: &quot;Pancasila Sakti Monument&quot;, &quot;Indonesia Museum&quot;, &quot;SnowBay Waterpark TMII&quot;, &quot;Taman Dadap Merah&quot;, &quot;Nurul Iman Mosque Blok M Square&quot;, &quot;Jakarta Planetarium&quot;, &quot;Taman Prasasti Museum&quot;

Day 2: &quot;Benteng Heritage Museum&quot;, &quot;Palm Bay Water Park&quot;, &quot;Pelabuhan Perikanan Samudera Nizam Zachman&quot;, &quot;Sea World Ancol&quot;,

Day 3: &quot;Marunda Beach&quot;, &quot;Waterpark Transera&quot;.
