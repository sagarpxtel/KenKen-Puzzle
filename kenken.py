####################################
# Name: Sagar Patel
####################################

# Main function and its tests are all the way at the bottom.

# All other functions are thoroughly tested, so you can hit run button and see all
# the test results (provided you have the check.py file within same directory)

import check # module used to test code 
import copy   #needed to copy a nested list to avoid mutating the consumed lists

###############################################################################
###############################################################################

class Puzzle:
    '''
      Fields:
            size: Nat 
            board: (listof (listof (anyof Str Nat Guess))
            constraints: (listof (list Str Nat (anyof '+' '-' '*' '/' '='))))
    '''
    
    def __init__(self, size, board, constraints):
        self.size=size
        self.board=board
        self.constraints=constraints
        
    def __eq__(self, other):
        return (isinstance(other,Puzzle)) and \
            self.size==other.size and \
            self.board == other.board and \
            self.constraints == other.constraints
    
    def __repr__(self):
        s='Puzzle(\nSize='+str(self.size)+'\n'+"Board:\n"
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.board[i][j],Guess):
                    s=s+str(self.board[i][j])+' '
                else:
                    s=s+str(self.board[i][j])+' '*12
            s=s+'\n'
        s=s+"Constraints:\n"
        for i in range(len(self.constraints)):
            s=s+'[ '+ self.constraints[i][0] + '  ' + \
                str(self.constraints[i][1]) + '  ' + self.constraints[i][2]+ \
                ' ]'+'\n'
        s=s+')'
        return s
    
###############################################################################
###############################################################################

class Guess:
    '''
    Fields:
            symbol: Str 
            number: Nat
    '''    
   
    def __init__(self, symbol, number):
        self.symbol=symbol
        self.number=number
        
    def __repr__(self):
        return "Guess('{0}',{1})".format(self.symbol, self.number)
    
    def __eq__(self, other):
        return (isinstance(other, Guess)) and \
            self.symbol==other.symbol and \
            self.number == other.number        

###############################################################################
############################################################################### 

class Posn:
    '''
    Fields:
            x: Nat 
            y: Nat
    '''    
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __repr__(self):
        return "Posn({0},{1})".format(self.x, self.y)
    
    def __eq__(self,other):
        return (isinstance(other, Posn)) and \
            self.x==other.x and \
            self.y == other.y 

###############################################################################
###############################################################################

#useful constants for testing
puzzle1 = Puzzle(4, [['a','b','b','c'],
                     ['a','d','e','e'],
                     ['f','d','g','g'],
                     ['f','h','i','i']],
                 [['a', 6,'*'],
                  ['b',3,'-'],
                  ['c',3,'='],
                  ['d',5,'+'],
                  ['e',3,'-'],
                  ['f',3, '-'],
                  ['g',2,'/'],
                  ['h',4,'='],
                  ['i',1,'-']])

puzzle1partial=Puzzle(4, [['a','b','b','c'],
                          ['a',2,1,4],
                          ['f',3,'g','g'],
                          ['f','h','i','i']],
                      [['a', 6,'*'],
                       ['b',3,'-'],
                       ['c',3,'='],
                       ['f',3, '-'],
                       ['g',2,'/'],
                       ['h',4,'='],
                       ['i',1,'-']])

# a partial solution to puzzle1 with a cage partially filled in
puzzle1partial2=Puzzle(4, [[Guess('a',2),'b','b','c'],
                          ['a',2,1,4],
                          ['f',3,'g','g'],
                          ['f','h','i','i']],
                      [['a', 6,'*'],
                       ['b',3,'-'],
                       ['c',3,'='],
                       ['f',3, '-'],
                       ['g',2,'/'],
                       ['h',4,'='],
                       ['i',1,'-']])

# a partial solution to puzzle1 with a cage partially filled in
#   but not yet verified 
puzzle1partial3=Puzzle(4, [[Guess('a',2),'b','b','c'],
                          [Guess('a',3),2,1,4],
                          ['f',3,'g','g'],
                          ['f','h','i','i']],
                      [['a', 6,'*'],
                       ['b',3,'-'],
                       ['c',3,'='],
                       ['f',3, '-'],
                       ['g',2,'/'],
                       ['h',4,'='],
                       ['i',1,'-']])

# The solution to puzzle 1
puzzle1soln=Puzzle(4, [[2,1,4,3],[3,2,1,4],[4,3,2,1],[1,4,3,2]], [])

puzzle2=Puzzle(6,[['a','b','b','c','d','d'],
                  ['a','e','e','c','f','d'],
                  ['h','h','i','i','f','d'],
                  ['h','h','j','k','l','l'],
                  ['m','m','j','k','k','g'],
                  ['o','o','o','p','p','g']],
               [['a',11,'+'],
                ['b',2,'/'],
                ['c',20,'*'],
                ['d',6,'*'],
                ['e',3,'-'],
                ['f',3,'/'],
                ['g',9,'+'],
                ['h',240,'*'],
                ['i',6,'*'],
                ['j',6,'*'],
                ['k',7,'+'],
                ['l',30,'*'],
                ['m',6,'*'],
                ['o',8,'+'],
                ['p',2,'/']])
                
#  The solution to puzzle 2
puzzle2soln=Puzzle(6,[[5,6,3,4,1,2],
                      [6,1,4,5,2,3],
                      [4,5,2,3,6,1],
                      [3,4,1,2,5,6],
                      [2,3,6,1,4,5],
                      [1,2,5,6,3,4]], [])


puzzle3=Puzzle(2,[['a','b'],['c','b']],[['b',3,'+'],
                                       ['c',2,'='],
                                       ['a',1,'=']])

puzzle3partial=Puzzle(2,[['a',Guess('b',1)],['c',Guess('b',2)]],
                      [['b',3,'+'],
                       ['c',2,'='],
                       ['a',1,'=']])
                  
puzzle3soln=Puzzle(2,[[1,2],[2,1]],[])      

###############################################################################
###############################################################################

def read_puzzle(fname):
    '''
    reads information from fname file and returns the info as Puzzle value.

    read_puzzle: Str -> Puzzle
    '''
    
    f = open(fname, 'r')
    n = int(f.readline())
    all_lines = f.readlines()
    f.close()
    
    first_half = all_lines[:n]
    second_half = all_lines[n:]
    p_board = []
    p_constraints = []
    
    for i in first_half:
        split = i.split()
        p_board.append(split)
    for i in second_half:
        split = i.split()
        p_constraints.append(split)
    for i in p_constraints:
        i[1] = int(i[1])
    return Puzzle(n, p_board, p_constraints)
        
    
   
check.expect("Ta1", read_puzzle("inp1.txt"), puzzle1 )  
check.expect("Ta2", read_puzzle("inp2.txt"), puzzle3 ) 

###############################################################################
###############################################################################

def print_sol(puz, fname):
    '''
    prints the Puzzle puz in fname file
    
    print_sol: Puzzle Str -> None
    '''
    
    w_file = open(fname, 'w')
    for i in puz.board:
        while i != []:
            num = str(i[0])
            w_file.write(num)
            w_file.write("  ")
            i = i[1:]
        w_file.write("\n")
    w_file.close()
            
            
        
  
check.set_file_exact("out1.txt", "result1.txt")               
check.expect("Tb1", print_sol(puzzle1soln, "out1.txt"), None)

check.set_file_exact("out2.txt", "result2.txt")
check.expect("Tb2", print_sol(puzzle2soln, "out2.txt"), None)

###############################################################################
###############################################################################

def find_blank(puz):
    '''
    returns the position of the first blank space in puz, or False if no cells 
    are blank.  If the first constraint has only guesses on the board, 
    find_blank returns 'guess'.  
    
    find_blank: Puzzle -> (anyof Posn False 'guess')
    
    Examples:
    find_blank(puzzle1) => Posn(0 0)
    find_blank(puzzle3partial) => 'guess'
    find_blank(puzzle2soln) => False
    '''
    
    rows = 0
    cols = 0
    
    if puz.constraints == []:
        return False
    pos = puz.constraints[0][0]
    for i in puz.board:
        for j in range(len(i)):
            if i[j] == pos:
                cols = j
                return Posn(cols, rows)
        rows += 1
    return "guess"


check.expect("Tc", find_blank(Puzzle(3, [["b","c","a"],["a","a","a"],      
                                          ["d","a","e"]],
                                          [["a",18,"*"],["b",1,"="],["c",2,"="],
                                           ["d",3,"="],["e",1,"="]])), 
             Posn(2,0))



###############################################################################
###############################################################################

def used_in_row(puz,pos):
    '''
    returns a list of numbers used in the same row as (x,y) position, pos, 
    in the given puz. 
    
    used_in_row: Puzzle Posn -> (listof Nat)
    '''
    
    row_y = pos.y
    r_strings = 0 # just a empty placeholder
    length = puz.size
    r_start = []
    block = puz.board[row_y]
    for i in block:
        if type(i) == str:
            r_strings = 0  # just a empty placeholder
        elif type(i) == int:
            r_start.append(i)
        else:
            r_start.append(i.number)
    return sorted(r_start) 


check.expect("Td1", used_in_row(puzzle1,Posn(1,1)), [])                
check.expect("Td2", used_in_row(Puzzle(4,[[4,'b','b',1],[Guess('a',2),'a',1,4],
                                          ['a','a','a','a'],[1,4,2,3]],
                                       [['a',144,'*'],['b',5,'+']])
                                       ,Posn(1,1)), [1,2,4])


###############################################################################
###############################################################################

def used_in_col(puz,pos):
    '''
    returns a list of numbers used in the same column as (x,y) position, pos, 
    in the given puz. 
    
    used_in_col: Puzzle Posn -> (listof Nat)
    '''
    
    n = 0
    c_strings = 0   # just a empty placeholder
    c_start = []
    cols_x = pos.x
    c_size = puz.size
    while n < c_size:
        x = puz.board[n][cols_x]
        if type(x) == str:
            c_strings = 0   # just a empty placeholder
        elif type(x) == int:
            c_start.append(x)
        else:
            c_start.append(x.number)            
        n += 1 
    return sorted(c_start)    
    
 
check.expect("Td3", used_in_col(puzzle1partial2,Posn(1,0)), [2,3])  
check.expect("Td4", used_in_col(puzzle2soln,Posn(3,5)), [1,2,3,4,5,6])  

###############################################################################
###############################################################################

def available_vals(puz,pos):
    '''
    returns a list of valid entries for the (x,y) position, pos, 
    of the consumed puzzle, puz.
    
    available_vals: Puzzle Posn -> (listof Nat)
    '''
    
    total_cells = used_in_col(puz,pos) + used_in_row(puz,pos)
    container = []
    n = puz.size
    num = 1
    
    for i in range(n):
        container.append(i + 1)
    for i in total_cells:
        if i in container:
            container.remove(i)
    return sorted(container)



check.expect("Te1", available_vals(puzzle1partial, Posn(2,2)), [2,4])
check.expect("Te2", available_vals(Puzzle(4, [['b','b',Guess('a',3),
                                               Guess('a',1)],
                                              ['b',3,'a','a'],
                                              [3,1,'a',2],
                                              [1,4,'a',3]],
                                          [['a',15,'+'],['b',8,'+']]),
                                   Posn(2,1)), [1,2,4])


###############################################################################
###############################################################################

def place_guess(brd,pos,val):
    '''
    fills in the (x,y) position, pos, of the board, brd, with the a guess with 
    value, val
    
    place_guess: (listof (listof (anyof Str Nat Guess))) Posn Nat 
                       -> (listof (listof (anyof Str Nat Guess)))
    '''
    
    res=copy.deepcopy(brd) # a copy of brd is assigned to res without any 
                           # aliasing to avoid mutation of brd. 
                           #  You should update res and return it
    
    col_f = pos.x                           
    row_f = pos.y
    pos_f = res[row_f][col_f]
    guess = Guess(pos_f, val)
    pos_f = guess
    guess = pos_f
    res[row_f][col_f] = guess
    return res
    

check.expect("Tf1", place_guess(puzzle3.board, Posn(1,1),2), 
             [['a','b'],['c',Guess('b',2)]])
check.expect("Tf2", place_guess(puzzle1partial2.board, Posn(0,1),3), 
             puzzle1partial3.board)


###############################################################################
###############################################################################

def fill_in_guess(puz, pos, val):
    '''
    fills in the pos Position of puz's board with a guess with value val
    
    fill_in_guess: Puzzle Posn Nat -> Puzzle
    '''
    
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    tmp=copy.deepcopy(res.board)
    res.board=place_guess(tmp, pos, val)
    return res
 
check.expect("Tf3", fill_in_guess(puzzle1, Posn(3,2),5), 
             Puzzle(4,[['a','b','b','c'],
                      ['a','d','e','e'],
                      ['f','d','g',Guess('g',5)],
                      ['f','h','i','i']], puzzle1.constraints))



###############################################################################
###############################################################################

def guess_valid(puz):
    '''
    determines if the guesses in puz satisfy their constraint
    
    guess_valid: Puzzle -> Bool

    '''
    
    board = puz.board
    container = []
    operator = puz.constraints[0][2]
    val = puz.constraints[0][1]
    
    for x in range(puz.size):
        for i in range(puz.size):
            cell = board[x][i]
            if type(cell) == Guess:
                container += [cell.number]
    if operator == "=":
        return container[0] == val
    elif operator == "+":
        return sum(container) == val
    elif operator == "-":
        return abs(container[0] - container[1]) == val
    elif operator == "*":
        multi = 1
        while container != []:
            multi = multi*container[0]
            container = container[1:]
        return multi == val
    elif operator == "/":
        return max(container) // min(container) == val


check.expect("Tg1", guess_valid(puzzle3partial), True)
check.expect("Tg2", guess_valid(Puzzle(2,[[Guess('a',2),Guess('a',1)],
                                          [Guess('a',1),Guess('a',2)]],
                                       [['a',4,'+']])), False)

check.expect("Tg3", guess_valid(Puzzle(2,[[Guess('a',2),Guess('a',1)],   
                                          [Guess('a',1),Guess('a',2)]],
                                       [['a',4,'*']])), True)


                 
###############################################################################
###############################################################################

def apply_guess(puz):
    '''
    converts all guesses in puz into their corresponding numbers and removes 
    the first contraint from puz's list of contraints
    
    apply_guess:  Puzzle -> Puzzle
    '''
    
    res=Puzzle(puz.size, copy.deepcopy(puz.board), 
                             copy.deepcopy(puz.constraints))
                   # a copy of puz is assigned to res without any 
                   # aliasing to avoid mutation of puz. 
                   #  You should update res and return it 
    n = 0
    h_board = res.board
    h_size = res.size
    
    while n < h_size:
        n_sub = 0
        while n_sub < h_size:
            if (not(str(h_board[n][n_sub]).isalpha()) and
                (not(str(h_board[n][n_sub]).isdigit()))):
                h_board[n][n_sub] = h_board[n][n_sub].number
                n_sub += 1
            else:
                n_sub += 1
        n += 1
    res.constraints = res.constraints[1:]
    return res    
    

check.expect("Th1", apply_guess(Puzzle(6,[[5,6,3,4,1,2],[6,1,4,5,2,3],
                                          [4,5,2,3,6,1],[3,4,1,2,5,6],
                                          [2,3,6,1,4,5],
                                          [1,2,5,Guess('p',6),Guess('p',3),4]],
                                       [['p',2,'/']])), puzzle2soln)
              


###############################################################################
###############################################################################

def neighbours(puz):                   
    '''
    returns a list of next puzzles after puz in the implicit graph
    
    neighbours: Puzzle -> (listof Puzzle)
    '''
    
    tmp=Puzzle(puz.size, copy.deepcopy(puz.board), 
               copy.deepcopy(puz.constraints))
    # a copy of puz is assigned to tmp without any 
    # aliasing to avoid mutation of puz.
    
    val = find_blank(puz)
    container = []
    if not(val):
        return container
    elif val == 'guess':
        if guess_valid(tmp):
            container.append(apply_guess(tmp))
    else:
        availabble = available_vals(tmp,val)
        for x in availabble:
            container.append(fill_in_guess(tmp,val,x))
    return container     
    
    
    
check.expect("Ti1", neighbours(puzzle2soln), [])
check.expect("Ti2", neighbours(puzzle3), [Puzzle(2,[['a',Guess('b',1)],
                                                    ['c','b']],
                                                 [['b',3,'+'], ['c',2,'='],
                                                  ['a',1,'=']]),
                                          Puzzle(2,[['a',Guess('b',2)],
                                                    ['c','b']],[['b',3,'+'],
                                                                ['c',2,'='],
                                                                ['a',1,'=']])])
puz1=Puzzle(4,[[4,2,'a','a'],['b', Guess('c',3),'a',4],
               ['b', Guess('c',1),Guess('c',4),2],
               [1,Guess('c',4),Guess('c',2),3]],
            [['c',96,'*'],['b',5,'+'],['a',3,'*']])
puz2=Puzzle(4,[[4,2,'a','a'],['b',3,'a',4],['b',1,4,2],
               [1,4,2,3]],[['b',5,'+'],['a',3,'*']])
check.expect("Ti3",neighbours(puz1),[puz2])

###############################################################################
###############################################################################
###################(!!!!!!MAIN FUNCTION!!!!!!)################################
###############################################################################
###############################################################################
###############################################################################


def solve_kenken(orig):
    '''
    finds the solution to a KenKen puzzle, orig, or returns False 
    if there is no solution.  
    
    solve-kenken: Puzzle -> (anyof Puzzle False)
    '''
    
    to_visit=[]
    visited=[]
    to_visit.append(orig)
    while to_visit!=[]:
        if find_blank(to_visit[0])==False:
            return to_visit[0]
        elif to_visit[0] in visited:
            to_visit.pop(0)
        else:
            nbrs = neighbours(to_visit[0])
            new = list(filter(lambda x: x not in visited, nbrs))
            new_to_visit=new + to_visit[1:] 
            new_visited= [to_visit[0]] + visited
            to_visit=new_to_visit
            visited=new_visited
            
    return False


check.expect("game1",solve_kenken(puzzle3partial),False)
check.expect("game2",solve_kenken(puzzle1), puzzle1soln)
check.expect("game3",solve_kenken(puzzle2), puzzle2soln)
check.expect("game4",solve_kenken(puzzle3), puzzle3soln)
check.expect("game5",solve_kenken(puzzle3soln), puzzle3soln)

###############################################################################
###############################################################################