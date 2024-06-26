# Readme

Below you can find instructions regarding the update process and the release process.

## Update Procedure

If a change to the API is to be made, make sure this change is reflected in all related resources, where applicable:

- [ ] OpenAPI specification: [api-eia.yml](api-eia.yml)
- [ ] documentation: [doc-eia.html](doc-eia.html)
- [ ] UML diagram: [dcat-ap-eia.eapx](dcat-ap-eia.eapx) and [DCAT-AP.EIA.jpg](DCAT-AP.EIA.jpg)
- [ ] SHACL shapefile: [shacl/dcat-ap-eia_shacl-shapes.ttl](shacl/dcat-ap-eia_shacl-shapes.ttl)
- [ ] [codelists](codelists)
- [ ] [examples](examples)

If the changes encompass the `SHACL` shapefile or the examples, ensure that the shapefile still correctly validates them all, e.g. using
https://www.itb.ec.europa.eu/shacl/any/upload

Finally, update the [changelog](../../CHANGELOG.md).

## Release Procedure

Run [release.sh](release.sh) and follow the instructions.

Alternatively, you can manually create a release:
- Validate all examples using the `SHACL` shapefile
- Finalize the [changelog](../../CHANGELOG.md)
- Create a new folder in [releases](../../releases), named after your new version number (semver)
- Copy all appropriate files from [drafts/0.0.1-draft-0.1](.) into this new folder
- In the new version folder, update
  - the `latestVersion` property in `doc-eia.html`
  - the `version` property in `api-eia.yml`
  - the version in `README.md`
- Merge `develop` into `main`

Finally, announce the new version via mail and ADO.
