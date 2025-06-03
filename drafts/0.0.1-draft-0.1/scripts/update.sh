#!/bin/env sh

cd "$(dirname "$0")"

echo "Cleaning up documentation HTML..."
./tidy/tidy.sh
echo "(Re-) Creating UML diagram..."
./diagram/create_diagram.sh
echo "Validating SHACL shapefile..."
./validation/validate_shacl.sh
echo "Validating RDF+XML examples..."
./validation/validate_examples.sh
