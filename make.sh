#!/bin/bash
find "$CONDA_PREFIX"/lib/python*/site-packages/ \
     -maxdepth 2 -name direct_url.json \
     -exec rm -f {} +
yes y | docker system prune && python3 -m pip freeze > requirements.txt && cp requirements.txt ./コーヒー && docker-compose -p kouhii up --build