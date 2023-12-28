import ndsk
import pyperclip
from bs4 import BeautifulSoup
import requests
import time




def main():
    last_search = ""
    # while loop that occasionally checks the clipboard
    while True:
        # wait some time
        try:
            board = pyperclip.paste()
            if (last_search != board and ndsk.is_kanji(board)):
                print("readings of", board + ":")
                jp_search_term, word_scrape_info, kanji_scrape_info = ndsk.parse_input(["ndsk", board, '-k', '-o'])
                page = requests.get(ndsk.BASE_URL + "%23kanji " + jp_search_term)
                soup = BeautifulSoup(page.content, "html.parser")
                out = ndsk.kanji_scrape(soup, kanji_scrape_info)
                print(out, end="")
                last_search = board
            elif last_search != board and ndsk.is_japanese_char(board):
                print(board + " is not kanji.")
                last_search = board
            elif last_search != board and ndsk.is_japanese_string(board):
                print("currently only single kanji characters are supported.")
                last_search = board
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()