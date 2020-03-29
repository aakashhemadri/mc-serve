#!/usr/bin/env bash
source config.sh

docker-compose logs --follow ${INSTANCE}
