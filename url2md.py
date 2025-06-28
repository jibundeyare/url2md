# This script takes urls as input and outputs links in markdown format.
# The script accepts a single url, mutiple urls or the name of a file
# containing one or more urls.
# In the file, empty lines and lines starting with a sharp symbol are
# ignored.
# Urls are printed to stdout and errors are printed to stderr.

from requests.exceptions import HTTPError
import html
import os.path
import re
import requests
import sys
import time

# all special characters
# MARKDOWN_SPECIAL_CHARACTERS = r'\`*_{}[]<>()#+-.!|'

# special characters that need escaping when used in a link description
MARKDOWN_SPECIAL_CHARACTERS = r'\`*_'

MARKDOWN_ESCAPE_REGEX = re.compile(f'([{re.escape(MARKDOWN_SPECIAL_CHARACTERS)}])')
TITLE_TAG_REGEX = re.compile(r'<title\s*>\s*([^<]*)\s*</title\s*>', re.IGNORECASE + re.DOTALL + re.MULTILINE)
CR_LF_REGEX = re.compile('\r\n', re.MULTILINE)
CR_REGEX = re.compile('\r', re.MULTILINE)
LF_REGEX = re.compile('\n', re.MULTILINE)
TAB_REGEX = re.compile('\t', re.MULTILINE)
SPACES_REGEX = re.compile(' +', re.MULTILINE)

DELAY = 0.5

def usage():
    script = sys.argv[0]
    print("usage:")
    print(f"{script} url1 [url2] [url3] [...]")
    print("")

def markdown_escape(text: str) -> str:
    """Inspired by [python-telegram-bot/telegram/utils/helpers.py at 1fdaaac8094c9d76c34c8c8e8c9add16080e75e7 · python-telegram-bot/python-telegram-bot · GitHub](https://github.com/python-telegram-bot/python-telegram-bot/blob/1fdaaac8094c9d76c34c8c8e8c9add16080e75e7/telegram/utils/helpers.py#L149-L174)"""

    markdown = str(text)
    text = re.sub(MARKDOWN_ESCAPE_REGEX, r'\\\1', text)

    return text

def main() -> None:
    if len(sys.argv) < 2:
        # there must be at least one argument, a url or a file name
        # @note argument 0 is the script name
        usage()
        sys.exit(1)

    errors_count = 0
    urls = []

    if os.path.isfile(sys.argv[1]):
        # first argument is a file name
        filename = sys.argv[1]

        with open(filename) as file_handler:
            # read all urls from file
            urls = file_handler.readlines()
    else:
        # read all urls from cli arguments
        # @note argument 0 is the script name
        urls = sys.argv[1:]

    for url in urls:
        # remove newlines at end of string
        url = url.rstrip('\n')
        # remove spaces at end of string
        url = url.rstrip()
        # remove spaces at beginning of string
        url = url.strip()

        if url == '' or url[0] == '#':
            # skip empty lines and comments
            continue
        elif (url[0:8] != 'https://' and url[0:7] != 'http://') \
            or (url[0:7] == 'http://' and len(url) < 10) \
            or (url[0:8] != 'https://' and len(url) < 11):
            # url is not valid
            print(f"error: `{url}` is not a valid url", file=sys.stderr, flush=True)
            errors_count += 1
            continue

        try:
            # verify=False disables SSL certificate verification
            # timeout is in seconds
            # response = requests.get(url, verify=False, timeout=3.0)

            # timeout is in seconds
            response = requests.get(url, timeout=3.0)
            # raise an exception in case of http error
            response.raise_for_status()
        except HTTPError as http_error:
            # http error exception
            print(f"error: http error with url `{url}`: `{http_error}`", file=sys.stderr, flush=True)
            errors_count += 1

            # leave title empty
            title = ''
            markdown = f'[{title}]({url})'
            print(markdown, flush=True)

            continue
        except Exception as exception:
            # other (non http error) exception
            print(f"error: exception with url `{url}`: `{exception}`", file=sys.stderr, flush=True)
            errors_count += 1

            # leave title empty
            title = ''
            markdown = f'[{title}]({url})'
            print(markdown, flush=True)

            continue

        # assign encoding according to content
        # provided by charset_normalizer or chardet under the hood
        response.encoding = response.apparent_encoding

        # regex for <title>...</title>
        result = TITLE_TAG_REGEX.findall(response.text)

        markdown = ''

        if len(result) == 0:
            # no title found
            # use url as a title
            title = url
        else:
            # title found
            title = result[0]

            # get rid of zero-width space \u200b
            title = title.replace('\u200b', '')

            # get rid of html entitites
            title = html.unescape(title)

            # get rid of windows cr lf
            title = re.sub(CR_LF_REGEX, ' ', title)

            # get rid of windows cr
            title = re.sub(CR_REGEX, ' ', title)

            # get rid of windows lf
            title = re.sub(LF_REGEX, ' ', title)

            # get rid of tabs
            title = re.sub(TAB_REGEX, ' ', title)

            # get rid of multiple spaces
            title = re.sub(SPACES_REGEX, ' ', title)

            # if title == '':
            #     # title is empty
            #     # use url as a title
            #     title = url

        # escape markdown special characters
        title = markdown_escape(title)

        markdown = f'[{title}]({url})'

        print(markdown, flush=True)

        # add some delay to avoid being considered as a bot
        time.sleep(DELAY)

    # exit code is the number of errors encountered
    # i.e. 0 errors in case of full success
    sys.exit(errors_count)

if __name__ == '__main__':
    main()

