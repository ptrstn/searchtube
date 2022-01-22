[![Python Package](https://github.com/ptrstn/searchtube/actions/workflows/python-package.yml/badge.svg)](https://github.com/ptrstn/searchtube/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/ptrstn/searchtube/branch/master/graph/badge.svg)](https://codecov.io/gh/ptrstn/searchtube)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# searchtube

## Installation

```bash
pip install --user git+https://github.com/ptrstn/searchtube
```

## Usage

### Help

```bash
searchtube --help
```

```bash
usage: searchtube [-h] [--version] [--language LANGUAGE] [--limit LIMIT] query

YouTube search client

positional arguments:
  query                Search query

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  --language LANGUAGE  BCP-47 code to set the response language
  --limit LIMIT        Limit of the amount of videos in result
```

### Example

```bash
searchtube "Pontius Pilate" --limit 5 --language de
```

Output:

```bash
Initializing search for query 'Pontius Pilate'...
      video_id                                              title published_time duration         view_count                                  author                        channel_url
0  PLmMcLIzn4U  Who Was Pontius Pilate? | The Man Who Killed J...   vor 2 Jahren    47:05  1.667.489 Aufrufe  Timeline - World History Documentaries                 /c/TimelineChannel
1  fppoqtIu2ug  Why Did Pontius Pilate Allow The Killing Of Ch...  vor 9 Monaten    49:10    678.848 Aufrufe  Timeline - World History Documentaries                 /c/TimelineChannel
2  XyIwSiPIb9c  The Death of Pontius Pilate - Ancient Christia...     vor 1 Jahr     5:54      4.521 Aufrufe                       Theosis Christian  /channel/UCcCO7V2VRTjEfXv3VyifOgA
3  pXGsio9H1xs  The Last Temptation of Christ (1988) - Pontius...   vor 2 Jahren     3:44    228.233 Aufrufe                              Movieclips                      /c/MOVIECLIPS
4  n2UdpqsN2tw  Acta Pilate: Pilate's Report to Caesar of the ...   vor 7 Jahren    28:47    363.107 Aufrufe                          Lovin TheLight                   /c/LovinTheLight
```

## Development

```bash
git clone https://github.com/ptrstn/searchtube
cd searchtube
python -m venv venv
. venv/bin/activate
pip install -e .
pip install -r testing-requirements.txt
```

### Testing

```bash
pytest --cov
```
