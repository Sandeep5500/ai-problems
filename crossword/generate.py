import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        x =  self.backtrack(dict())
        print(f"{x}")
        return x

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for var in self.domains:
            words = copy.deepcopy(self.domains[var])
            for word in words:    
                # print(f"{var} with word {word}")
                if var.length != len(word):
                    self.domains[var].remove(word)
        # raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revise = False

        domainx = copy.deepcopy(self.domains[x])

        for valx in domainx:
            foundy = False
            for valy in self.domains[y]:
                if valx == valy:
                    continue
                if self.crossword.overlaps[x,y] != None :
                    # print(f"{self.crossword.overlaps[x,y]}")
                    if valx[self.crossword.overlaps[x,y][0]] != valy[self.crossword.overlaps[x,y][1]]:
                        continue
                foundy = True
                break
            if foundy == False:
                revise = True
                self.domains[x].remove(valx)

        return revise        





        # raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = []
            for x in self.domains:
                for y in self.domains:
                    if x == y:
                        continue
                    if self.crossword.overlaps[x,y] != None and (x,y) not in arcs:
                        arcs.append((x,y))

        
        while arcs != []:
            (x,y) = arcs.pop(0)

            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False

                for var in self.domains:
                    if var != x and self.crossword.overlaps[var,x] != None:
                        arcs.append((var,x))

        return True      

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        if len(assignment) == len(self.domains):
            return True
        return False     

        # raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for x in assignment:
            if x.length != len(assignment[x]):
                return False
            for y in assignment:
                if assignment[x] == assignment[y] and x!=y:
                    return False
                if x!=y and self.crossword.overlaps[x,y] != None :
                    if assignment[x][self.crossword.overlaps[x,y][0]] != assignment[y][self.crossword.overlaps[x,y][1]]:
                        return False
        return True

    def second(self,x):
        return x[1]              

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        sorted_domain={ word : 0 for word in self.domains[var]}
        neighbours = []

        for y in self.domains:
            if y not in assignment and y!=var and self.crossword.overlaps[var,y] != None :
                neighbours.append((y,self.crossword.overlaps[var,y][0],self.crossword.overlaps[var,y][1]))

        for val in self.domains[var]:
            for y, i, j in neighbours:
                for word in self.domains[y]:
                    if val[i] != word[j] or val == word:
                        sorted_domain[val]+=1

        return sorted(sorted_domain, key = self.second)                
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        min_vars = []
        mini = 3000
        for x in self.domains:
            if x not in assignment:
                if len(self.domains[x]) < mini:
                    mini = len(self.domains[x])
                    min_vars=[]
                    min_vars.append(x)
                elif self.domains[x] == mini:
                    min_vars.append(x)

        mini = 3000
        select_var = None            

        for var in min_vars:
            if mini > len(self.crossword.neighbors(var)):
                mini = len(self.crossword.neighbors(var))
                select_var = var
        return var
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        # result = False

        for val in self.order_domain_values(var,assignment):
            assignment[var] = val
            if self.consistent(assignment):           
                result = self.backtrack(assignment)
                   
                if result != None:
                    return result            
            assignment.pop(var)   

        return None        




        # raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
