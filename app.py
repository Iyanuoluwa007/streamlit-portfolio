import streamlit as st
import requests
import pathlib, json
from datetime import datetime

# ---------- Page Config ----------
st.set_page_config(
    page_title="Iyanuoluwa Oke | Robotics & AI Engineer",
    page_icon="🤖",
    layout="wide"
)

# ---------- Background Styling ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0A1E2E 0%, #0E7490 100%);
    color: #E6F0FA;
}
h1, h2, h3, h4, h5, h6 {
    color: #3BC9DB;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero Section ----------
st.markdown("""
<div style="text-align:center; padding:2rem;">
  <h1>👋 Hi, I'm <span style="color:#3BC9DB;">Iyanuoluwa Oke</span></h1>
  <h3>Robotics & AI Engineer | Computer Vision | ROS2 Developer</h3>
  <p style="max-width:800px; margin:auto;">
    I build intelligent robotics and AI systems with strong focus on real-time perception,
    computer vision, and deep learning. Explore my projects below 🚀.
  </p>
  <br>
  <a href="https://github.com/Iyanuoluwa007" style="margin:10px; text-decoration:none;">
    <button style="padding:10px 20px; border:none; border-radius:8px; background:#3BC9DB; color:#0A1E2E; font-weight:bold;">💻 GitHub</button>
  </a>
  <a href="https://www.linkedin.com/in/iyanuoluwa-enoch-oke/" style="margin:10px; text-decoration:none;">
    <button style="padding:10px 20px; border:none; border-radius:8px; background:#3BC9DB; color:#0A1E2E; font-weight:bold;">🔗 LinkedIn</button>
  </a>
  <a href="mailto:oke.iyanuoluwa12@gmail.com" style="margin:10px; text-decoration:none;">
    <button style="padding:10px 20px; border:none; border-radius:8px; background:#3BC9DB; color:#0A1E2E; font-weight:bold;">📧 Contact</button>
  </a>
</div>
""", unsafe_allow_html=True)

# ---------- Load Featured Projects ----------
def load_featured():
    cfg_path = pathlib.Path("projects.json")
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return []

featured_projects = load_featured()

# ---------- Fetch All GitHub Repos ----------
@st.cache_data(ttl=3600)
def fetch_repos(user="Iyanuoluwa007"):
    url = f"https://api.github.com/users/{user}/repos?per_page=100&sort=updated"
    r = requests.get(url, timeout=30)
    if r.status_code == 200:
        repos = r.json()
        return [repo for repo in repos if not repo.get("fork") and not repo.get("archived")]
    return []

repos = fetch_repos()

# ---------- Featured Section ----------
if featured_projects:
    st.subheader("⭐ Featured Projects")
    for pr in featured_projects:
        with st.container():
            st.markdown(f"### [{pr['title']}]({pr['repo_url']})")
            st.write(pr.get("description",""))
            if "tech" in pr:
                st.markdown(" ".join([f"<span class='chip'>{t}</span>" for t in pr["tech"]]), unsafe_allow_html=True)
            col1, col2 = st.columns([1,1])
            with col1:
                st.link_button("GitHub Repo", pr["repo_url"], use_container_width=True)
            with col2:
                if pr.get("demo_url"):
                    st.link_button("Live Demo", pr["demo_url"], use_container_width=True)
            st.markdown("---")

# ---------- All Repos ----------
st.subheader("📂 All GitHub Repositories")
for repo in repos:
    with st.container():
        name = repo["name"]
        url = repo["html_url"]
        desc = repo.get("description") or ""
        stars = repo.get("stargazers_count", 0)
        updated = repo.get("pushed_at") or repo.get("updated_at")
        ts = datetime.fromisoformat(updated.replace("Z","+00:00")) if updated else None

        st.markdown(f"#### [{name}]({url})")
        st.write(desc)
        st.caption(f"⭐ {stars} • Updated {ts.date() if ts else ''}")
        st.markdown("---")

# ---------- Contact Section ----------
st.markdown(f"""
---
### 📩 Get in Touch
- 📧 Email: [oke.iyanuoluwa12@gmail.com](mailto:oke.iyanuoluwa12@gmail.com)  
- 💼 LinkedIn: [linkedin.com/in/iyanuoluwa-enoch-oke](https://www.linkedin.com/in/iyanuoluwa-enoch-oke/)  
- 📝 [Download my CV](https://drive.google.com/file/d/1QwpycQIutZnM9STD5lv9PMcv4v3nZxjS/view?usp=sharing)  

---
<small style="color:#ccc;">Built with ❤️ using Streamlit • © 2025 Iyanuoluwa Oke</small>
""", unsafe_allow_html=True)

# ---------- CSS Styling ----------
st.markdown("""
<style>
.chip {
    display:inline-block;
    padding:5px 12px;
    border-radius:20px;
    background:#3BC9DB;
    color:#0A1E2E;
    margin:4px 4px;
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)
