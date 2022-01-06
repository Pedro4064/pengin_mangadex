import requests

class MangaEntry:

    def __init__(self, entry_data):
        self.data = {}
        self.__populate_data(entry_data)

    def __populate_data(self, entry_data:dict):

        self.data['Id'] = entry_data['id']
        self.data['Title'] = entry_data['attributes']['title'].get('en') or list(entry_data['title'].values())[0]
        self.data['Description'] = self.__retrieve_description(entry_data['attributes'])
        self.data['Status'] = entry_data['attributes']['status']
        self.data['tags'] = self.__retrieve_tags(entry_data['attributes']['tags'])
        self.data['Cover URL'] = self.__retrieve_cover(entry_data['relationships'])

    def __retrieve_description(self, manga_atributes: dict) -> str:
        try:
            description = manga_atributes['description'].get('en') or list(manga_atributes['description'].values())[0]
            return description
        except:
            return '...'

    def __retrieve_tags(self, raw_tag_data:list)->list:
        tags = []
        
        for data in raw_tag_data:
            tags.append(data['attributes']['name']['en'])

        return tags

    def __retrieve_cover(self, relationships:list)->str:
        cover_id = ''
        
        for relation in relationships:
            if relation['type'] == 'cover_art':
                cover_id = relation['id']
                break

        cover_file = requests.get(f'https://api.mangadex.org/cover?ids[]={cover_id}').json()['data'][0]['attributes']['fileName']
        cover_url  = f"https://uploads.mangadex.org/covers/{self.data['Id']}/{cover_file}" 

        return cover_url
