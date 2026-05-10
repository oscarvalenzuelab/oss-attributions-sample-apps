# Generating Open Source Legal Notices using SBOMs

There's different approaches to generate Legal Notices, and while the most common depends on manually collecting information from the software artifacts, there are chances to use information from the package metadata troguht the package managers to produce an Open Source Package Inventory that later feed the generation of OSS attributions. While an Open Source Package Inventory (OSPI) is similar to an Software Build of Materials (SBoM), aren't usually the same as license attestation is not a requirement for a valid SBOM. Instead an OSPI presume that such information will be present in order to perform a risk evaluation for the project.

This guide describes how to produce an OSPI, using tools to produce SBOMs but with additional configurations to produce license attestation or obtain such information from the package registry (Maven, PyPI, NPM, etc.) to generate a human redeable Legal Notices file. 
The Legal Notices is a requirement to distribute software that use (consume) Open Source Software, as most licenses require to provide attributions to the original author.

Here are some examples for common languages and package managers on how to create notices:

* Projects using Maven
* Projects using Gradle
* Projects using PyPI

## Note on sample apps

The sample apps under `pypi/vulnerable-sample-app/` and `maven/sample-app/` intentionally pin known-vulnerable dependency versions (e.g. `Django==1.11.29`, `requests==2.19.1`, `PyYAML==3.12`). They exist as fixtures to demonstrate SBOM and OSS-attribution generation against realistic, version-locked manifests — not as code intended to be deployed. Dependabot is configured to skip update PRs for these paths; security alerts may still surface in the dependency graph and are kept as documentation of the demo's vulnerability surface.