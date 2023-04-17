from libgen_api import LibgenSearch

def handleValidation(type: str, search: str):
    valid_types = ["author", "title"]
    in_string = type.lower()
    if in_string not in valid_types:
        print('Bad Type')
        type_str = ', '.join(valid_types)
        return "Invalid type, must be one of the following: " + type_str
    if (len(search) < 3):
        return "Search string must be at least 3 characters long"
    return True

def basicSearch(type: str, search: str):
    s = LibgenSearch()
    type = type.lower()
    search = search.lower()
    if (type == 'author'):
        results = s.search_author(search)
    else:
        results = s.search_title(search)
    results = results[:10] # get first 10 elements
    return list(map(clearUneeded, results))

def getLinksFor(obj: dict):
    s = LibgenSearch()
    links = s.resolve_download_links(obj)
    return links

def clearUneeded(tuple):
    return {
        "id": tuple['ID'],
        "author": tuple['Author'],
        "title": tuple['Title'],
        "year": tuple['Year'],
        "size": tuple['Size'],
        "ext": tuple['Extension'],
        "Mirror_1": tuple['Mirror_1'],
    }

# Returns a list of strings
def formatResults(arr: list):
    sarr = []
    for i, t in enumerate(arr):
        msg = f"{str(i + 1)}. Author: {t['author']}, Title: {t['title']}, Ext: {t['ext']}"
        sarr.append(msg)
    return sarr

def formatLinks(obj: dict):
    arr = []
    for key in obj:
        arr.append(key + ': ' + obj[key])
    return arr