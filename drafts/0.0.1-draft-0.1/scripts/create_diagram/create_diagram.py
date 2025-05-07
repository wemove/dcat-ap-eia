#!/bin/env python3

import json
import os
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from model import requirements, UML_Class, UML_Property, UML_Relation, UML_Template
from rdflib import BNode, Graph, Literal, RDF, RDFS, SH, URIRef

# change working directory to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# this is hardcoded to obtain a nicer diagram
with open('orientations.json', 'r') as f:
    orientations = json.load(f)

def extract_cardinalities_from_shacl(shacl_path):
    def get_prefix_name(url):
        split_idx = url.rfind('#') if url.rfind('#') > url.rfind('/') else url.rfind('/')
        return f"{prefix_dict[url[:split_idx + 1]]}:{url[split_idx + 1:]}"
    
    def get_class_id_from_url(class_url):
        class_id = class_url
        for ns, prefix in prefix_dict.items():
            class_id = class_id.replace(ns, prefix)
        return class_id

    prefix_dict = {}

    g = Graph()
    g.parse(shacl_path, format='turtle')
    for prefix, namespace in g.namespaces():
        prefix_dict[str(namespace)] = prefix

    shapes = defaultdict(dict)  # (shape URI -> class data)

    class_ids = dict()
    for shape_name, _, class_url in g.triples((None, SH.targetClass, None)):
        class_ids[shape_name] = get_class_id_from_url(class_url)

    for shape_name, prop_pred, prop_constraint in g.triples((None, SH.property, None)):
        path_list = list(g.objects(prop_constraint, SH.path))
        class_id = class_ids[shape_name]
        if 'relations' not in shapes[class_id]:
            shapes[class_id]['relations'] = dict()
        if 'properties' not in shapes[class_id]:
            shapes[class_id]['properties'] = dict()
        if path_list:
            path = path_list[0]
            property_name = get_prefix_name(path)

            min_count_list = list(g.objects(prop_constraint, SH.minCount))
            max_count_list = list(g.objects(prop_constraint, SH.maxCount))
            class_constraint_list = list(g.objects(prop_constraint, SH['class']))

            cardinality = "*"
            if min_count_list and max_count_list:
                min_val = int(min_count_list[0])
                max_val = int(max_count_list[0])
                if min_val == 1 and max_val == 1:
                    cardinality = "1"
                elif min_val == 0 and max_val == 1:
                    cardinality = "0..1"
                elif min_val == 0 and not max_count_list:
                    cardinality = "*"
                else:
                    cardinality = f"{min_val}..{max_val}"
            elif min_count_list:
                min_val = int(min_count_list[0])
                cardinality = f"{min_val}..*"
            elif max_count_list:
                max_val = int(max_count_list[0])
                cardinality = f"0..{max_val}"

            if class_constraint_list:
                target_class = get_class_id_from_url(class_constraint_list[0])
                orientation = orientations[f'{class_id}-{target_class}-{property_name}']
                shapes[class_id]['relations'][property_name] = UML_Relation(class_id, target_class, UML_Property(property_name, cardinality, ''), orientation)
            else:
                shapes[class_id]['properties'][property_name] = cardinality
    return shapes


def extract_uml(uri: str):
    if uri.startswith('http'):
        response = requests.get(uri)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        with open(uri, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

    uml_classes = {}
    uml_relations = []
    cardinalities = extract_cardinalities_from_shacl('../../shacl/dcat-ap-eia_shacl-shapes.ttl')

    # extract classes
    for class_section in soup.find_all('section', id=lambda id: id and id.startswith('Class:')):
        class_name = class_section.select_one('th:nth-child(2)').text
        class_id = class_name.replace(':', '')
        requirement = requirements[class_section.select_one('tr:nth-child(1) td:nth-child(2)').text]
        uml_class = UML_Class(class_id, class_name, requirement, [])

        # extract properties
        relations = cardinalities[class_id]['relations']
        properties = class_section.select('section[id^="Property:"]')
        for property_section in properties:
            property_name = property_section.select_one('th:nth-child(2)').text
            requirement = requirements[property_section.select_one('tr:nth-child(1) td:nth-child(2)').text]
            if property_name in relations: # and (uml_classes[relations[property_name].target_id].properties) > 0:
                uml_relation = relations[property_name]
                uml_relation.property.requirement = requirement
                uml_relations.append(uml_relation)
            else:
                cardinality = cardinalities[class_id]['properties'][property_name]
                uml_property = UML_Property(property_name, cardinality, requirement)
                uml_class.add_property(uml_property)
        uml_classes[uml_class.id] = uml_class

    # transform relations into properties if target class is empty
    for uml_relation in uml_relations.copy():
        if uml_relation.target_id not in uml_classes:
            uml_relations.remove(uml_relation)
            uml_classes[uml_relation.source_id].add_property(uml_relation.property)

    # add "hidden" relations that affect the diagram without being displayed
    for relation, orientation in orientations.items():
        if '[hidden]' in orientation:
            source_id, target_id, *_ = relation.split('-')
            uml_relations.append(UML_Relation(source_id, target_id, None, orientation))

    return UML_Template(uml_classes.values(), uml_relations)


if __name__ == '__main__':
    plantuml = extract_uml('../../doc-eia.html')
    plantuml.write('./output/respec.puml') # debug output
    plantuml.render('../../DCAT-AP.EIA.jpg')
