import requests
from io import StringIO
import json, re

def isNum(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

def search_anilist(search, max_results=10):
    query = """
    query ($id: Int, $page: Int, $search: String, $type: MediaType) {
        Page (page: $page, perPage: 10) {
            media (id: $id, search: $search, type: $type) {
                id
                idMal
                description(asHtml: false)
                title {
                    english
                    romaji
                }
                coverImage {
                    extraLarge
                }
                bannerImage
                averageScore
                meanScore
                status
                genres
                episodes
                externalLinks {
                    url
                    site
                }
                nextAiringEpisode {
                    timeUntilAiring
                }
            }
        }
    }
    """
    id_query = '''
                query ($id: Int) {
                    Media (id: $id, type: ANIME) {
                        id
                        idMal
                        description(asHtml: false)
                        title {
                            english
                            romaji
                        }
                        coverImage {
                            extraLarge
                        }
                        bannerImage
                        averageScore
                        meanScore
                        status
                        genres
                        episodes
                        externalLinks {
                            url
                            site
                        }
                        nextAiringEpisode {
                            timeUntilAiring
                        }
                    }
                }
                '''
    variables = {
        'search': search,
        'page': 1,
        'perPage': max_results,
        'type': 'ANIME',
        'sort': 'SEARCH_MATCH'
    }
    url = 'https://graphql.anilist.co'
    if not isNum(search):
        response = requests.post(url, json={'query': query, 'variables': variables}).json()
        results = response['data']['Page']['media']

        results = response['data']['Page']['media']
        datas = []
        for result in results:
            title = result['title']['english'] if bool(result['title']['english']) else result['title']['romaji']
            res = {
                'desc': re.sub(r"\<(.*?)\>", '', result['description']) if type(result['description']) == str else None,
                'title': title,
                'link': 'https://anilist.co/anime/{}'.format(result['id']),
                'img': result['coverImage']['extraLarge'],
                'status': result['status'],
                'genres': result['genres'],
                'totalEpisodes': result['episodes'],
                'id': result['id']
                }
            datas.append(res)
        return datas
    else:
        variables = {
            'id': search
        }
        response = requests.post(url, json={'query': id_query, 'variables': variables}).json()
        result = response['data']['Media']
        title = result['title']['english'] if bool(result['title']['english']) else result['title']['romaji']
        res = {
            'desc': re.sub(r"\<(.*?)\>", '', result['description']) if type(result['description']) == str else None,
            'title': title,
            'link': 'https://anilist.co/anime/{}'.format(result['id']),
            'img': result['coverImage']['extraLarge'],
            'status': result['status'],
            'genres': result['genres'],
            'totalEpisodes': result['episodes'],
            'id': result['id']
        }
        return [res]
