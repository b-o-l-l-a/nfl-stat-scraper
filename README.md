nfl-stat-scraper
================
Get NFL statistics of all games and players since 2012

### obj-oriented-classes branch
This particular project was conducive to using python classes because of how hierarchical the relevant concepts are. `Season`s have  `Week`s, `Week`s have `Game`s, `Game`s have `Team`s, `Team`s have `Player`s, and `Player`s have `Position`s. 

Each one of these objects is a separate class (taking methods/attributes of parent classes, as appropriate); all classes can be found [here](https://github.com/b-o-l-l-a/nfl-stat-scraper/tree/obj-oriented-classes/src/data/classes)
