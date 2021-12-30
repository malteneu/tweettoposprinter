import time
import urllib.parse
from typing import Optional, Dict, Any, List
from requests import Request, Session, Response



class TwitterClient:
    _ENDPOINT = 'https://api.twitter.com/2/'

    def __init__(self, bearer_token=None) -> None:
        self._session = Session()
        self._bearer_token = bearer_token
        self._create_header()
        self._users = []

    def _create_header(self):
        self._headers = {"Authorization": "Bearer {}".format(self._bearer_token)}

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, self._headers, **kwargs)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if 'errors' in data:
                raise Exception(data['errors'])
            return data['data']

    def _get_userid_by_username(self, username: str):
        for user in self._users:
            if username.upper() == str(user['username']).upper():
                return user

        result = self._get("users/by/username/" + username)
        self._users.append(result)
        return result

    def get_user_tweets(self, username: str):
        return self._get("users/" + self._get_userid_by_username(username)['id'] + "/tweets")