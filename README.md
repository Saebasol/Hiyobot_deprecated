# Hiyobot

> Manga and doujinshi are shown at Discord

| Project name                                         | Badge                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Hiyobot](https://github.com/Saebasol/Hiyobot)       | [![Build Status](https://travis-ci.com/Saebasol/Hiyobot.svg?branch=master)](https://travis-ci.com/Saebasol/Hiyobot) [![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)                                                                                                                                                                                    |
| [Heliotrope](https://github.com/Saebasol/Heliotrope) | [![Build Status](https://travis-ci.com/Saebasol/Heliotrope.svg?token=tgm7xirkFfBB6hx7iLsr&branch=master)](https://travis-ci.com/Saebasol/Heliotrope) [![codecov](https://codecov.io/gh/Saebasol/Heliotrope/branch/master/graph/badge.svg?token=VTL1Z4abB7)](https://codecov.io/gh/Saebasol/Heliotrope) [![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black) |
| [Rose](https://github.com/Saebasol/Rose)             | [![Build Status](https://travis-ci.com/Saebasol/Rose.svg?branch=master)](https://travis-ci.com/Saebasol/Rose) [![codecov](https://codecov.io/gh/Saebasol/Rose/branch/master/graph/badge.svg)](https://codecov.io/gh/Saebasol/Rose) [![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)                                                                     |                                                                |

## About

Obtain information from the Heliotrope(private api server) and Hiyobi.me that mirrors Hitomi.la and show it in the Discord.

All images and DB are processed by Heliotrope.

Faster download and viewer functions can be provided through API.

### Heliotrope

Heliotrope is an api server using a sanic framework.

All work information or image information except search (scheduled to be implemented) is processed by the API.

All images are deleted every day.

## Development environment

* Windows 10 1904

* CPython 3.8.5
  
* git

* see requirements.txt

### Setup

| Environment variable | value                    |
| -------------------- | ------------------------ |
| heliotrope_auth      | Heliotrope Authorization |
| token                | Discord Bot token        |
| status_api_key       | statuspage apikey        |
| page_id              | statuspage page id       |
| metric_id            | statuspoge metric id     |

#### Windows

```powershell
git clone https://github.com/SaidBySolo/Hiyobot.git

cd Hiyobot

python -m Hiyobot
```

#### Linux

```bash
git clone https://github.com/SaidBySolo/Hiyobot.git

cd Hiyobot

python3 -m Hiyobot
```
