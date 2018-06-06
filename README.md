# Tweebo Parser Python API

This is a Python 3 API to the [TweeboParser](https://github.com/apmoore1/TweeboParser) using the TweeboParser API server which is servered using the Docker image which can be found [here](https://github.com/apmoore1/TweeboParserDocker).

## Installation and setup

1. Requires Python 3.6
2. `pip install tweebo-parser-python-api`
3. Install [docker](https://docs.docker.com/install/)
4. Start the TweeboParser API server running locally on port 8000: `docker run -p 8000:8000 -d --rm mooreap/tweeboparserdocker`

**NOTE** This will run the server using as many threads as you have CPU cores on your machine. If you would like to specify the number of threads use the `--threads` flag e.g.:

`docker run -p 8000:8000 -d --rm mooreap/tweeboparserdocker --threads 4`

Also to stop the docker server running:
1. Find the name assigned to the docker image using: `docker ps`
2. Then stop the relevant docker image: `docker stop name_of_image`

## Example

```
from tweebo_parser import API, ServerError
# Assumes server is running locally at 0.0.0.0:8000
tweebo_api = API()
text_data = ['Guangdong University of Foreign Studies is located in Guangzhou.',
             'Lucy is in the sky with diamonds.']
try:
    result_stanford = tweebo_api.parse_stanford(text_data)
    result_conll = tweebo_api.parse_conll(text_data)
except ServerError as e:
    print(f'{e}\n{e.message}')
```

For a more detailed example see the following [jupyter notebook](https://github.com/apmoore1/tweebo_parser_python_api/blob/master/notebooks/example.ipynb)
