import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if (len(self.cells) == self.count):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0):
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if(cell in self.cells):
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if(cell in self.cells):
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        x = cell[0]
        y = cell[1]
        topOfxIsInGird = x-1 >= 0
        bottomOfxIsInGrid = x+1 <= self.width-1
        leftOfyIsInGrid = y-1 >= 0
        rightOfyIsInGrid = y+1 <= self.height-1
        newSentence = set()

        if(topOfxIsInGird):
            # topleft neighbor cell
            if(leftOfyIsInGrid):
                topLeft = (x-1, y-1)
                if(topLeft not in self.mines or topLeft not in self.safes):
                    newSentence.add(topLeft)
            # topMiddle
            topMiddle = (x-1, y)
            if(topMiddle not in self.mines or topMiddle not in self.safes):
                newSentence.add(topMiddle)
            # topRight
            if(rightOfyIsInGrid):
                topRight = (x-1, y+1)
                if(topRight not in self.mines or topRight not in self.safes):
                    newSentence.add(topRight)

        if(bottomOfxIsInGrid):
            # bottomLeft
            if(leftOfyIsInGrid):
                bottomLeft = (x+1, y-1)
                if(bottomLeft not in self.mines or bottomLeft not in self.safes):
                    newSentence.add(bottomLeft)
            # bottomMiddle
            bottomMiddle = (x+1, y)
            if(bottomMiddle not in self.mines or bottomMiddle not in self.safes):
                newSentence.add(bottomMiddle)
            # bottomRight
            if(rightOfyIsInGrid):
                bottomRight = (x+1, y+1)
                if(bottomRight not in self.mines or bottomRight not in self.safes):
                    newSentence.add(bottomRight)

        if(leftOfyIsInGrid):
            centerLeft = (x, y-1)
            if(centerLeft not in self.mines or centerLeft not in self.safes):
                newSentence.add(centerLeft)
        if(rightOfyIsInGrid):
            centerRight = (x, y+1)
            if(centerRight not in self.mines or centerRight not in self.safes):
                newSentence.add(centerRight)

        sentenceToAdd = Sentence(newSentence, count)
        self.knowledge.append(sentenceToAdd)
        # Case where count = length
        mine_cells = []
        for sentence in self.knowledge:
            # print("running")
            if(sentence.known_mines() is not None):
                for cell in sentence.known_mines():
                    mine_cells.append(cell)
            for cell in mine_cells:
                sentence.mark_mine(cell)
                self.mines.add(cell)

        # Case where count is 0
        safe_cells = []
        for sentence in self.knowledge:
            # print("running")
            if(sentence.known_safes() is not None):
                for cell in sentence.known_safes():
                    safe_cells.append(cell)
            for cell in safe_cells:
                sentence.mark_safe(cell)
                self.safes.add(cell)
        for sentence in self.knowledge:
            if(len(sentence.cells) == 0):
                self.knowledge.remove(sentence)

        # Case where we have a subset of another set
        used_cells = []
        repeatedSentence = False
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:

                if (sentence1 != sentence2 and len(sentence1.cells) != 0 and len(sentence2.cells) != 0 and sentence1.cells.issubset(sentence2.cells)):

                    for usedCells in used_cells:
                        if(len(sentence1.cells) == len(usedCells) and sentence1.cells.issubset(usedCells)):
                            repeatedSentence = True
                        elif(len(sentence2.cells) == len(usedCells) and sentence2.cells.issubset(usedCells)):
                            repeatedSentence = True

                    if(not repeatedSentence):
                        newSentenceCells = sentence2.cells.difference(
                            sentence1.cells)
                        newCount = sentence2.count - sentence1.count
                        self.knowledge.append(
                            Sentence(newSentenceCells, newCount))
                        used_cells.append(sentence1.cells)
                        used_cells.append(sentence2.cells)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(0, self.height):
            for j in range(0, self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    return move
        return None
