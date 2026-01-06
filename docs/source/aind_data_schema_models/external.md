# External registries

External registries act as an application programming interfaces (API). They allow us to store metadata from registries that are too large to store inside of the `aind-data-schema-models` repository. Because of this, we can't enumerate all of the options for each model in the documentation. Instead we link here to the search page for each registry along with one example of what the atlas responses look like.

## Model definitions

### MouseAnatomyModel

[EMAPA](https://www.ebi.ac.uk/ols4/ontologies/emapa)

Base model for mouse anatomy. Some examples:

| Name | Registry | Registry Identifier |
|------|-------|--------|
| `heart` | `Registry.EMAPA` |  `16105`  |

### Gene

[GenBank](https://www.ncbi.nlm.nih.gov/genbank/)

Base model for genes. One example:

| Name | Description | Registry | Registry Identifier |
|------|------|-------|--------|
| `gfp` | `Human adenovirus B isolate 340-2010 DNA, complete genome` | `Registry.GENBANK` | `LN515608` |
