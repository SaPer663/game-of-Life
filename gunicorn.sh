#!/usr/bin/env sh

set -o errexit
set -o nounset

/usr/local/bin/gunicorn main:app \
  --workers=4 `# Sync worker settings` \
  --max-requests=2000 \
  --max-requests-jitter=400 \
  --bind='0.0.0.0:5000' `# Run on 5000 port` \
  --chdir='/code/app'       `# Locations` \
  --worker-class=uvicorn.workers.UvicornWorker \
  --log-file=- \
  --access-logfile=- \
  --worker-tmp-dir='/dev/shm' \
  --timeout=3000
