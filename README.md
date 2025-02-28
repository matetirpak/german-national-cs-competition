# german-national-cs-competition
This was my submission for the 2. round of the 42. German National CS Competition (42. Bundeswettbewerb Informatik) held in early 2024, rated with 41/40 points.
Despite this being my very first CS competition, I advanced to finals in Munich and became a prizewinner ("Preistraeger") in september, equivalent to #7-11.

The original German version of the problem descriptions can be found in "Aufgabenstellungen.pdf".

As for an English version, here are translations for the 2 problems I chose:

Problem 2: Stylish Packages

Numerous pieces of clothing have been bought and should be grouped into outfit-boxes. A piece is characterized by it's type and style. For example, type being "shirt" and style being "sporty". It has to be guaranteed that every piece inside a box has to be compatible with every other piece in terms of style. Whether two styles are compatible is defined in the input. For example, "elegant" and "formal" might fit together whilst "sporty" is not compatible with them. Additionally to the style compatibilities, each box has to include each clothing type at least once and at most three times.
Given as inputs are the amount of types, amount of styles, compatible style pairs, and pieces characterized by type, style and quantity.

A program has to be written which packages clothes in a way that the amount of unpackaged pieces is minimized.


Problem 3: Settlers

To prevent future epidemics, the government wants to design the colonization of a new area with special attention towards following conditions. Settlements have to have a distance of at least 10km towards each other. If the distance between two settlements is at least 20km, the decease will not spread between those. A health center can be placed at an arbitrary position. Settlements within a radius of 85km can not spread or be infected by the decease.

A program has to be written which given a concave polygon maximizes the amount of settlements whilst ensuring that decease spreading is impossible at every part of the area.