import curses
from curses import wrapper
from curses.textpad import Textbox

def main(s):
    '''
    * Main function wrapped by wrapper so that terminal doesn't get messed
    * up by accident
    '''
    sh, sw = s.getmaxyx() # Get the height, and width of the terminal

    s.clear() # Clear the terminal
    curses.raw()
    curses.echo()
    curses.nl()
    s.keypad(1)
    # Display the height and width of the terminal

    # A title box with height 2 rows and width 100%,
    # starting at 0, 0
    title_box = s.subwin(2, sw, 1, 0)

    # Title of the program
    title_box.addstr('   Directory searching using Trie, fuzzysearch and DFS', curses.A_REVERSE)
    title_box.chgat(-1, curses.A_REVERSE)
    
    s.addstr(curses.LINES-1, 3, 'Start typing to search! Press <ESC> twice to exit.')
    # Draw a horizontal line under the title box
    title_box.hline(1, 3, '-', sw-7)

    search_box = s.subwin(2, sw, 3, 0)
    search_box.addstr('   Search: ')
    search_box.hline(1, 3, '-', sw-7)

    output_box = s.subwin(sh-5, sw-3, 5, 3)
    output_box.addstr('Results:\n')
    

    input_x = 11
    full_string = ""
    while True:
        c = s.getch(3, input_x)
        if (c == 263 and not input_x == 11):
            input_x -=1
            full_string = full_string[:-1]
            s.delch(3,input_x)
            output_box.clear()
            output_box.addstr(full_string)
            output_box.refresh()

        elif (c== 263 and input_x == 11):
            continue
        else:
            full_string += chr(c)
            input_x += 1
            s.refresh()
            output_box.clear()
            output_box.addstr(full_string)
            output_box.refresh()
        search_box.refresh()
        output_box.refresh()
        s.refresh()
        s.addstr(curses.LINES-1, 3, 'Start typing to search! Press <ESC> twice to exit.')
        if (c == 27):
           curses.endwin()
           break

wrapper(main)
