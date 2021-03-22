from SPARQLWrapper import SPARQLWrapper, JSON
import en_core_web_md
import requests
import bs4
import wikipedia
import people_also_ask

en_model = en_core_web_md.load()


# POS identity
def find_entities(corpus):
    query_properties = []
    query_entities = []
    question_start = []
    parsed_sent = en_model(corpus)
    print(' '.join(['{}_{}'.format(tok, tok.tag_) for tok in parsed_sent]))
    for chunk in parsed_sent.ents:
        query_entities.append(chunk)
    for tok in parsed_sent:
        if tok.tag_ in ('NN', 'NNS', 'VB', 'JJ'):
            query_properties.append(tok)
        if tok.tag_ in ('WRB', 'WP', 'WP$'):
            question_start.append(tok)
        if len(query_entities) == 0:
            if tok.tag_ in ('NNP'):
                query_entities.append(tok)
    # print("name entities: ", query_entities)
    # print("query properties: ", query_properties)
    return query_entities, query_properties, question_start


def find_code(word, type_query='query_entity'):
    print("word in find code: ", word)
    code_result = []
    if type_query == 'query_property':
        url = 'https://www.wikidata.org/w/index.php?search=p:{}'.format(word)
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        links = []
        for i in soup.find_all("div", class_="mw-search-result-heading"):
            for link in i:
                if isinstance(link, bs4.element.NavigableString):
                    continue
                else:
                    links.append(link.get('href'))
        if len(links) == 0:
            return code_result
        code = links[0][links[0].find(':') + 1:]
        code_result.append(code)
    else:
        link = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&redirects=1' \
               '&format=json&titles={}'.format(word)
        page = requests.get(link)
        page = page.json()
        page_id = list(page['query']['pages'].keys())[0]
        code = page['query']['pages'][page_id]['pageprops']['wikibase_item']
        code_result.append(code)
    return code_result


def wiki_query(property_code, entity_code, mode=1):
    # we try to swap the entity and ?item variable to see if we can get the results due to the relationship between
    # them is complicated.
    if mode == 1:
        query = """
                            SELECT ?item ?itemLabel
                            WHERE {
                              wd:""" + entity_code + """ wdt:""" + property_code + """ ?item
                              SERVICE wikibase:label { bd:serviceParam wikibase:language "en".}
                            }
                            """
        print("wikidata query: ", query)
    else:
        query = """
                    SELECT ?item ?itemLabel
                    WHERE {
                      ?item wdt:""" + property_code + """ wd:""" + entity_code + """
                      SERVICE wikibase:label { bd:serviceParam wikibase:language "en".}
                    }
                    """
        print("wikidata query: ", query)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = sparql.query().convert()
    results = []
    for result in response['results']['bindings']:
        results.append(result['itemLabel']['value'])
    return results


def wikipedia_query(query_entity):
    result = [wikipedia.summary(query_entity[0].text).split('\n')[0]]
    return result


# add the property and noun in the query
def wiki_data(query_entity, query_property):
    # query using dbpedia
    print(query_entity)
    print(query_property)
    results = []
    if len(query_property) == 0 and len(query_entity) == 0:
        return results
    elif len(query_property) == 0:
        results = wikipedia_query(query_entity)
    elif len(query_entity) == 0:
        results = wikipedia_query(query_property)
    elif (len(query_property) != 0) and (len(query_entity) != 0):
        # query using wikidata
        # find the property code
        property_word = query_property[0].text
        property_code = find_code(property_word, 'query_property')
        # find the entity code
        entity_word = query_entity[0].text
        entity_code = find_code(entity_word, 'query_entity')
        if len(entity_code) > 0 and len(property_code) > 0:
            results = wiki_query(property_code[0], entity_code[0])
            # print(len(results['results']['bindings']))
            # if len(results['results']['bindings']) == 0:
            if len(results) == 0:
                results = wiki_query(property_code[0], entity_code[0], mode='reverse')

    return results


def google_answer(corpus):
    result = []
    response = people_also_ask.get_answer(corpus)
    print("response: ", response)
    if response['has_answer']:
        if len(response['response']) == 0 and len(response['related_questions']) > 0:
            answer = get_related_question_google(response)
            result.append(answer)
        if response['displayed_link'] is not None and len(response['related_questions']) > 0:
            if "youtube.com" in response['displayed_link']:
                print('here 1')
                answer = get_related_question_google(response)
            else:
                print('here 2')
                answer = response['response']
            result.append(answer)
        else:
            print('here 3')
            answer = response['response']
            if 'Wikipedia' in answer:
                print('here 4')
                result.append(answer[:(answer.find('Wikipedia'))])
            else:
                result.append(answer)
    if not response['has_answer'] and len(response['related_questions']) > 0:
        answer = get_related_question_google(response)
        result.append(answer)
    # To avoid the None answer from the get_related_question_google function:
    if None in result:
        result = []
    return result


def get_related_question_google(response):
    related_question = response['related_questions'][0]
    related_response = people_also_ask.get_answer(related_question)
    print("related response: ", related_response)
    if 'response' in related_response:
        answer = related_response['response']
        return answer
    else:
        return


def wiki_bot(corpus):
    answer = google_answer(corpus)
    print("answer google is: ", answer)
    if len(answer) == 0:
        query_entity, query_property, question_start = find_entities(corpus)
        print(question_start)
        answer = wiki_data(query_entity, query_property)
    answer_json = {'answer': answer}
    return answer_json


if __name__ == '__main__':
    answer = wiki_bot("what is the fastest animal?")
    print(answer)
