import curses
from curses import wrapper
from curses.textpad import Textbox

"""
NOTE: All coordinates are in the format (y, x) cuz thaz how curses works)
"""


def main(s):
    '''
    * Main function wrapped by wrapper so that terminal doesn't get messed
    * up by accident
    '''
    sh, sw = s.getmaxyx() # Get the height, and width of the terminal

    s.clear() # Clear the terminal
    curses.raw() # Get raw input from the keyboard, dangerous stuff
    curses.echo() # Echo the input keys to the screen
    curses.nl() # Set enter to correspond to new line, breaks if set to nonl()
    s.keypad(1) # Accept all kinds of inputs (like page up and page down), [unnecessary]

    # A title box with height 2 rows and width 100%,
    # starting at 1, 0
    title_box = s.subwin(2, sw, 1, 0)

    # Title of the program
    title_box.addstr('   Directory searching using Trie, fuzzysearch and DFS', curses.A_REVERSE)
    title_box.chgat(-1, curses.A_REVERSE) # That sweet background on the title
    

    # The thing on the bottom of the screen
    s.addstr(curses.LINES-1, 3, 'Start typing to search! Press <ESC> twice to exit.')


    # Draw a horizontal line under the title box
    title_box.hline(1, 3, '-', sw-7)

    # Create a search box of height 2 rows, width 100%
    # at 3, 0 
    search_box = s.subwin(2, sw, 3, 0)
    search_box.addstr('   Search: ') 
    search_box.hline(1, 3, '-', sw-7) # That line below search
    
    # The output box
    output_box = s.subwin(sh-5, sw-3, 5, 3)
    output_box.addstr('Results:\nTo find, you must seek')
    
    input_x = 11 # The x coordinate of the cursor, [do not change]

    # full_string is the search query
    full_string = ""
    
    # This is the expected format of output from the fuzzysearch
    matches = [(49, 'JimiHendrix'), (3, 'Gilmour')]
    
    # Main loop
    while True:

        # Get a character from the keyboard
        c = s.getch(3, input_x)

        if (c == 263 and not input_x == 11):
            # Check if backspace and not empty string [dont change]
            input_x -=1
            full_string = full_string[:-1]
            s.delch(3,input_x)
            output_box.clear()
            output_box.addstr(full_string)
            output_box.refresh()
        
        elif (c == 10 or (c == 263 and input_x == 11)):
            # Just some input validation, [dont change]
            continue
        else:
            # dun want a newline to be there in search string
            if chr(c) == "\n":
                continue
            full_string += chr(c)
            input_x += 1
            s.refresh() # refresh screen
        
        """
        
            Insert logic for fuzzysearch and put the results in matches
            after implementing it, go to line 29 and set matches to []
        
        """

        if (not full_string == "" and not matches == []):
            output_box.clear() # clear output box
            for match in matches: # add the matches to the output box
                output_box.addstr(f'{match[0]:>4} | {match[1]}\n')
        elif (full_string == ""):
            # If no input
            output_box.clear()
            output_box.addstr('To find, you must seek')
        else:
            # If no match
            output_box.clear()
            output_box.addstr('What you seek for lies beyond the relms of possibility')
        
        # refreesh all boxes 
        search_box.refresh()
        output_box.refresh()
        s.refresh()

        # since errthing cleared, the message at bottom needs to be written again
        s.addstr(curses.LINES-1, 3, 'Start typing to search! Press <ESC> twice to exit.')
        if (c == 27):
            # if escape key, shut program
           curses.endwin()
           break

wrapper(main)
