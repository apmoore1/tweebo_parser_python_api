'''
Module contains the following class:
'''

from pathlib import Path
import json
import tempfile
from typing import List, Dict, Union

import requests


class API(object):
    '''
    Allows easy connection and requests to the TweeboParse API server. \
    TweeboParse is a Twitter specific dependency parser.

    Attributes:

    1. hostname -- The IP address of the TweeboParser API server.
    2. port -- The Port that the TweeboParser API server is attached to.
    3. retries -- Number of times to retry json decoding the returned data.
    4. log_errors -- Whether to log errors or not. If this is True it logs
       errors under `tweebo_log` file within your temp_dir
    .. automethod:: __init__
    '''

    def __init__(self, hostname: str = '0.0.0.0',
                 port: int = 8000, retries: int = 10,
                 log_errors: bool = False) -> None:
        '''
        :param hostname: The IP address of the TweeboParser API server.
        :param port: The Port that the TweeboParser API server is attached to.
        :param retries: Number of times to retry json decoding the
                        returned data.

        '''
        self.hostname = hostname
        self.port = port
        self.retries = retries
        self.log_errors = log_errors
        self._log_fp = Path(tempfile.gettempdir(), 'tweebo_log')
        # Delete the old file
        if self._log_fp.is_file():
            self._log_fp.open('w').close()

    def log_error(self, text: str) -> None:
        '''
        Given some error text it will log the text if self.log_errors is True

        :param text: Error text to log
        '''
        if self.log_errors:
            with self._log_fp.open('a+') as log_file:
                log_file.write(f'{text}\n')

    def parse_conll(self, texts: List[str], retry_count: int = 0) -> List[str]:
        '''
        Processes the texts using TweeboParse and returns them in CoNLL format.

        :param texts: The List of Strings to be processed by TweeboParse.
        :param retry_count: The number of times it has retried for. Default
                            0 does not require setting, main purpose is for
                            recursion.
        :return: A list of CoNLL formated strings.
        :raises ServerError: Caused when the server is not running.
        :raises :py:class:`requests.exceptions.HTTPError`: Caused when the
                input texts is not formated correctly e.g. When you give it a
                String not a list of Strings.
        :raises :py:class:`json.JSONDecodeError`: Caused if after self.retries
                attempts to parse the data it cannot decode the data.

        :Example:

        '''
        post_data = {'texts': texts, 'output_type': 'conll'}
        try:
            response = requests.post(f'http://{self.hostname}:{self.port}',
                                     json=post_data,
                                     headers={'Connection': 'close'})
            response.raise_for_status()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as server_error:
            raise ServerError(server_error, self.hostname, self.port)
        except requests.exceptions.HTTPError as http_error:
            raise http_error
        else:
            try:
                return response.json()
            except json.JSONDecodeError as json_exception:
                if retry_count == self.retries:
                    self.log_error(response.text)
                    raise Exception('Json Decoding error cannot parse this '
                                    f':\n{response.text}')
                return self.parse_conll(texts, retry_count + 1)

    def parse_stanford(self, texts: List[str], retry_count: int = 0
                       ) -> List[Dict[str, Union[str, int]]]:
        '''
        Processes the texts using TweeboParse and returns them in a Stanford
        styled format (as in the same format as the json return of the Stanford
        CoreNLP server dependency parser).

        :param texts: The List of Strings to be processed by TweeboParse.
        :param retry_count: The number of times it has retried for. Default
                            0 does not require setting, main purpose is for
                            recursion.
        :return: A list of dicts.
        :raises ServerError: Caused when the server is not running.
        :raises :py:class:`requests.exceptions.HTTPError`: Caused when the
                input texts is not formated correctly e.g. When you give it a
                String not a list of Strings.
        :raises :py:class:`json.JSONDecodeError`: Caused if after self.retries
                attempts to parse the data it cannot decode the data.

        :Example:
        ::
            from tweebo_parser import API
            tweebo_api = API()
            text_data = ['hello how are you', 'Where are we going']
            result = tweebo_api.parse_stanford(text_data)
            print(result)
            [{}]
        '''

        post_data = {'texts': texts, 'output_type': 'stanford'}
        try:
            response = requests.post(f'http://{self.hostname}:{self.port}',
                                     json=post_data,
                                     headers={'Connection': 'close'})
            response.raise_for_status()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.InvalidSchema) as server_error:
            raise ServerError(server_error, self.hostname, self.port)
        except requests.exceptions.HTTPError as http_error:
            raise http_error
        else:
            try:
                return response.json()
            except json.JSONDecodeError as json_exception:
                if retry_count == self.retries:
                    self.log_error(response.text)
                    raise Exception('Json Decoding error cannot parse this '
                                    f':\n{response.text}')
                return self.parse_stanford(texts, retry_count + 1)


class ServerError(Exception):
    '''
    Exception raised when the Server API is not avliable.

    Attributes:

    1. message -- Explains why it could not connect to the server, and
       details of the server it tried to connect to.

    .. automethod:: __init__
    '''

    def __init__(self, excpetion: requests.exceptions.RequestException,
                 hostname: str, port: int) -> None:
        '''
        :param exception: The requests exception instance that is raised.
        :param hostname: The IP address of the API server.
        :param port: The Port that the API server is attached to.
        '''

        message = f'Cannot connect to the server at {hostname}:{port}'
        if isinstance(excpetion, requests.exceptions.Timeout):
            message = 'Error caused by Time out. This is most likely due to '\
                      f'the server not running at: {hostname}:{port}'
        elif isinstance(excpetion, requests.exceptions.ConnectionError):
            message = 'Error caused by Connection Error. This is most likely '\
                      f'due to the server not running at {hostname}:{port}'
        self.message = message
