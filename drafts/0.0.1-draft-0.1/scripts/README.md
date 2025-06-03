# DCAT-AP.EIA scripts

The below scripts can be run independently of each other, or in one swoop via

* [update.sh](update.sh) (Linux/MacOS)
* [update.bat](update.bat) (Windows)


## Create UML diagram

The diagram is created based on the documentation and the SHACL shape file.

* Prerequisites: python

```
./diagram/create_diagram.sh (Linux/MacOS)
diagram\create_diagram.bat (Windows)
```


## Clean up HTML documentation

* Prerequisites: tidy

```
./tidy/tidy.sh (Linux/MacOS)
tidy\tidy.bat (Windows)
```


## Validate SHACL shapefile and examples

The SHACL shapefile and the XML examples are validated using the EU SHACL Validator REST API: https://www.itb.ec.europa.eu/shacl

* Prerequisites: python

Validate the SHACL file itself:
```
./validate/validate.sh shacl (Linux/MacOS)
validate\validate.bat shacl (Windows)
```

Validate the examples using the SHACL file:
```
./validate/validate.sh examples (Linux/MacOS)
validate\validate.bat examples (Windows)
```
