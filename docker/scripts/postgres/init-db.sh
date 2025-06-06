#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname $POSTGRES_DB <<-EOSQL
  CREATE TABLE training (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    code UUID UNIQUE NOT NULL
  )
EOSQL

