#!/usr/local/autopkg/python
"""See docstring for MunkiRepoVersionChecker class"""

import os
import plistlib

from autopkglib import Processor

__all__ = ["MunkiRepoVersionChecker"]


class MunkiRepoVersionChecker(Processor):
    """Stops processing the recipe if the Munki repo's 'all' catalog already
    holds an item with the given name and version. Without a local catalog
    (a repo reached through a plugin, or makecatalogs never run) it lets the
    recipe go on, and MunkiImporter's own duplicate check applies."""

    description = __doc__
    input_variables = {
        "MUNKI_REPO": {
            "required": True,
            "description": "Path to the Munki repo.",
        },
        "name": {
            "required": True,
            "description": "Name of the Munki item.",
        },
        "version": {
            "required": True,
            "description": "Version to look for.",
        },
    }
    output_variables = {
        "stop_processing_recipe": {
            "description": "True if the version is already in the Munki repo."
        }
    }

    def main(self):
        catalog_path = os.path.join(self.env["MUNKI_REPO"], "catalogs", "all")
        name = self.env["name"]
        version = self.env["version"]

        if not os.path.isfile(catalog_path):
            self.output(f"No catalog at {catalog_path}, not checking.")
            self.env["stop_processing_recipe"] = False
            return

        with open(catalog_path, "rb") as f:
            catalog = plistlib.load(f)

        found = any(
            item.get("name") == name and item.get("version") == version
            for item in catalog
        )
        self.env["stop_processing_recipe"] = found
        if found:
            self.output(f"{name} {version} is already in the Munki repo.")
        else:
            self.output(f"{name} {version} is not in the Munki repo yet.")


if __name__ == "__main__":
    PROCESSOR = MunkiRepoVersionChecker()
    PROCESSOR.execute_shell()
