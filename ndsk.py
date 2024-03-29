import sys
import requests
from bs4 import BeautifulSoup

# used for making searches on jisho
BASE_URL = "https://jisho.org/search/"

# used by `is_japanese_char()`. ranges from StackOverflow,
# reference: https://stackoverflow.com/questions/30069846/how-to-find-out-chinese-or-japanese-character-in-a-string-in-python
# TODO: remove unnecessary ranges if necessary
JAPANESE_CHAR_UNICODE_RANGES = [
    {"from": ord(u"\u3330"), "to": ord(u"\u33ff")},
    {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
    {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
    {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
    {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
    {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
    {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
    {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
    {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
    {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
    {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
    {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
    {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}
]


def main():
    jp_search_term, word_scrape_info, kanji_scrape_info = parse_input(sys.argv)
    req_list = []
    out = ""        # output string

    verbose = False
    if kanji_scrape_info is not None:
        verbose = "verbose" in kanji_scrape_info
    elif word_scrape_info is not None:
        verbose = "verbose" in word_scrape_info

    # # if we need to scrape the #word page for this kanji, add a request for it
    if word_scrape_info != []:
        req_list.append("%23word " + jp_search_term)
    # same as above for the #kanji page.
    if kanji_scrape_info != []:
        req_list.append("%23kanji " + jp_search_term)

    for req in req_list:
        page = handle_request(BASE_URL + req, verbose)
        soup = BeautifulSoup(page.content, "html.parser") 
        
        if "word" in req:
            out += word_scrape(soup, word_scrape_info)
        else: # must be a kanji request
            out += kanji_scrape(soup, kanji_scrape_info)

    print(out, end="") # no \n... that's automatically added by the scraping functions...

"""
This function makes a request to the given url and returns the page as a
requests.Response object.

It also handles any errors that might arise.
"""
def handle_request(url, verbose = False):
    try:
        page = requests.get(url, timeout=3)
        return page
    except requests.exceptions.Timeout:
        print("Connection timed out.")
        exit(1)
    except requests.exceptions.HTTPError:
        print("Invalid HTTPS response; please try again.")
        exit(1)
    except requests.exceptions.ConnectionError:
        print("Could not connect. Are you connected to the internet?")
        exit(1)
    except requests.RequestException as ex:
        if verbose:
            print(f"A {type(ex).__name__} error was raised when making a request to {url}.")
        else:
            print("Something went wrong; please try again.")

"""
This function scrapes the #word page for the given input.

Or, at least it will. For now, this isn't supported, but it will eventually
allow the user to grab info such as the meaning of vocab words and their
possible readings.

TODO:
* optimization... this is currently pretty slow.
* document me
* test me
"""
def word_scrape(soup, word_scrape_info):
    out = ""
    verbose = "verbose" in word_scrape_info

    for elem in word_scrape_info:
        if elem == "def":  # get the definition...
            try:
                definition_blocks = soup.find_all("div", class_="concept_light clearfix")

                # for now, get the first few definitions of the first block of definitions.
                definition_divs = (definition_blocks[0]
                                   .find("div", class_="concept_light-meanings medium-9 columns")
                                   .find("div", class_="meanings-wrapper")
                                   .find_all("div", class_="meaning-wrapper"))

                definitions = []
                for div in definition_divs:
                    definitions.append(div.find("span", class_="meaning-meaning"))

                if definitions is not None:  # if we found definitions
                    out += "Definitions: "
                    for definition in definitions:
                        if definition is not None:
                            out += definition.text + ", "
                    if out[-2:] == ", ":
                        out = out[:-2]
                    out += ".\n"
                elif verbose:
                    print("No definitions found.")
            except AttributeError:
                if verbose:
                    print("No definitions found.")
            except Exception as e:
                print(type(e))

        else:  # probably "verbose" or potentially an invalid element that should be ignored.
            pass

    return out

"""
This function scrapes the #kanji and returns a string containing
the information requested by the user. 

For now, it is capable of grabbing the kun'yomi and on'yomi readings 
of a given kanji. Ideally, it will eventually allow the user to grab 
any info from the #kanji page as needed.

This function takes a list of strings as input. The strings tell 
the function which parts of the page the user is requesting. For example:

    kanji_scrape(soup, ["kun"])

will return a string with the kun'yomi readings of the requested kanji.
The order of the elements in this list matters, so

    kanji_scrape(soup, ["kun", "on"])

will print the kun'yomi readings first, then the on'yomi, whereas

    kanji_scrape(soup, ["on", "kun"])

will print the on'yomi first. The list is automatically generated by
the function `parse_input`.
"""
def kanji_scrape(soup, kanji_scrape_info):
    out = ""
    verbose = "verbose" in kanji_scrape_info

    for elem in kanji_scrape_info:
        if elem == "kun":
            try:
                readings = soup.find("div", class_="kanji-details__main-readings").find("dl", class_="dictionary_entry kun_yomi").find("dd", class_="kanji-details__main-readings-list").find_all("a")
                if readings is not None:
                    out += "Kun: "
                    for reading in readings:
                        out += reading.text.strip() + ", "
                    if out[-2:] == ", ":
                        out = out[:-2]  # if the last two chars are the comma/space, remove it.
                    out += "\n"
                elif verbose:
                    out += "No Kun'yomi readings found.\n"
            except AttributeError:  # can be thrown by soup.find() if the div dne
                if verbose:
                    out += "No Kun'yomi readings found.\n"

        elif elem == "on":
            try:
                readings = soup.find("div", class_="kanji-details__main-readings").find("dl", class_="dictionary_entry on_yomi").find("dd", class_="kanji-details__main-readings-list").find_all("a")
                if readings is not None:
                    out += "On: "
                    for reading in readings:
                        out += reading.text.strip() + ", "
                    if out[-2:] == ", ":
                        out = out[:-2]  # if the last two chars are the comma/space, remove it.
                    out += ".\n"
                elif verbose:
                    out += "No On'yomi readings found.\n"
            except AttributeError:  # can be thrown by soup.find() if the div dne
                if verbose:
                    out += "No On'yomi readings found.\n"

        elif elem == "meaning":
            try:
                meanings = soup.find("div", class_="kanji-details__main-meanings")
                if meanings is not None:
                    out += "Meaning: "
                    for meaning in meanings:
                        out += meaning.text.strip() + ", "
                    if out[-2:] == ", ":
                        out = out[:-2]  # if the last two chars are the comma/space, remove it.
                    out += ".\n"
                elif verbose:
                    out += "No meanings found.\n"
            except AttributeError:  # can be thrown by soup.find() if the div dne
                if verbose:
                    out += "No meanings found.\n"

        else:  # probably "verbose" or otherwise invalid, ignore it...
            pass

    return out


"""
This function takes in a character and determines whether or not it is a
japanese character by checking if falls within any of the unicode ranges
that such characters can be found in.

logic from StackOverflow, reference: https://stackoverflow.com/questions/30069846/how-to-find-out-chinese-or-japanese-character-in-a-string-in-python
"""
def is_japanese_char(char):
    return any([ascii_range["from"] <= ord(char) <= ascii_range["to"] for ascii_range in JAPANESE_CHAR_UNICODE_RANGES])


"""
This function returns True if a string of characters consists of only
japanese characters.
"""
def is_japanese_string(string):
    return all(is_japanese_char(char) for char in string)


"""
This function parses the command line input from the user and uses it to determing
how the webscraper should operate.

It will raise errors if the input is improperly formatted.

Proper input should be formatted as follows:

    ndkk [kanji] [flags ....]

ex.: get the on'yomi reading of '日':

    ndkk 日 -o

TODO:
* test me
* implement values passed into flags (ex. `ndkk 日 -m 2 -k 3` should return the top 2 meanings of 日 and its top 3 kun'yomi readings.)
* implement more rigorous input validation
    * #kanji page scrapes should not be possible on strings of length > 1, or strings with hiragana/katakana, or otherwise non-kanji characters.
    * should a single flag be allowed to appear in a command more than once?
"""
def parse_input(args):
    word_scrape_info = []
    kanji_scrape_info = []

    # nothing to do if we don't have even a kanji...
    if len(args) < 2:
        print("too few arguments")
        exit(1)
    
    # the first argument should be a japanese character / string of characters:
    if not is_japanese_string(args[1]):
        print(f"request on \"{args[1]}\" could not be made.")
        exit(1)
    
    # grab just the kanji term and remove it from the list of arguments
    jp_search_term = args[1] 
    args = args[2:] 

    if args is []:
        # do a generic info splash... for now, just print the kanji's inherent meaning, kun'yomi, and on'yomi
        kanji_scrape_info = ["meaning", "kun", "on"]
    
    else:
        # parse flags to give direction to the soup.
        for argument in args:
            if argument == "-m":
                kanji_scrape_info.append("meaning")
            elif argument == "-o":
                kanji_scrape_info.append("on")
            elif argument == "-k":
                kanji_scrape_info.append("kun")
            elif argument == "-d":
                word_scrape_info.append("def")
            elif argument == "-v" or argument == "--verbose":
                kanji_scrape_info.append("verbose")
                word_scrape_info.append("verbose")
            else:
                print(f"error: unrecognizable flag/argument \"{argument}\"")
                exit(1)
    
    # parsed info returned as a tuple to be unpacked in main...
    # first, the kanji / search term, 
    # then the info to be used in scraping the #word page,
    # and finally the info for scraping the #kanji page.
    # "verbose" is a bool that is sometimes used to display error information.
    return jp_search_term, word_scrape_info, kanji_scrape_info


if __name__ == "__main__":
    main()
