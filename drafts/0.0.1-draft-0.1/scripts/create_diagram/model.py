#!/bin/env python3
import os
from dataclasses import dataclass
from plantweb.render import render
from textwrap import dedent
from typing import List

requirements = {
    'Verpflichtend': 'mandatory',
    'Empfohlen': 'recommended',
    'Optional': 'optional'
}

@dataclass
class UML_Class():
    id: str
    name: str
    requirement: str
    properties: List

    def add_property(self, property):
        self.properties.append(property)
    
    def __repr__(self):
        properties = []
        for requirement in requirements.values():
            requirement_properties = sorted([str(p) for p in self.properties if p.requirement == requirement])
            if len(requirement_properties) > 0:
                properties.append("\n".join([f'<i>  <<{requirement}>>  </i>'] + requirement_properties))
        return dedent(f"""
            class {self.id} as " **{self.name}** " <<{self.requirement}>> {{
                {"\n\n".join(properties)}
            }}
        """)

@dataclass
class UML_Property():
    name: str
    cardinality: str
    requirement: str
    
    def __repr__(self):
        cardinality = f" [{self.cardinality}]" if self.cardinality is not None and self.cardinality != '1' else ''
        return f'<font color="Maroon">{self.name}{cardinality}</font>'

@dataclass
class UML_Relation():
    source_id: str
    target_id: str
    property: UML_Property
    orientation: str = ''

    def __repr__(self):
        return f'{self.source_id} -{self.orientation}-> "  <back:#FFFFFF>{self.property.cardinality}</back>  " {self.target_id} : "  <back:#FFFFFF>{self.property.name}</back>  \\n  <back:#FFFFFF><<{self.property.requirement}>></back>  "'

@dataclass
class UML_Template():
    classes: List[UML_Class]
    relations: List[UML_Relation]

    def write(self, target_path):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w') as f:
            f.write(str(self))
    
    def render(self, target_path):
        response = render(str(self), engine='plantuml', format='png', cacheopts={ 'use_cache': False })
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'wb') as f:
            f.write(response[0])

    def __repr__(self):
        return dedent(f"""
            @startuml DCAT-AP.EIA

            hide circle
            'ortho is bugged, so it's disabled for now
            'skinparam linetype ortho
            'skinparam nodesep 140
            'skinparam ranksep 140

            <style>
                mainframe {{
                    Margin 10
                    Padding 30
                }}
                class {{
                    BackgroundColor #FloralWhite|#BlanchedAlmond
                    FontSize 12
                }}
            </style>

            mainframe <plain> class DCAT-AP.EIA </plain>

            {''.join(str(c) for c in self.classes)}

            {'\n'.join(str(r) for r in self.relations)}
            @enduml
        """)