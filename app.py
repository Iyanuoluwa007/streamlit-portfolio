import streamlit as st
import json
import pathlib

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
</div>
""", unsafe_allow_html=True)

# ---------- Load Projects ----------
def load_projects():
    cfg_path = pathlib.Path("projects.json")
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return []

projects = load_projects()

# ---------- CSS for Flip Cards ----------
st.markdown("""
<style>
.container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-top: 2rem;
}
.card {
  perspective: 1000px;
  width: 100%;
  height: 350px;
}
.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}
.card:hover .card-inner {
  transform: rotateY(180deg);
}
.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  backface-visibility: hidden;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.card-front {
  background: #fff;
  color: #111;
}
.card-front img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.card-front h3 {
  margin: 0.5rem;
  font-size: 1.2rem;
  color: #0E7490;
}
.card-front p {
  font-size: 0.9rem;
  padding: 0 0.8rem;
}
.card-back {
  background: #0A1E2E;
  color: #E6F0FA;
  transform: rotateY(180deg);
  padding: 1rem;
  text-align: center;
}
.card-back h3 {
  margin-bottom: 1rem;
}
.card-back a {
  display: inline-block;
  margin: 0.3rem;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  background: #3BC9DB;
  color: #0A1E2E;
  font-weight: bold;
  text-decoration: none;
}
.chip {
  display:inline-block;
  padding:3px 10px;
  border-radius:20px;
  background:#0E7490;
  color:white;
  font-size:0.8rem;
  margin:2px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Render All Projects Vertically ----------
st.markdown("<div class='container'>", unsafe_allow_html=True)

for pr in projects:
    tech_html = " ".join([f"<span class='chip'>{t}</span>" for t in pr.get("tech", [])])
    st.markdown(f"""
    <div class="card">
      <div class="card-inner">
        <div class="card-front">
          <img src="{pr.get("thumbnail","")}" alt="thumbnail">
          <h3>{pr['title']}</h3>
          <p>{pr.get("description","")[:120]}...</p>
          <div style="padding:0.5rem;">{tech_html}</div>
        </div>
        <div class="card-back">
          <h3>{pr['title']}</h3>
          <p>{pr.get("description","")}</p>
          <a href="{pr['repo_url']}" target="_blank">GitHub Repo</a>
          {"<a href='"+pr['demo_url']+"' target='_blank'>Live Demo</a>" if pr.get("demo_url") else ""}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
