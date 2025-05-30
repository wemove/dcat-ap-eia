# Readme

Below you can find instructions regarding the update process and the release process.

## Update Procedure

If a change to the API is to be made, make sure this change is reflected in all related resources, where applicable:

- [ ] OpenAPI specification: [api-eia.yml](api-eia.yml)
- [ ] Documentation: [doc-eia.html](doc-eia.html)
- [ ] SHACL shapefile: [shacl/dcat-ap-eia-shapes.ttl](shacl/dcat-ap-eia-shapes.ttl)
- [ ] UML diagram: [DCAT-AP-EIA.jpg](DCAT-AP-EIA.jpg)
  - no manual changes necessary; done via script, see end of paragraph
- [ ] Codelists: [codelists](codelists)
- [ ] Examples: [examples/eia-example-full.xml](examples/eia-example-full.xml), [examples/eia-example-03.xml](examples/eia-example-03.xml)

After making the changes, run [scripts/update.sh](scripts/update.sh) (Linux) or [scripts/update.bat](scripts/update.bat) (Windows), to
* tidy up the HTML documentation
* validate the SHACL shapefile and the examples
* re-create the UML diagram

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
- In `develop`, add a new dummy entry to the changelog

Finally, announce the new version via mail and ADO.
