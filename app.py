
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

import requests
import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="Iyanuoluwa Enoch | Project Portfolio",
    page_icon="🧠",
    layout="wide"
)

# ---------- Header ----------
st.title("👋 Hi, I'm Iyanuoluwa — Robotics & AI Engineer")
st.write(
    "I build Robotics, Computer Vision, and ML systems. "
    "Below is a curated selection of my open‑source projects."
)

# Quick links row
cols = st.columns([1,1,1,3])
with cols[0]:
    st.link_button("GitHub", "https://github.com/Iyanuoluwa007")
with cols[1]:
    st.link_button("LinkedIn", "https://www.linkedin.com/in/iyanuoluwa-enoch-oke/")
with cols[2]:
    st.link_button("Email", "mailto:oke.iyanuoluwa12@gmail.com")

st.divider()

# ---------- Config ----------
# Secrets allow higher GitHub rate limits and private repo access if needed.
GH_USERNAME = st.secrets.get("GITHUB_USERNAME", "Iyanuoluwa007")
GH_TOKEN = st.secrets.get("GITHUB_TOKEN", None)

HEADERS = {"Accept": "application/vnd.github+json"}
if GH_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GH_TOKEN}"

API_BASE = "https://api.github.com"

# ---------- Data helpers ----------
@st.cache_data(ttl=3600)
def fetch_repos(user: str) -> List[Dict[str, Any]]:
    """Fetch public repos for a username (excluding forks and archived)."""
    url = f"{API_BASE}/users/{user}/repos?per_page=100&sort=updated"
    all_repos = []
    while url:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        all_repos.extend(r.json())
        # Pagination
        next_url = None
        if 'link' in r.headers:
            links = r.headers['link'].split(',')
            for link in links:
                if 'rel="next"' in link:
                    next_url = link[link.find('<')+1:link.find('>')]
                    break
        url = next_url
    # filter
    filtered = [repo for repo in all_repos if not repo.get("fork") and not repo.get("archived")]
    return filtered

@st.cache_data(ttl=3600)
def fetch_readme(owner: str, repo: str) -> Optional[str]:
    url = f"{API_BASE}/repos/{owner}/{repo}/readme"
    r = requests.get(url, headers=HEADERS, timeout=30)
    if r.status_code != 200:
        return None
    data = r.json()
    raw = data.get("download_url")
    if not raw:
        return None
    rr = requests.get(raw, timeout=30)
    if rr.status_code == 200:
        return rr.text
    return None

def load_featured() -> List[Dict[str, Any]]:
    """Load curated featured projects from projects.json if present."""
    cfg_path = pathlib.Path("projects.json")
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return []

def get_opengraph_image(owner: str, repo: str) -> str:
    # GitHub OG preview image
    return f"https://opengraph.githubassets.com/1/{owner}/{repo}"

# ---------- Sidebar controls ----------
st.sidebar.header("Filters & Settings")
st.sidebar.caption("Tip: Add a **GITHUB_TOKEN** in app secrets for higher API limits.")

query = st.sidebar.text_input("Search name/description", "")
sort_by = st.sidebar.selectbox("Sort by", ["Updated", "Stars", "Name"], index=0)
show_forks = st.sidebar.checkbox("Include forks", value=False)

# ---------- Load data ----------
try:
    repos = fetch_repos(GH_USERNAME)
except Exception as e:
    st.error(f"Could not fetch GitHub repositories: {e}")
    repos = []

if show_forks:
    # If user wants forks, refetch without filtering
    try:
        url = f"{API_BASE}/users/{GH_USERNAME}/repos?per_page=100&sort=updated"
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        repos = r.json()
    except Exception:
        pass

# Build language/topic sets
languages = sorted({(repo.get("language") or "Other") for repo in repos})
topics = set()
for repo in repos:
    ts = repo.get("topics") or []
    for t in ts:
        topics.add(t)
topics = sorted(topics)

lang_filter = st.sidebar.multiselect("Languages", languages, default=[])
topic_filter = st.sidebar.multiselect("Topics", topics, default=[])

# ---------- Featured Section ----------
featured = load_featured()
if featured:
    st.subheader("⭐ Featured Projects")
    for item in featured:
        with st.container(border=True):
            top = st.columns([3,1])
            with top[0]:
                st.markdown(f"### [{item['title']}]({item['repo_url']})")
                st.write(item.get("description",""))
                chips = []
                for tech in item.get("tech", []):
                    chips.append(f"<span class='chip'>{tech}</span>")
                st.markdown(" ".join(chips), unsafe_allow_html=True)
                if item.get("demo_url"):
                    st.link_button("Live Demo", item["demo_url"])
            with top[1]:
                if thumb := item.get("thumbnail"):
                    st.image(thumb, use_column_width=True)
    st.divider()

# ---------- Filtering ----------
def passes_filters(r):
    name = r.get("name","").lower()
    desc = (r.get("description") or "").lower()
    if query and (query.lower() not in name) and (query.lower() not in desc):
        return False
    if lang_filter:
        lang = (r.get("language") or "Other")
        if lang not in lang_filter:
            return False
    if topic_filter:
        ts = r.get("topics") or []
        if not any(t in ts for t in topic_filter):
            return False
    return True

repos = [r for r in repos if passes_filters(r)]

# Sorting
if sort_by == "Updated":
    repos.sort(key=lambda r: r.get("pushed_at") or r.get("updated_at") or "", reverse=True)
elif sort_by == "Stars":
    repos.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
else:
    repos.sort(key=lambda r: r.get("name","").lower())

# ---------- Render repo cards ----------
st.subheader("📦 All Repositories")
if not repos:
    st.info("No repositories match your filters.")
else:
    # grid layout
    cols = st.columns(2, gap="large")
    for idx, repo in enumerate(repos):
        with cols[idx % 2]:
            with st.container(border=True):
                owner = repo["owner"]["login"]
                name = repo["name"]
                html_url = repo["html_url"]
                description = repo.get("description") or ""
                lang = repo.get("language") or "Other"
                stars = repo.get("stargazers_count", 0)
                updated = repo.get("pushed_at") or repo.get("updated_at")
                homepage = repo.get("homepage") or ""
                topics = repo.get("topics") or []

                # Header row
                top = st.columns([4,1])
                with top[0]:
                    st.markdown(f"#### [{name}]({html_url})")
                    st.write(description)
                with top[1]:
                    st.image(get_opengraph_image(owner, name), use_column_width=True)

                # Chips
                chip_html = []
                chip_html.append(f"<span class='chip'>{lang}</span>")
                for t in topics[:6]:
                    chip_html.append(f"<span class='chip'>{t}</span>")
                st.markdown(" ".join(chip_html), unsafe_allow_html=True)

                # Meta + buttons
                meta = st.columns([1,1,2])
                with meta[0]:
                    st.metric("⭐ Stars", value=stars)
                with meta[1]:
                    ts = datetime.fromisoformat((updated or '').replace('Z','+00:00')) if updated else None
                    st.caption(f"Updated: {ts.date() if ts else '—'}")
                with meta[2]:
                    btn_cols = st.columns(2)
                    with btn_cols[0]:
                        st.link_button("Repo", html_url, use_container_width=True)
                    with btn_cols[1]:
                        st.link_button("Demo", homepage if homepage else html_url, use_container_width=True)

                # Readme preview
                with st.expander("Readme (first 3000 chars)"):
                    text = fetch_readme(owner, name)
                    if text:
                        st.code(text[:3000] + ("..." if len(text) > 3000 else ""), language="markdown")
                    else:
                        st.info("No README found or not accessible.")

# ---------- Footer & Styles ----------
st.divider()
st.caption("Built with Streamlit • © 2025 Iyanu")

st.markdown("""
<style>
.chip {
    display:inline-block;
    padding: 3px 8px;
    border-radius: 999px;
    background: rgba(127,127,127,0.15);
    margin-right: 6px;
    margin-top: 6px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)
