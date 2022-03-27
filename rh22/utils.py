import requests

from bs4 import BeautifulSoup

MY_ANIME_LIST_URL_FMT = 'https://myanimelist.net/anime/{}'


class MissingEmbeddedVideoException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_embedded_video_url(anime_id: int) -> str:
    try:
        html = requests.get(MY_ANIME_LIST_URL_FMT.format(anime_id)).content
        soup = BeautifulSoup(html, 'html.parser')
        element = soup.find(
            'a', class_='iframe js-fancybox-video video-unit promotion', href=True)
        if element is None:
            raise MissingEmbeddedVideoException(
                f'{anime_id} does not have an embedded video on myanimelist.net.')
        return element.attrs['href']
    except MissingEmbeddedVideoException:
        raise
    except:
        raise ValueError(f'{anime_id} was not found in myanimelist.net.')
