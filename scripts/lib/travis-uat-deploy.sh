#!/usr/bin/env bash
set -e
ssh -o StrictHostKeyChecking=no -t $HOST_USER@$UAT_REMOTE_HOST "cd $DIR; $UAT_SCRIPT_PATH"
