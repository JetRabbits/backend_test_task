#!/usr/bin/env bash
export $(cat .env | xargs)
docker exec -it local-storage-db psql -d ${POSTGRES_DB} -U ${POSTGRES_USER}