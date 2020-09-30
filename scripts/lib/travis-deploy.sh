#!/usr/bin/env bash
set -e
ssh -o StrictHostKeyChecking=no -t $HOST_USER@$REMOTE_HOST "cd $DIR; $SCRIPT_PATH"