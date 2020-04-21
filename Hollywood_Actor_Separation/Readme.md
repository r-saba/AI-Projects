# Find Degree of Separation Between Hollywood Actors

## Given two actors, the program returns the degree of separation between them as well as how they are connected.

### Usage

python degrees.py large

### How it works

Parses CSV's containing the Actors, Movies, and relationship between Actors and Movies. Using this information a graph is built where each node contains 3 pieces of information. The actor ID, the Parent node and the Movie Id. 
Using BFS the shortest degree of separation is found.

### Issues I ran across
The program took very long to run at first because I was only checking if the goal was reached after I added all the nodes to the frontier. I optimized the time drastically by checking if the node being added to the frontier is the goal before adding it. This way once the goal is found, other nodes are not unecessarily added to the frontier.
