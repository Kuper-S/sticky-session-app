#!/bin/bash

# Number of instances for each service
NUM_WEB_INSTANCES=2

# Scale the web services
docker compose up --scale web1=$NUM_WEB_INSTANCES --scale web2=$NUM_WEB_INSTANCES -d

# Optional: Restart the nginx service to reconfigure with the new web instances
docker compose restart nginx