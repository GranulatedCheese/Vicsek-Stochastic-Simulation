import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

from core.physics_math import initialize_system, get_new_angles, update_positions

st.set_page_config(page_title="Project Vortex", layout="centered")
st.title("Active Matter Simulation: Emergent Phase Transitions")

st.sidebar.header("System Parameters")
frames = st.sidebar.slider("Frames", min_value=50, max_value=500, value = 50, step = 10)
N = st.sidebar.slider("Density (Number of Agents)", min_value=50, max_value=500, value=200, step=10)
noise = st.sidebar.slider("Noise Level (Temperature)", min_value=0.0, max_value=3.0, value=0.1, step=0.1)
radius = st.sidebar.slider("Interaction Radius", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
velocity = st.sidebar.slider("Velocity", min_value=0.1, max_value=1.0, value=0.5, step=0.1)

box_size = 10.0

if 'positions' not in st.session_state or st.sidebar.button("Reset Simulation"):
    pos, ang = initialize_system(N, box_size)
    st.session_state.positions = pos
    st.session_state.angles = ang

plot_placeholder = st.empty()

if st.button(f"Run Simulation ({frames} Frames)"):
    for frame in range(frames):
        new_angles = get_new_angles(
            st.session_state.positions, 
            st.session_state.angles, 
            radius, 
            noise, 
            box_size
        )
        st.session_state.angles = new_angles
        
        st.session_state.positions = update_positions(
            st.session_state.positions, 
            st.session_state.angles, 
            velocity, 
            box_size
        )
        
        fig, ax = plt.subplots(figsize=(6, 6))
        u = np.cos(st.session_state.angles)
        v = np.sin(st.session_state.angles)
        
        ax.quiver(st.session_state.positions[:, 0], st.session_state.positions[:, 1], 
                  u, v, color='red', alpha=0.5)
        
    
        ax.quiver(st.session_state.positions[0, 0], st.session_state.positions[0, 1], 
                  u[0], v[0], color='blue', alpha=1.0)
        
        tracer_circle = plt.Circle( #type: ignore
            (st.session_state.positions[0, 0], st.session_state.positions[0, 1]), 
            radius, color='blue', fill=False, linestyle='--', alpha=0.8
        )
        ax.add_patch(tracer_circle)
        # --------------------------
        
        ax.set_xlim(0, box_size)
        ax.set_ylim(0, box_size)
        ax.set_xticks([]) 
        ax.set_yticks([])
        ax.set_title(f"Frame: {frame+1} | Noise: {noise} | Radius: {radius}")
        
        plot_placeholder.pyplot(fig)
        plt.close(fig) 
        time.sleep(0.05)