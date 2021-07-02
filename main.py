from urllib.request import urlopen
from urllib.error import HTTPError
import sys
import validators

domains = ["https://github.com/",
           "https://vk.com/",
           "https://stackoverflow.com/users/",
           "https://twitter.com/",
           "https://stepik.org/users/"]

extendedDomains = []


invalidDomains = []
domainFlag = "-d"
refusedFlag = "-refused"

refused = False

usernames = []

def checkSite(url):
    try:
        html = urlopen(url)
    except HTTPError:
        return False
    else:
        return True

def userDomainCheck(domains, username, refusedDomains):
    for _ in domains:
        result = checkSite(_ + username)
        if result:
            print("    " + _ + username + ";")
        else:
            refusedDomains.append(_ + username)

def parseArguments():
    domain = False
    if refusedFlag in sys.argv[1:]:
        global refused
        refused = True
        sys.argv.remove(refusedFlag)

    for _ in sys.argv[1:]:

        if domain:
            if _.endswith("/"):
                if validators.url(_):
                    extendedDomains.append(_)
                else:
                    invalidDomains.append(_)
                domain = False

            if _.endswith(","):
                if validators.url(_[:-1]):
                    extendedDomains.append(_[:-1])
                else:
                    if validators.url(_[:-1] + '/'):
                        extendedDomains.append(_[:-1] + '/')
                    invalidDomains.append(_[:-1])

            if not _.endswith(",") and not _.endswith("/"):
                if validators.url(_ + '/'):
                    extendedDomains.append(_ + '/')
                else:
                    invalidDomains.append(_)
                domain = False
            continue

        if domainFlag.lower() in _ or domainFlag.upper() in _:
            domain = True
        else:
            usernames.append(_)

    if extendedDomains.__len__():
        if extendedDomains.__len__() == 1:
            print("New domain:", end=" ")
        else:
            print("New domains:", end=' ')
        print(*extendedDomains, sep=', ')

    if invalidDomains.__len__():
        if invalidDomains.__len__() == 1:
            print("Invalid domain:", end=" ")
        else:
            print("Invalid domains:", end=' ')
        print(*invalidDomains, sep=', ')

    print()

def usersCheck():
    for _ in usernames:
        print(_ + ":")
        refusedDomains = []
        userDomainCheck(domains, _, refusedDomains)
        userDomainCheck(extendedDomains, _, refusedDomains)

        global refused
        if refused and len(refusedDomains):
            print("    Refused domains:")
            for _ in refusedDomains:
                print("    " + _)
        print()

if(len(sys.argv) < 1):
    print("Error with arguments")
    sys.exit()
else:
    parseArguments()
    if len(usernames):
        usersCheck()
    else:
        print("Not found any users to check")
