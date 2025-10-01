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

# ---------- Load Featured Projects ----------
def load_projects():
    cfg_path = pathlib.Path("projects.json")
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return []

projects = load_projects()

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs(["🤖 Robotics", "🧠 Computer Vision", "📊 AI/ML", "⚙️ Deployment"])

# ---------- Helper: Render Project Cards ----------
def render_project_card(project):
    col1, col2 = st.columns([1,2])
    with col1:
        if project.get("thumbnail"):
            st.image(project["thumbnail"], use_column_width=True)
    with col2:
        st.markdown(f"### [{project['title']}]({project['repo_url']})")
        st.write(project.get("description", ""))
        if "tech" in project:
            st.markdown(" ".join([f"<span class='chip'>{t}</span>" for t in project["tech"]]), unsafe_allow_html=True)
        btns = st.columns(2)
        with btns[0]:
            st.link_button("GitHub Repo", project["repo_url"], use_container_width=True)
        with btns[1]:
            if project.get("demo_url"):
                st.link_button("Live Demo", project["demo_url"], use_container_width=True)

# ---------- Display Projects by Category ----------
categories = {
    "🤖 Robotics": ["ros2_yolo_ws", "submarine_ws", "ws_moveit"],
    "🧠 Computer Vision": ["Plant-Disease-Detection-using-CNN-PyTorch", "Brain-Tumor-Classification", "British-Sign-Language-BSL-Recognition"],
    "📊 AI/ML": ["Gesture_Control", "Yolo_and_SSD", "Chatgpt-bigram"],
    "⚙️ Deployment": ["streamlit-portfolio", "mlops_pipeline_project", "cloud_ml_deployment"]
}

tabs = [tab1, tab2, tab3, tab4]
for tab, (cat, repo_names) in zip(tabs, categories.items()):
    with tab:
        st.subheader(f"{cat} Projects")
        for pr in projects:
            if any(name.lower() in pr['repo_url'].lower() for name in repo_names):
                with st.container():
                    render_project_card(pr)
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
