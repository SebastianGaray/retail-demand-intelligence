# Streamlit Community Cloud

The dashboard reads a precomputed artifact run directly. It does not call FastAPI and does not
train a model at startup.

## Artifact bundle

The tracked bundle is `demo_artifacts/v0.1.0`. Build it from the local synthetic pipeline with:

```bash
make demo-artifacts
```

The command validates dataset contracts, required files, row counts, and SHA-256 checksums before
replacing the bundle.

## Deployment settings

1. Confirm the artifact bundle contains synthetic data only and passes `make check` locally.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) and create an app from this
   repository.
3. Select the release branch and use `src/retail_demand/dashboard/app.py` as the entrypoint.
4. In advanced settings, select Python 3.12.
5. Leave `RETAIL_DEMAND_ARTIFACT_DIRECTORY` unset to use `demo_artifacts/v0.1.0`, or set it to a
   different validated bundle.
6. Deploy, inspect the build log, and complete the
   [manual dashboard smoke test](interfaces.md#manual-dashboard-smoke-test).

Community Cloud recognizes the root `uv.lock`, so no separate requirements file is needed. The
app uses no credentials. If future deployment settings contain secrets, store them in Community
Cloud settings and never commit `.streamlit/secrets.toml`.

See Streamlit's official documentation for
[dependency files](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
and [deployment settings](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).
