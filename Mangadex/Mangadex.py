import requests
import json

from Exceptions.FailedRequest import FailedRequest
from Manga.MangaEntry import MangaEntry

class MangadexScrapper:

    def __init__(self):
        ...

    def search(self, manga_name:str, response_limit:int = 10):

        # Build the API url and make the resquest
        search_url = f'https://api.mangadex.org/manga?title={manga_name}&limit={response_limit}'
        raw_response = requests.get(search_url)

        # Now check if the request was successful and parse the data
        self.__validate_response(raw_response)
        return self.__parse_data(raw_response)


    def get_chapters(self, manga_id: str, language: str = 'en') -> dict:
        base_url = f'https://api.mangadex.org/manga/{manga_id}/aggregate?translatedLanguage[]={language}'
        raw_response = requests.get(base_url)

        self.__validate_response(raw_response)
        return raw_response.json()['volumes']

    def get_chapter_pages(self, chapter_id: str) -> list:
        base_url = f'https://api.mangadex.org/chapter/{chapter_id}'
        chapters_urls = []


        # Make the get request and check the return status
        raw_response = requests.get(base_url)
        self.__validate_response(raw_response)

        # Now we can get the necessary information to format the URL for each page and add it to the list
        base_page_url = 'https://uploads.mangadex.org/data/{chapter_hash}/{chapter_url}'
        pages_data = raw_response.json()

        for image_file in pages_data['data']['attributes']['data']:
            chapters_urls.append(base_page_url.format(chapter_hash = pages_data['data']['attributes']['hash'], chapter_url = image_file))

        return chapters_urls


    def download(self, manga_id:str):
        ...

    def __parse_data(self, raw_data:requests.Response)-> list:
        # First we need to load the data as JSON and them only keep the title, id, tags and cover id
        raw_data = raw_data.json()

        manga_entry = []
        for series_data in raw_data['data']:
            manga_entry.append(MangaEntry(entry_data = series_data))

        return manga_entry

    def __validate_response(self, response:requests.Response) -> None :
        if response.status_code != 200 or response.json().get('result') == 'error':
            raise FailedRequest(response) 

# if __name__ == '__main__':
    # s = MangadexScrapper()
    # result = s.search('Quinte')
