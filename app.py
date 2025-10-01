import streamlit as st
import pathlib
import json

# ---------- Page Config ----------
st.set_page_config(
    page_title="Iyanuoluwa Oke | Robotics & AI Engineer",
    page_icon="🤖",
    layout="wide"
)

# ---------- Hero Section ----------
st.markdown("""
<div style="text-align:center; padding:2rem; background:linear-gradient(90deg,#0A1E2E,#0E7490); border-radius:12px;">
  <h1 style="color:#E6F0FA;">👋 Hi, I'm <span style="color:#3BC9DB;">Iyanuoluwa Oke</span></h1>
  <h3 style="color:#E6F0FA;">Robotics & AI Engineer | Computer Vision | ROS2 Developer</h3>
  <p style="color:#E6F0FA; max-width:800px; margin:auto;">
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

st.write("")

# ---------- Load Projects ----------
def load_projects():
    cfg_path = pathlib.Path("projects.json")
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return []

projects = load_projects()

# ---------- Render Projects Straight Down ----------
st.subheader("📂 My Projects")

for pr in projects:
    with st.container():
        st.markdown(f"### [{pr['title']}]({pr['repo_url']})")
        st.write(pr.get("description", ""))
        
        # Tech stack chips
        if "tech" in pr:
            st.markdown(" ".join([f"<span class='chip'>{t}</span>" for t in pr["tech"]]), unsafe_allow_html=True)
        
        # Links
        col1, col2 = st.columns([1,1])
        with col1:
            st.link_button("GitHub Repo", pr["repo_url"], use_container_width=True)
        with col2:
            if pr.get("demo_url"):
                st.link_button("Live Demo", pr["demo_url"], use_container_width=True)
        
        st.markdown("---")

# ---------- Contact Section ----------
st.markdown("""
---
### 📩 Get in Touch
- 📧 Email: [oke.iyanuoluwa12@gmail.com](mailto:oke.iyanuoluwa12@gmail.com)  
- 💼 LinkedIn: [linkedin.com/in/iyanuoluwa-enoch-oke](https://www.linkedin.com/in/iyanuoluwa-enoch-oke/)  
- 📝 [Download my CV](https://github.com/Iyanuoluwa007)  

---
<small style="color:grey;">Built with ❤️ using Streamlit • © 2025 Iyanuoluwa Oke</small>
""", unsafe_allow_html=True)

# ---------- CSS Styling ----------
st.markdown("""
<style>
.chip {
    display:inline-block;
    padding:5px 12px;
    border-radius:20px;
    background:#0E7490;
    color:white;
    margin:4px 4px;
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)
