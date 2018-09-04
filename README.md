nfl-stat-scraper
================
Get NFL statistics of all games and players since 2012. 

Data collected through this script includes information about potential response variables that *could* be interesting to the user, including:
- which team won the game
- whether or not the favored NFL team beat the spread
- whether the teams involved in each game scored more points than the over/under

Predictor variables that may be useful were also collected. I won't mention examples here because there are numerous team- and player-level statistics available. For the full data sets, check out the [corresponding page within the project](https://github.com/b-o-l-l-a/nfl-stat-scraper/tree/obj-oriented-classes/data/external)

### obj-oriented-classes branch
This particular project was conducive to using python classes because of how hierarchical the relevant concepts are. `Season`s have  `Week`s, `Week`s have `Game`s, `Game`s have `Team`s, `Team`s have `Player`s, and `Player`s have `Position`s. 

Each one of these objects is a separate class (taking methods/attributes of parent classes, as appropriate); all classes can be found [here](https://github.com/b-o-l-l-a/nfl-stat-scraper/tree/obj-oriented-classes/src/data/classes)

### other things to know about this project
- __Folder structure based on article found here__: https://www.kdnuggets.com/2018/07/cookiecutter-data-science-organize-data-project.html

- __Scripts to collect data__: `src/data` (output goes to `data/external`)

- __Additional steps__: I'm hoping to work on models which can somewhat-reliably predict the response variable(s) specified above. More to come!
