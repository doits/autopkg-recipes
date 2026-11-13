# AGENTS.md

- New recipes are YAML (`<Name>.download.recipe.yaml`, `<Name>.munki.recipe.yaml`, `MinimumVersion: "2.3"`), split into download and munki recipe like the existing ones; older recipes are still plist.
- Identifiers follow `com.github.doits.<download|munki>.<Name>`.
- Every download recipe verifies the app with `CodeSignatureVerifier`.
- This repository is public: nothing about anyone's machine, Munki repository or setup goes into its files or commit messages.
