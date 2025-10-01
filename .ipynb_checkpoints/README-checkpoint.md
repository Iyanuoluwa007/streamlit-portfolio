
# Streamlit Portfolio (Starter)

A simple Streamlit app that automatically showcases your GitHub projects with filters, search, and featured cards.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Configure (optional)

- Create `.streamlit/secrets.toml` with:
  ```toml
  GITHUB_USERNAME = "Iyanuoluwa007"
  # Optional for higher rate limits:
  # GITHUB_TOKEN = "ghp_..."
  ```

- Curate **featured projects** by editing `projects.json`.

## Deploy

- Push this folder to a GitHub repo.
- On https://share.streamlit.io (Streamlit Community Cloud):
  - Connect your repo.
  - Set the main file to `app.py`.
  - (Optional) Add secrets (same keys as above) under *App settings → Secrets*.

## Customize

- Update the title, intro text, or theme in `app.py` and `.streamlit/config.toml`.
- Add your own thumbnails in `assets/` and reference them inside `projects.json`.
