# Minesweeper with AI

### Usage

run `pip3 install -r requirements.txt`

run `python runner.py`


![Example Usage](https://i.imgur.com/ePZM6ZB.png)

### How it works

The AI uses model checking to determine the best move. Internally there is a knowledge base. Each sentence in the knowledge base has information about a set of cells and the count of mines for that set. For example cells={(0,0), (0,1), (1,0)} count = 3 represents that with the given set all cells are mines. The knowledge base is updated with information from moves and inferences.

### Issues I ran across
I had trouble with infinite loops while checking an inference. This gave me a great opportunity to work with the debugger in python. An example of the issue I was having is 
when a sentence is a subset of another sentence, an inference can be made and then another useless inference can be made from the inferred sentence.
`{(0,0), (1,1)} = 1 is a subset of {(0,0), (1,1), (1,0)} = 1`.
We can infer that
`{1,0} = 0`
My issue was when I added the new inference to my knowledge base I kept inferring the sentences it was derived from. The fix was to ensure the knowledge base contained only unique sentences. 
