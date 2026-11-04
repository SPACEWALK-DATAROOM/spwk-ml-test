# Portable reviewed campaign contracts

```sh
python tests/file50_python/pipeline/run_quality.py --coverage --output /path/to/evidence
```

The current interpreter supplies pytest/coverage and actual libraries required by the repository. Additional prepared/private package directories can be given through PIPELINE_EXTRA_PYTHONPATH. No installation is performed. Only explicit campaign additions listed in quality_scope.json run. Pre-campaign source/tests/locks are unchanged. A minimal synthetic environment and output-owned TMPDIR isolate dependencies. Python children inherit a network-denying sitecustomize. See quality-review and exclusions for static manifest/documentation/subprocess contracts versus Python production behavior; no model/training/production operations execute.
