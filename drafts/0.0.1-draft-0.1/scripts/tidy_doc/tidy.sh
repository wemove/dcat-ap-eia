#!/bin/env sh

if ! command -v "tidy" >/dev/null 2>&1; then
  echo "Error: 'tidy' could not be found. Please install it and run this script again."
  exit 1
fi

tidy -config tidy.config -m ../../doc-eia.html
