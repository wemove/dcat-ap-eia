#!/bin/env python3

import json
import os
import requests
import sys
from datetime import datetime

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# color codes
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
BOLD = "\033[1m"

VALIDATOR_SHAPEFILE_URL = 'https://www.itb.ec.europa.eu/shacl/shacl/api/validate'
VALIDATOR_RDF_URL = 'https://www.itb.ec.europa.eu/shacl/any/api/validate'


def validate(example_path: str, shacl_path: str):
    with open(shacl_path, 'r') as f:
        shacl = f.read()
    headers = {
        'accept': 'application/ld+json',
        'Content-Type': 'application/json'
    }
    if example_path is None:
        validator_url = VALIDATOR_SHAPEFILE_URL
        post_data = {
            "contentToValidate": shacl,
            "contentSyntax": "text/turtle",
            "validationType": "core"
        }
    else:
        with open(example_path, 'r') as f:
            example = f.read()
        validator_url = VALIDATOR_RDF_URL
        post_data = {
            "contentToValidate": example,
            "contentSyntax": "application/rdf+xml",
            "externalRules": [{
                "ruleSet": shacl,
                "embeddingMethod": "STRING",
                "ruleSyntax": "text/turtle"
            }]
        }

    response = requests.post(validator_url, headers=headers, data=json.dumps(post_data))
    # response.raise_for_status()
    report = response.json()
    if '@graph' in report:
        report = report['@graph']
    else:
        report = [report]

    report_filename = f'output/report_{datetime.now().isoformat()}.json'
    os.makedirs(os.path.dirname(report_filename), exist_ok=True)
    with open(report_filename, 'w') as f:
        json.dump(response.json(), f, indent=2)

    validated = is_valid(report)
    validation_path = example_path if example_path is not None else shacl_path
    validation_msg = f'{BOLD}{GREEN}valid{RESET}' if validated else f'{BOLD}{RED}invalid{RESET}'
    print(f'  Report result ({validation_path}): {validation_msg}')
    if not validated:
        print(f'    -- for more details, see {report_filename}')


def is_valid(report):
    for item in report:
        if item.get('@type') == 'sh:ValidationReport':
            # sh_conforms_dict = item.get('sh:conforms')
            if (sh_conforms_dict := item.get('sh:conforms')) and '@value' in sh_conforms_dict:
                return sh_conforms_dict['@value'].lower() == 'true'
    return False


if __name__ == '__main__':
    shacl_path = '../../shacl/dcat-ap-eia_shacl-shapes.ttl'
    examples_path = '../../examples/'
    mode = sys.argv[1] if len(sys.argv) > 1 else None

    if mode == 'shacl':
        # print(f'Validating {mode}...')
        report = validate(None, shacl_path)
    elif mode == 'examples':
        # print(f'Validating {mode}...')
        for example_path in os.listdir(examples_path):
            report = validate(examples_path + example_path, shacl_path)
    else:
        print('Usage: validate.py [shacl|examples]')
