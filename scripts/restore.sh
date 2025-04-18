#!/bin/bash
docker exec -i energystaff_postgres sh -c "psql --username admin --dbname db_energystaff -c \"DROP SCHEMA public CASCADE; CREATE SCHEMA public;\""
docker exec -i energystaff_postgres sh -c "psql --username admin --dbname db_energystaff -f /backup/dump_2025_04_18_11_48.sql"