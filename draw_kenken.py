import tkinter
import time

import kenken

class BorderedFrame(tkinter.Frame):
  def __init__(self, master, bordercolor=None, borderleft=0, bordertop=0, 
               borderright=0, borderbottom=0, interiorwidget=tkinter.Frame, 
               **kwargs):
    tkinter.Frame.__init__(self, master, background=bordercolor, bd=0, 
                           highlightthickness=0)

    self.interior = interiorwidget(self, **kwargs)
    self.interior.pack(padx=(borderleft, borderright), pady=(bordertop, 
                                                             borderbottom))

def draw_board(puz, root):
  cells = []
  for r in range(puz.size):
    row = []
    for c in range(puz.size):
      if r == 0 or puz.board[r][c] != puz.board[r-1][c]:
        bordertop = 1
      else:
        bordertop = 0
  
      if c == 0 or puz.board[r][c-1] != puz.board[r][c]:
        borderleft = 1
      else:
        borderleft = 0
  
      label = BorderedFrame(root, width=8, height=4, bordercolor='#000000', 
                            borderleft=borderleft, borderright=0, 
                            bordertop=bordertop, borderbottom=0, 
                            interiorwidget=tkinter.Label, font=('Arial', 14))
      label.grid(row=r, column=c)
      row.append(label)
    cells.append(row)
    
    for constr in puz.constraints:
        placed = False
        for r in range(puz.size):
            if placed:
                break
            for c in range(puz.size):
                if puz.board[r][c] != constr[0]:
                    continue
                placed = True
                cstr = str(constr[1])
                if constr[2] != '=':
                    cstr += ' ' + constr[2]
                label = tkinter.Label(text=cstr, bg='#ffffff', 
                                      font=('Arial', 12))
                label.place(x=96 * c + 5, y=96 * r + 5)
                break
  return cells

def update_board(cells, puz):
  for r in range(puz.size):
    for c in range(puz.size):
      if isinstance(puz.board[r][c], kenken.Guess):
        new_str = str(puz.board[r][c].number)
      else:
        new_str = str(puz.board[r][c])
      
      if new_str != cells[r][c].interior['text']:
        cells[r][c].interior['bg'] = '#ccccff'
      cells[r][c].interior['text'] = new_str
        
def colour_cells(cells, colour):
  for r in range(len(cells)):
    for c in range(len(cells)):
      cells[r][c].interior['bg'] = colour

def animate_puzzle(puz, speed = 1):
    import _tkinter
    try:
        animate_puzzle_run(puz, speed)
    except _tkinter.TclError:
        pass

def animate_puzzle_run(puz, speed):
    root = tkinter.Tk()
    root.lift()
    cells = draw_board(puz, root)
    update_board(cells, puz)
    to_visit=[]
    visited=[]
    to_visit.append(puz)
    while to_visit!=[] :
        if kenken.find_blank(to_visit[0])==False:
            colour_cells(cells, '#ccffcc')
            break
        elif to_visit[0] in visited:
            to_visit.pop(0)
        else:
            update_board(cells, to_visit[0])
            root.update_idletasks()
            root.update()
            time.sleep(0.5 / speed)
            colour_cells(cells, '#ffffff')
            root.update_idletasks()
            root.update()
            time.sleep(0.5 / speed)
    
            nbrs = kenken.neighbours(to_visit[0])
            new = list(filter(lambda x: x not in visited, nbrs))
            new_to_visit=new + to_visit[1:] 
            new_visited= [to_visit[0]] + visited
            to_visit=new_to_visit
            visited=new_visited

    if len(to_visit) == 0:
        colour_cells(cells, '#ffcccc')

    root.mainloop()
    
    
    
'''
Now, a big disclaimer. This was created for fun so you could play around with 
your completed solution. It's possible that the visualizations will be 
incorrect. Therefore you should not rely on this to debug or test your solution. 
Also, the code uses many Python features not discussed in class and is probably 
not a good example of style. Do not assume that because a feature is used here, 
that it can be used on your assignment or final exam.

animate_puzzle(kenken.puzzle1)


'''