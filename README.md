# Hiyobot

> Manga and doujinshi are shown at Discord

| Project name | Badge                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Heliotrope   | [![Build Status](https://travis-ci.com/SaidBySolo/Heliotrope.svg?token=tgm7xirkFfBB6hx7iLsr&branch=master)](https://travis-ci.com/SaidBySolo/Heliotrope) [![codecov](https://codecov.io/gh/SaidBySolo/Heliotrope/branch/master/graph/badge.svg?token=VTL1Z4abB7)](https://codecov.io/gh/SaidBySolo/Heliotrope) [![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black) |
| Rose         | [![Build Status](https://travis-ci.com/SaidBySolo/Rose.svg?branch=master)](https://travis-ci.com/SaidBySolo/Rose) [![codecov](https://codecov.io/gh/SaidBySolo/Rose/branch/master/graph/badge.svg)](https://codecov.io/gh/SaidBySolo/Rose) [![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)                                                                     |

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
| sentry               | Sentry DSN               |
| heliotrope_auth      | Heliotrope Authorization |
| token                | Discord Bot token        |

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
