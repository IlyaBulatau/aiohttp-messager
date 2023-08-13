#!/bin/bash
set -eo pipefail
shopt -s nullglob

# илья тут код который ты до запуска хочешь выполнить, по типу миграций дбшки там через алембик и тп

exec python -m src
