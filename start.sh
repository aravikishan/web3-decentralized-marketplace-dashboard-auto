#!/bin/bash
set -e
echo "Starting Web3 Decentralized Marketplace Dashboard..."
uvicorn app:app --host 0.0.0.0 --port 9074 --workers 1
