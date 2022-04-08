import json
import math
from bs4 import BeautifulSoup
from django.conf import settings
from scipy import spatial


class ResultDetails:
    def __init__(self, url=None, title=None, distance=None):
        self.url = url
        self.title = title
        self.distance = distance

    def to_json(self):
        return json.dumps(self.__dict__)


mock = [
    ResultDetails('https://vk.com', 'VK', 0.5),
    ResultDetails('https://youtube.com', 'Youtube', 0.4),
    ResultDetails('https://twitch.tv', 'Twitch', 0.3)
]


def get_all_words(path):
    all_words = list()
    with open(path, mode='r') as file:
        for line in file:
            word = line[:-1]
            all_words.append(word)
    return all_words


all_words = get_all_words(str(settings.BASE_DIR) + '/tokens.txt')


def get_query_vector(q: str):
    query_words = q.split(' ')
    vector = list()
    for word in all_words:
        if word in query_words:
            vector.append(get_tf_idf_for_word(word, query_words))
        else:
            vector.append(0)
    return vector


def get_distances_between_query_and_documents(query_vector):
    distances = list()
    for i, vector in enumerate(settings.VECTOR_SPACE):
        distance = spatial.distance.cosine(query_vector, vector)
        distance = distance or 1
        distances.append(distance)
    return distances


def get_url_and_title_of_page(i):
    with open(str(settings.BASE_DIR) + f'/pages/{i}.html', mode='r') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        title = soup.find('title').string

    with open(str(settings.BASE_DIR) + '/index.txt', mode='r') as file:
        for line in file:
            number, page_url = line.split(' - ')
            if int(number) == i:
                url = page_url
                break
    return url, title


def convert_distances_to_results(distances):
    results = list()
    for i, distance in enumerate(distances):
        url, title = get_url_and_title_of_page(i+1)
        results.append(ResultDetails(url=url, title=title, distance=distance))
    return sorted(results, key=lambda result: result.distance)[:20]


def get_search_results(q):
    vector = get_query_vector(q)
    distances = get_distances_between_query_and_documents(vector)
    results = convert_distances_to_results(distances)
    serialized_results = list()
    for res in results:
        serialized_results.append(res.to_json())
    return serialized_results


def get_tf_for_word(word, tokens):
    return tokens.count(word) / len(tokens)


def get_idf_for_word(word, tokens):
    index = settings.INVERTED_INDEX
    return math.log(100/len(index[word]))


def get_tf_idf_for_word(word, tokens):
    idf = get_idf_for_word(word, tokens)
    tf = get_tf_for_word(word, tokens)
    return tf * idf
