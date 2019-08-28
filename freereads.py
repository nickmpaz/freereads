import sys, curses, time
from components.freereads_components import *   
from components.curses_components import *
from utils.libgen import *  
from utils.gmail import *

def main(stdscr):
    
    stdscr.refresh()
    
    search_bar = SearchBarComponent(3, 200, 0, 0)
    scroll_page = ScrollPage(27, 200, 3, 0)
    text_box = TextBox(12,200,30,0)
    progress_bar = ProgressBarComponent(12,200,30,0)
    libgen = LibGen()

    
    while True:
         
        text_box.content = scroll_page.items[scroll_page.focus] if scroll_page.focus != -1 else {}

        scroll_page.draw()
        text_box.draw()
        search_bar.draw()

        curses.curs_set(scroll_page.focus == -1)
        ch = stdscr.getkey()

        if ch == '\n': 

            if scroll_page.focus == -1:
                scroll_page.items = libgen.search(search_bar.query)

            else:
                current_book = scroll_page.get_current_item()
                filename = (
                    "books/" + 
                    current_book['title'].replace(" ", "-") + 
                    "." + current_book["extension"]
                )

                text_box.win.clear()
                text_box.win.refresh()

                libgen.download(current_book, filename, progress_bar)
                time.sleep(1)

                send_email(filename, progress_bar)
                time.sleep(1)

                curses.flushinp()

        elif ch == 'KEY_BACKSPACE':

            if scroll_page.focus == -1: 
                search_bar.query = search_bar.query[:-1]

        elif ch == 'KEY_DC':

            if scroll_page.focus == -1:
                search_bar.query = ""

        elif ch == 'KEY_UP': 

            scroll_page.decrement_focus()
                    

        elif ch == 'KEY_DOWN': 

            scroll_page.increment_focus()

        else: 
            search_bar.query += ch
    

try: curses.wrapper(main)
except KeyboardInterrupt: sys.exit()
except: raise