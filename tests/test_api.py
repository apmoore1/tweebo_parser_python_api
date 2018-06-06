import copy
import multiprocessing
from typing import Any

import pytest
import requests

from tweebo_parser import API


TEST_SENTENCES_0 = ["I predict I won't win a single game I bet on. "
                    "Got Cliff Lee today, so if he loses its on me RT "
                    "@e_one: Texas (cont) http://tl.gd/6meogh",
                    "Wednesday 27th october 2010. 》have a nice day :)",
                    "RT @DjBlack_Pearl: wat muhfuckaz wearin 4 the lingerie "
                    "party?????"]
TEST_SENTENCES_1 = ["I predict I won't win a single game I bet on. "
                    "Got Cliff Lee today, so if he loses its on me RT "
                    "@e_one: Texas (cont) http://tl.gd/6meogh",
                    "              ",
                    "Wednesday 27th october 2010. 》have a nice day :)",
                    "RT @DjBlack_Pearl: wat muhfuckaz wearin 4 the lingerie "
                    "party?????",
                    ""]
TOKENS_0 = [{'index': 1, 'word': 'I', 'originalText': 'I', 'pos': 'O'},
            {'index': 2, 'word': 'predict', 'originalText': 'predict',
             'pos': 'V'},
            {'index': 3, 'word': 'I', 'originalText': 'I', 'pos': 'O'},
            {'index': 4, 'word': "won't", 'originalText': "won't",
             'pos': 'V'},
            {'index': 5, 'word': 'win', 'originalText': 'win',
             'pos': 'V'},
            {'index': 6, 'word': 'a', 'originalText': 'a', 'pos': 'D'},
            {'index': 7, 'word': 'single', 'originalText': 'single',
             'pos': 'A'},
            {'index': 8, 'word': 'game', 'originalText': 'game',
             'pos': 'N'},
            {'index': 9, 'word': 'I', 'originalText': 'I', 'pos': 'O'},
            {'index': 10, 'word': 'bet', 'originalText': 'bet',
             'pos': 'V'},
            {'index': 11, 'word': 'on', 'originalText': 'on',
             'pos': 'P'},
            {'index': 12, 'word': '.', 'originalText': '.', 'pos': ','},
            {'index': 13, 'word': 'Got', 'originalText': 'Got',
             'pos': 'V'},
            {'index': 14, 'word': 'Cliff', 'originalText': 'Cliff',
             'pos': '^'},
            {'index': 15, 'word': 'Lee', 'originalText': 'Lee',
             'pos': '^'},
            {'index': 16, 'word': 'today', 'originalText': 'today',
             'pos': 'N'},
            {'index': 17, 'word': ',', 'originalText': ',', 'pos': ','},
            {'index': 18, 'word': 'so', 'originalText': 'so',
             'pos': 'P'},
            {'index': 19, 'word': 'if', 'originalText': 'if',
             'pos': 'P'},
            {'index': 20, 'word': 'he', 'originalText': 'he',
             'pos': 'O'},
            {'index': 21, 'word': 'loses', 'originalText': 'loses',
             'pos': 'V'},
            {'index': 22, 'word': 'its', 'originalText': 'its',
             'pos': 'L'},
            {'index': 23, 'word': 'on', 'originalText': 'on',
             'pos': 'P'},
            {'index': 24, 'word': 'me', 'originalText': 'me',
             'pos': 'O'},
            {'index': 25, 'word': 'RT', 'originalText': 'RT',
             'pos': '~'},
            {'index': 26, 'word': '@e_one', 'originalText': '@e_one',
             'pos': '@'},
            {'index': 27, 'word': ':', 'originalText': ':', 'pos': '~'},
            {'index': 28, 'word': 'Texas', 'originalText': 'Texas',
             'pos': '^'},
            {'index': 29, 'word': '(', 'originalText': '(', 'pos': ','},
            {'index': 30, 'word': 'cont', 'originalText': 'cont',
             'pos': '~'},
            {'index': 31, 'word': ')', 'originalText': ')', 'pos': ','},
            {'index': 32, 'word': 'http://tl.gd/6meogh',
             'originalText': 'http://tl.gd/6meogh', 'pos': 'U'}]
TOKENS_1 = [{'index': 1, 'word': 'Wednesday',
             'originalText': 'Wednesday', 'pos': '^'},
            {'index': 2, 'word': '27th', 'originalText': '27th',
             'pos': 'A'},
            {'index': 3, 'word': 'october', 'originalText': 'october',
             'pos': '^'},
            {'index': 4, 'word': '2010', 'originalText': '2010',
             'pos': '$'},
            {'index': 5, 'word': '.', 'originalText': '.', 'pos': ','},
            {'index': 6, 'word': '》have', 'originalText': '》have',
             'pos': 'V'},
            {'index': 7, 'word': 'a', 'originalText': 'a', 'pos': 'D'},
            {'index': 8, 'word': 'nice', 'originalText': 'nice',
             'pos': 'A'},
            {'index': 9, 'word': 'day', 'originalText': 'day',
             'pos': 'N'},
            {'index': 10, 'word': ':)', 'originalText': ':)',
             'pos': 'E'}]
TOKENS_2 = [{'index': 1, 'word': 'RT',
             'originalText': 'RT', 'pos': '~'},
            {'index': 2, 'word': '@DjBlack_Pearl',
             'originalText': '@DjBlack_Pearl', 'pos': '@'},
            {'index': 3, 'word': ':', 'originalText': ':', 'pos': '~'},
            {'index': 4, 'word': 'wat', 'originalText': 'wat',
             'pos': 'O'},
            {'index': 5, 'word': 'muhfuckaz',
             'originalText': 'muhfuckaz', 'pos': 'N'},
            {'index': 6, 'word': 'wearin', 'originalText': 'wearin',
             'pos': 'V'},
            {'index': 7, 'word': '4', 'originalText': '4', 'pos': 'P'},
            {'index': 8, 'word': 'the', 'originalText': 'the',
             'pos': 'D'},
            {'index': 9, 'word': 'lingerie', 'originalText': 'lingerie',
             'pos': 'N'},
            {'index': 10, 'word': 'party', 'originalText': 'party',
             'pos': 'N'},
            {'index': 11, 'word': '?????', 'originalText': '?????',
             'pos': ','}]
B_DEP_0 = [{'dep': '_', 'governor': 2, 'governorGloss': 'predict',
            'dependent': 1, 'dependentGloss': 'I'},
           {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
            'dependent': 2, 'dependentGloss': 'predict'},
           {'dep': '_', 'governor': 4, 'governorGloss': "won't",
            'dependent': 3, 'dependentGloss': 'I'},
           {'dep': '_', 'governor': 2, 'governorGloss': 'predict',
            'dependent': 4, 'dependentGloss': "won't"},
           {'dep': '_', 'governor': 4, 'governorGloss': "won't",
            'dependent': 5, 'dependentGloss': 'win'},
           {'dep': '_', 'governor': 8, 'governorGloss': "game",
            'dependent': 6, 'dependentGloss': 'a'},
           {'dep': '_', 'governor': 8, 'governorGloss': "game",
            'dependent': 7, 'dependentGloss': 'single'},
           {'dep': '_', 'governor': 5, 'governorGloss': "win",
            'dependent': 8, 'dependentGloss': 'game'},
           {'dep': '_', 'governor': 10, 'governorGloss': "bet",
            'dependent': 9, 'dependentGloss': 'I'},
           {'dep': '_', 'governor': 8, 'governorGloss': "game",
            'dependent': 10, 'dependentGloss': 'bet'},
           {'dep': 'MWE', 'governor': 10, 'governorGloss': "bet",
            'dependent': 11, 'dependentGloss': 'on'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 12, 'dependentGloss': '.'},
           {'dep': 'ROOT', 'governor': 0, 'governorGloss': "ROOT",
            'dependent': 13, 'dependentGloss': 'Got'},
           {'dep': 'MWE', 'governor': 15, 'governorGloss': "Lee",
            'dependent': 14, 'dependentGloss': 'Cliff'},
           {'dep': '_', 'governor': 13, 'governorGloss': "Got",
            'dependent': 15, 'dependentGloss': 'Lee'},
           {'dep': '_', 'governor': 13, 'governorGloss': "Got",
            'dependent': 16, 'dependentGloss': 'today'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 17, 'dependentGloss': ','},
           {'dep': 'ROOT', 'governor': 0, 'governorGloss': "ROOT",
            'dependent': 18, 'dependentGloss': 'so'},
           {'dep': '_', 'governor': 22, 'governorGloss': "its",
            'dependent': 19, 'dependentGloss': 'if'},
           {'dep': '_', 'governor': 21, 'governorGloss': "loses",
            'dependent': 20, 'dependentGloss': 'he'},
           {'dep': '_', 'governor': 19, 'governorGloss': "if",
            'dependent': 21, 'dependentGloss': 'loses'},
           {'dep': '_', 'governor': 18, 'governorGloss': "so",
            'dependent': 22, 'dependentGloss': 'its'},
           {'dep': '_', 'governor': 22, 'governorGloss': "its",
            'dependent': 23, 'dependentGloss': 'on'},
           {'dep': '_', 'governor': 23, 'governorGloss': "on",
            'dependent': 24, 'dependentGloss': 'me'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 25, 'dependentGloss': 'RT'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 26, 'dependentGloss': '@e_one'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 27, 'dependentGloss': ':'},
           {'dep': '_', 'governor': 21, 'governorGloss': "loses",
            'dependent': 28, 'dependentGloss': 'Texas'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 29, 'dependentGloss': '('},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 30, 'dependentGloss': 'cont'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 31, 'dependentGloss': ')'},
           {'dep': '_', 'governor': -1, 'governorGloss': "$$NAN$$",
            'dependent': 32, 'dependentGloss': 'http://tl.gd/6meogh'}]
B_DEP_1 = [{'dep': 'MWE', 'governor': 2, 'governorGloss': '27th',
            'dependent': 1, 'dependentGloss': 'Wednesday'},
           {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
            'dependent': 2, 'dependentGloss': '27th'},
           {'dep': 'MWE', 'governor': 1, 'governorGloss': 'Wednesday',
            'dependent': 3, 'dependentGloss': 'october'},
           {'dep': 'MWE', 'governor': 3, 'governorGloss': 'october',
            'dependent': 4, 'dependentGloss': '2010'},
           {'dep': '_', 'governor': -1, 'governorGloss': '$$NAN$$',
            'dependent': 5, 'dependentGloss': '.'},
           {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
            'dependent': 6, 'dependentGloss': '》have'},
           {'dep': '_', 'governor': 9, 'governorGloss': 'day',
            'dependent': 7, 'dependentGloss': 'a'},
           {'dep': '_', 'governor': 9, 'governorGloss': 'day',
            'dependent': 8, 'dependentGloss': 'nice'},
           {'dep': '_', 'governor': 6, 'governorGloss': '》have',
            'dependent': 9, 'dependentGloss': 'day'},
           {'dep': '_', 'governor': -1, 'governorGloss': '$$NAN$$',
            'dependent': 10, 'dependentGloss': ':)'}]
B_DEP_2 = [{'dep': '_', 'governor': -1, 'governorGloss': '$$NAN$$',
            'dependent': 1, 'dependentGloss': 'RT'},
           {'dep': '_', 'governor': -1, 'governorGloss': '$$NAN$$',
            'dependent': 2, 'dependentGloss': '@DjBlack_Pearl'},
           {'dep': '_', 'governor': -1, 'governorGloss': '$$NAN$$',
            'dependent': 3, 'dependentGloss': ':'},
           {'dep': 'ROOT', 'governor': 0, 'governorGloss': 'ROOT',
            'dependent': 4, 'dependentGloss': 'wat'},
           {'dep': '_', 'governor': 6, 'governorGloss': 'wearin',
            'dependent': 5, 'dependentGloss': 'muhfuckaz'},
           {'dep': '_', 'governor': 4, 'governorGloss': 'wat',
            'dependent': 6, 'dependentGloss': 'wearin'},
           {'dep': '_', 'governor': 6, 'governorGloss': 'wearin',
            'dependent': 7, 'dependentGloss': '4'},
           {'dep': '_', 'governor': 10, 'governorGloss': 'party',
            'dependent': 8, 'dependentGloss': 'the'},
           {'dep': '_', 'governor': 10, 'governorGloss': 'party',
            'dependent': 9, 'dependentGloss': 'lingerie'},
           {'dep': '_', 'governor': 7, 'governorGloss': '4',
            'dependent': 10, 'dependentGloss': 'party'},
           {'dep': '_', 'governor': -1, 'governorGloss': '$$NAN$$',
            'dependent': 11, 'dependentGloss': '?????'}]
CONLL_0 = ('1\tI\t_\tO\tO\t_\t2\t_\n'
           '2\tpredict\t_\tV\tV\t_\t0\t_\n'
           '3\tI\t_\tO\tO\t_\t4\t_\n'
           "4\twon't\t_\tV\tV\t_\t2\t_\n"
           '5\twin\t_\tV\tV\t_\t4\t_\n'
           '6\ta\t_\tD\tD\t_\t8\t_\n'
           '7\tsingle\t_\tA\tA\t_\t8\t_\n'
           '8\tgame\t_\tN\tN\t_\t5\t_\n'
           '9\tI\t_\tO\tO\t_\t10\t_\n'
           '10\tbet\t_\tV\tV\t_\t8\t_\n'
           '11\ton\t_\tP\tP\t_\t10\tMWE\n'
           '12\t.\t_\t,\t,\t_\t-1\t_\n'
           '13\tGot\t_\tV\tV\t_\t0\t_\n'
           '14\tCliff\t_\t^\t^\t_\t15\tMWE\n'
           '15\tLee\t_\t^\t^\t_\t13\t_\n'
           '16\ttoday\t_\tN\tN\t_\t13\t_\n'
           '17\t,\t_\t,\t,\t_\t-1\t_\n'
           '18\tso\t_\tP\tP\t_\t0\t_\n'
           '19\tif\t_\tP\tP\t_\t22\t_\n'
           '20\the\t_\tO\tO\t_\t21\t_\n'
           '21\tloses\t_\tV\tV\t_\t19\t_\n'
           '22\tits\t_\tL\tL\t_\t18\t_\n'
           '23\ton\t_\tP\tP\t_\t22\t_\n'
           '24\tme\t_\tO\tO\t_\t23\t_\n'
           '25\tRT\t_\t~\t~\t_\t-1\t_\n'
           '26\t@e_one\t_\t@\t@\t_\t-1\t_\n'
           '27\t:\t_\t~\t~\t_\t-1\t_\n'
           '28\tTexas\t_\t^\t^\t_\t21\t_\n'
           '29\t(\t_\t,\t,\t_\t-1\t_\n'
           '30\tcont\t_\t~\t~\t_\t-1\t_\n'
           '31\t)\t_\t,\t,\t_\t-1\t_\n'
           '32\thttp://tl.gd/6meogh\t_\tU\tU\t_\t-1\t_')
CONLL_1 = ('1\tWednesday\t_\t^\t^\t_\t2\tMWE\n'
           '2\t27th\t_\tA\tA\t_\t0\t_\n'
           '3\toctober\t_\t^\t^\t_\t1\tMWE\n'
           "4\t2010\t_\t$\t$\t_\t3\tMWE\n"
           '5\t.\t_\t,\t,\t_\t-1\t_\n'
           '6\t》have\t_\tV\tV\t_\t0\t_\n'
           '7\ta\t_\tD\tD\t_\t9\t_\n'
           '8\tnice\t_\tA\tA\t_\t9\t_\n'
           '9\tday\t_\tN\tN\t_\t6\t_\n'
           '10\t:)\t_\tE\tE\t_\t-1\t_')
CONLL_2 = ('1\tRT\t_\t~\t~\t_\t-1\t_\n'
           '2\t@DjBlack_Pearl\t_\t@\t@\t_\t-1\t_\n'
           '3\t:\t_\t~\t~\t_\t-1\t_\n'
           "4\twat\t_\tO\tO\t_\t0\t_\n"
           '5\tmuhfuckaz\t_\tN\tN\t_\t6\t_\n'
           '6\twearin\t_\tV\tV\t_\t4\t_\n'
           '7\t4\t_\tP\tP\t_\t6\t_\n'
           '8\tthe\t_\tD\tD\t_\t10\t_\n'
           '9\tlingerie\t_\tN\tN\t_\t10\t_\n'
           '10\tparty\t_\tN\tN\t_\t7\t_\n'
           '11\t?????\t_\t,\t,\t_\t-1\t_')


def test_api_conll():
    '''
    Tests :py:func:`tweebo_parser.API.parse_conll` where the output type is \
    conll. We perform the following tests:
    1. 3 different sentences (one of the sentences contains a UTF specific \
    character)
    2. 5 sentences that include empty sentences.
    3. Empty list
    '''

    tweebo_api = API()
    expected_return = [CONLL_0, CONLL_1, CONLL_2]
    assert expected_return == tweebo_api.parse_conll(TEST_SENTENCES_0)

    expected_return = [CONLL_0, '', CONLL_1, CONLL_2, '']
    assert expected_return == tweebo_api.parse_conll(TEST_SENTENCES_1)

    assert tweebo_api.parse_conll([]) == []


def test_api_stanford():
    '''
    Tests :py:func:`tweebo_parser.API.parse_stanford` where the output type \
    is stanford styled. We perform the following tests:
    1. 3 different sentences (one of the sentences contains a UTF character)
    2. 5 sentences that include empty sentences.
    3. Empty list
    '''

    tweebo_api = API()
    stanford_0 = {'index': 0, 'tokens': TOKENS_0, 'basicDependencies': B_DEP_0}
    stanford_1 = {'index': 1, 'tokens': TOKENS_1, 'basicDependencies': B_DEP_1}
    stanford_2 = {'index': 2, 'tokens': TOKENS_2, 'basicDependencies': B_DEP_2}
    expected_return = [stanford_0, stanford_1, stanford_2]
    assert expected_return == tweebo_api.parse_stanford(TEST_SENTENCES_0)

    empty = {'index': 1, 'tokens': [], 'basicDependencies': []}
    last_empty = copy.deepcopy(empty)
    last_empty['index'] = 4
    stanford_1['index'] = 2
    stanford_2['index'] = 3
    expected_return = [stanford_0, empty, stanford_1, stanford_2, last_empty]
    assert expected_return == tweebo_api.parse_stanford(TEST_SENTENCES_1)

    assert tweebo_api.parse_stanford([]) == []


def test_multi_processing():
    '''
    Test that the API can handle lots of simultaneous requests.
    '''

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        tasks = []
        for _ in range(10):
            tasks.append(pool.apply_async(test_api_conll))
            tasks.append(pool.apply_async(test_api_stanford))
        for task in tasks:
            task.get()


def test_api_exceptions():

    def cause_error(data: Any, exception: Any, api: API):
        functions = ['parse_conll', 'parse_stanford']
        for function in functions:
            with pytest.raises(exception):
                getattr(api, function)(data)
    tweebo_api = API()
    cause_error([1], requests.exceptions.HTTPError, tweebo_api)
    cause_error('hello how are you', requests.exceptions.HTTPError, tweebo_api)
