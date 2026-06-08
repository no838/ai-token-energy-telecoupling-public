# Zenodo archive checklist

## Target release

```text
v1.0-applied-energy-public-release
```

## Repository metadata files

- `.zenodo.json`
- `CITATION.cff`
- `LICENSE`
- `DATA_LICENSE.md`
- `THIRD_PARTY_DATA_NOTICE.md`
- `docs/RELEASE_NOTES_v1.0_applied_energy_public_release.md`

## Manual actions still required

1. Enable the GitHub repository under the connected Zenodo account.
2. Create or publish a GitHub release from the existing tag
   `v1.0-applied-energy-public-release`.
3. Wait for Zenodo to archive the release and mint the DOI.
4. Record the DOI in:
   - `CITATION.cff`
   - `docs/DATA_AND_CODE_AVAILABILITY.md`
   - the active manuscript `Data availability` and `Code availability`
     paragraphs

## Do not do before DOI exists

- do not write a Zenodo DOI into the manuscript
- do not write a Zenodo DOI into `CITATION.cff`
- do not describe Zenodo archiving as complete
