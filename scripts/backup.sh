#!/bin/bash
docker exec energystaff_postgres bash -c "pg_dump -U admin -h 127.0.0.1 db_energystaff > ./backup/dump_$(date +"%Y_%m_%d_%H_%M").sql"