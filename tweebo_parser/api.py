'''
Module contains the following class:
'''

from typing import List, Dict, Union

import requests


class API(object):
    '''
    Allows easy connection and requests to the TweeboParse API server. \
    TweeboParse is a Twitter specific dependency parser.

    Attributes:

    1. hostname -- The IP address of the TweeboParser API server.
    2. port -- The Port that the TweeboParser API server is attached to.

    .. automethod:: __init__
    '''

    def __init__(self, hostname: str = '0.0.0.0',
                 port: int = 8000) -> None:
        '''
        :param hostname: The IP address of the TweeboParser API server.
        :param port: The Port that the TweeboParser API server is attached to.
        '''
        self.hostname = hostname
        self.port = port

    def parse_conll(self, texts: List[str]) -> List[str]:
        '''
        Processes the texts using TweeboParse and returns them in CoNLL format.

        :param texts: The List of Strings to be processed by TweeboParse.
        :return: A list of CoNLL formated strings.
        :raises ServerError: Caused when the server is not running.
        :raises HTTPError: Caused when the input texts is not formated \
        correctly e.g. When you give it a String not a list of Strings.

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
            return response.json()

    def parse_stanford(self, texts: List[str]
                       ) -> List[Dict[str, Union[str, int]]]:
        '''
        Processes the texts using TweeboParse and returns them in \
        a Stanford styled format (as in the same format as the json return \
        of the Stanford CoreNLP server dependency parser).

        :param texts: The List of Strings to be processed by TweeboParse.
        :return: A list of dicts.
        :raises ServerError: Caused when the server is not running.
        :raises HTTPError: Caused when the input texts is not formated \
        correctly e.g. When you give it a String not a list of Strings.

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
            return response.json()


class ServerError(Exception):
    '''
    Exception raised when the Server API is not avliable.

    Attributes:

    1. message -- Explains why it could not connect to the server, and \
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
