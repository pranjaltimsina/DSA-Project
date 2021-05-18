import curses
from curses import wrapper
import sys
from timeit import default_timer
import multiprocessing

from trie import main as trie
import fuzzy
from LRUcache import LRUCache

"""
NOTE: All coordinates are in the format (y, x) because that's how curses works)
"""
manager = multiprocessing.Manager()
mutex = manager.Lock()

INVALIDS = [
        10,
        263,
        262,
        360,
        331,
        339,
        330,
        338,
        258,
        259,
        260,
        261,
        410,
        343,
        575,
        580,
        579,
        577
        ]
INVALIDS += range(265, 275)


def validate_key(c: int):
    decoded = curses.keyname(c).decode('utf-8')
    if (c in INVALIDS or decoded.startswith('^') and not decoded.startswith('^[')):
        return False
    else:
        return True


cache = LRUCache(40)

def index_letters():
    with open('log.txt', 'a') as log:
        log.write("index thread\n")
    try:
        path = sys.argv[1]
    except IndexError:
        path = None

    file_list = trie(path)

    for i in range(ord('a'), ord('z')+1):
        full_string = chr(i)
        matches = []
        for file in file_list:
            file_name = file.split('/')[-1]
            if ('.' in file_name):
                out = fuzzy.fuzzy_match(full_string, file_name)
                if out[0]:
                    full_path = "/".join(file.split('/')[-3:-1])
                    if len(full_path) > 45:
                        full_path = "..." + full_path[-42:]
                    matches.append((out[1], file_name, full_path))
        matches.sort(key=lambda x: x[0], reverse=True)
        mutex.acquire()
        cache.put(full_string, matches)
        mutex.release()

def main(s):
    '''
    * s is the whole screen as an object
    * Main function wrapped by wrapper so that terminal doesn't get messed up
    * by accident
    '''

    with open('log.txt', 'a') as log:
        log.write("Curses thread\n")

    # Accept path as command line argument
    try:
        path = sys.argv[1]
    except IndexError:
        path = None

    # Define colors
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    # Make the trie
    # trie.main returns list of all possible paths
    file_list = trie(path)
    sh, sw = s.getmaxyx()  # Get the height, and width of the terminal

    s.clear()  # Clear the terminal
    curses.raw()  # Get raw input from the keyboard
    curses.echo()  # Echo the input keys to the screen
    curses.nl()  # Set enter to correspond to new line

    # Create a title box with height 2 rows and width 100%, starting at 1, 0
    title_box = s.subwin(2, sw-7, 1, 3)
    title_box.addstr('Directory searching using Trie, fuzzysearch and DFS', curses.color_pair(2))
    # title_box.chgat(-1, curses.A_REVERSE)  # That sweet background on the title
    title_box.chgat(-1, curses.color_pair(5))  # That sweet background on the title
    title_box.hline(1, 0, '-', sw-7)

    # Create a search box of height 2 rows, width 100 at 3, 0
    search_box = s.subwin(2, sw, 3, 0)
    search_box.addstr('   Search: ', curses.color_pair(4))
    search_box.hline(1, 3, '-', sw-7)

    # The output box that covers the rest of the screen
    output_box = s.subwin(sh-5, sw-3, 5, 3)
    output_box.addstr('Results:\nTo find, you must seek!')

    # Instructions the bottom of the screen
    s.addstr(sh-1, 3, 'Start typing to search! Press <ESC> to exit.', curses.color_pair(3))

    input_x = 11  # The x coordinate of the cursor
    full_string = ""  # full_string is the search query

    # Store the output here, edit line 86 to format things appropriately

    new_file_list = file_list

    BACKSPACES = [127, 263]
    # Main loop


    while 1:
        # Get a character from the keyboard
        c = s.getch(3, input_x)
        if (c == 27):
            # Quit if <ESC> is pressed
            curses.endwin()
            sys.exit()
        elif c in BACKSPACES:
            # Check if backspace
            new_file_list = file_list
            s.addch(3, input_x, " ")
            s.addch(3, input_x+1, " ")
            s.addch(3, input_x+2, " ")
            if (not input_x == 11):
                # Check if not empty string
                input_x -= 1  # Decrement cursors x-coordinate
                full_string = full_string[:-1]  # Remove last char of search query
                s.delch(3, input_x)  # Remove the character from the screen
                output_box.clear()  # Clear the output box
            else:
                continue
        elif not validate_key(c):
            continue

        elif not chr(c) == "\n":
            # Add the chr to the search query and increment cursor position
            full_string += chr(c)
            input_x += 1

        matches = []
        time_taken = ""
        # Performing fuzzy search on each file in file system (reducing number of files searched on each query)
        start_time = default_timer()

        matches = cache.get(full_string)

        if matches is None:
            matches = []
            for file in new_file_list:
                file_name = file.split('/')[-1]
                if ('.' in file_name):
                    out = fuzzy.fuzzy_match(full_string, file_name)
                    if out[0]:
                        full_path = "/".join(file.split('/')[-3:-1])
                        if len(full_path) > 45:
                            full_path = "..." + full_path[-42:]
                        matches.append((out[1], file_name, full_path))
            matches.sort(key=lambda x: x[0], reverse=True)
            mutex.acquire()
            cache.put(full_string, matches)
            mutex.release()

        end_time = default_timer()
        if matches:
            new_file_list = []
            for match in matches:
                full_file_path = match[2]+'/'+match[1]
                new_file_list.append(full_file_path)
        time_taken = f"{len(matches)} matches in {(end_time - start_time) * 1000} ms"
        if (not (full_string == "" or matches == [])):
            # Clear the output box and add the matches
            output_box.clear()
            if len(matches) > sh - 10:
                temp_matches = matches[:sh-11]
            else:
                temp_matches = matches

            for match in temp_matches:
                output_box.addstr(f'{match[0]:>4} | ')
                output_box.addstr(f'.../{match[2]:<45}', curses.color_pair(2))
                output_box.addstr(f' | {match[1]}\n')

        elif (full_string == ""):
            # Message if there is no input
            output_box.clear()
            output_box.addstr('To find, you must seek!')

        else:
            # Message if there are no matches
            output_box.clear()
            output_box.addstr('What you seek for lies beyond the realms of possibility!')

        # refreesh all boxes
        search_box.refresh()
        output_box.refresh()
        s.refresh()

        # since everything cleared, the message at bottom needs to be written
        s.addstr(sh-2, 3, time_taken, curses.color_pair(2))
        s.addstr(sh-1, 3, 'Start typing to search! Press <ESC> to exit.', curses.color_pair(3))


if __name__ == "__main__":
    indexer = multiprocessing.Process(target=index_letters)
    main_loop = multiprocessing.Process(target=wrapper, args=(main,))
    indexer.start()
    main_loop.start()
    indexer.join()
    main_loop.join()
