import re
import wikipedia
import duckduckgo


def wiki(term):
    try:
        result = wikipedia.summary(term, sentences=1)
        result = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", result)
        result = result.replace("(", "")
        result = result.replace(")", "")
    except Exception, e:
        print e
        result = 'null_result'

    return result


def ddg(term):
    print("ddg" + term)
    result = duckduckgo.Search(term)
    if result == term:
        return 'null_result'
    return result
