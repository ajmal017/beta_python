#!/bin/bash
# For Production server we're going to run daily backups
# with this script with a cronjob

# dev database backup
# create .pgpass
echo "127.0.0.1:5432:betasmartz_dev:betasmartz_dev:${DEV_DB_PASS}" > .pgpass
docker cp .pgpass postgres:.pgpass
docker exec -it postgres bash
pg_dump -U betasmartz_dev -Fc betasmartz_dev -h 127.0.0.1 > betasmartz_dev_latest.dump
${DEV_DB_PASS}
exit
docker cp postgres:betasmartz_dev_latest.dump backups/betasmartz_dev_$(date +%s).dump


# restore betasmartz_dev with:
# pg_restore -U betasmartz_dev -h 127.0.0.1 --verbose --no-owner betasmartz_dev.dump