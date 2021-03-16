import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import json

endpoint_url = "https://query.wikidata.org/sparql"

all_cats_query = """
SELECT ?cl ?clLabel ?c
WITH { SELECT ?cl (COUNT(*) AS ?c)
WHERE {
?i wdt:P31 ?cl
}
GROUP BY ?cl
} AS %classes
WHERE {
INCLUDE %classes
FILTER(?c >= 5 && ?c <= 200)
SERVICE wikibase:label { bd:serviceParam wikibase:language "en"}
} ORDER BY ?c
"""


def aliases_query(category):
    query = """
SELECT ?i ?iLabel ?iAltLabel
WHERE {
?i wdt:P31 wd:"""+category+"""
SERVICE wikibase:label { bd:serviceParam wikibase:language "en"}
}
"""
    return query


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0],
                                                sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    # Try to return JSON if doesn't work return None
    try:
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()
    except:
        return None


def make_cat_list(query):
    categories = []
    results_dict = get_results(endpoint_url, query)
    for result in results_dict['results']['bindings']:
        categories.append(result['cl']['value'][31:])
    return categories


def make_vocab_dicts(categories):
    vocab_dicts = []
    failed_cats = []
    # loop through categories
    for c in categories:
        results_dict = get_results(endpoint_url, aliases_query(c))
        # only work with categories that returned valid JSON
        if results_dict is not None:
            for result in results_dict['results']['bindings']:
                word_dict = {}
                key = result['iLabel']['value']
                # check if synonyms list is non-empty
                if 'iAltLabel' in result:
                    values = [i.strip() for i in
                              result['iAltLabel']['value'].split(',')]
                # if no synonyms exist, add empty list as value
                else:
                    values = ['']
                word_dict.update({key: values})
                vocab_dicts.append(word_dict)
        # keep track of how many/which categories
        # didn't return valid JSON
        else:
            failed_cats.append(c)
    print("failed_cats=", failed_cats)
    print("len(failed_cats)=", len(failed_cats))
    return vocab_dicts


def write_vocab_file(vocab_dicts):
    with open('vocab_capitals.jsonl', 'w') as outfile:
        for d in vocab_dicts:
            json.dump(d, outfile)
            outfile.write('\n')

# steps for all cats

# categories = make_cat_list(all_cats_query)
# vocab_dicts = make_vocab_dicts(categories)
# write_vocab_file(vocab_dicts)


# steps for single cat
# capital = 'Q5119'
# vocab_dicts = make_vocab_dicts([capital])
# write_vocab_file(vocab_dicts)
