#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 09:58:45 2023

@author: juanjosefernandezmorales
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

def pendulum_equations_3D(y, t, g, l):
    """Compute the derivatives for the spherical coordinates of the 3D simple pendulum.
    
    Args:
        y (list): A list of [theta, omega_theta, phi, omega_phi] values.
        t (float): The time at which to compute the derivatives.
        g (float): The gravitational constant.
        l (float): The length of the pendulum.

    Returns:
        dydt (list): A list of the computed derivatives.
    """
    theta, omega_theta, phi, omega_phi = y
    dydt = [
        omega_theta,
        -(g/l) * np.sin(theta) - (omega_phi**2) * np.sin(theta) * np.cos(theta),
        omega_phi,
        2 * omega_theta * omega_phi * np.cos(theta) / np.sin(theta)
    ]
    return dydt

def cart_coords(theta, phi, l):
    """Convert the spherical coordinates to Cartesian coordinates.
    
    Args:
        theta (float): The polar angle.
        phi (float): The azimuthal angle.
        l (float): The length of the pendulum.

    Returns:
        x, y, z (float): The Cartesian coordinates.
    """
    x = l * np.sin(theta) * np.cos(phi)
    y = l * np.sin(theta) * np.sin(phi)
    z = -l * np.cos(theta)
    return x, y, z

def solve_pendulum_ode(y0, t, g, l):
    """Solve the differential equations for the 3D simple pendulum.
    
    Args:
        y0 (list): The initial conditions [theta, omega_theta, phi, omega_phi].
        t (numpy array): The time vector.
        g (float): The gravitational constant.
        l (float): The length of the pendulum.

    Returns:
        sol (numpy array): The solution array of the pendulum's motion.
    """
    sol = odeint(pendulum_equations_3D, y0, t, args=(g, l))
    return sol

def setup_3d_plot(l):
    """Set up the 3D plot for the pendulum simulation.
    
    Args:
        l (float): The length of the pendulum.

    Returns:
        fig (matplotlib.figure.Figure): The figure object.
        ax (matplotlib.axes._subplots.Axes3DSubplot): The 3D axes object.
    """
    fig = plt.figure(figsize = (10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-l, l])
    ax.set_ylim([-l, l])
    ax.set_zlim([-l, 0])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Simple Pendulum Simulation')
    ax.grid(True)  # Add grid
    return fig, ax

# Parameters
g = 9.81
l = 1.0
y0 = [np.pi/4, 0.0, np.pi/2, np.pi/2]

# Time vector
t = np.linspace(0, 10, 1000)

# Solve the differential equations
sol = solve_pendulum_ode(y0, t, g, l)

# Convert the spherical coordinates to Cartesian coordinates
x, y, z = cart_coords(sol[:, 0], sol[:, 2], l)

# Set up the 3D plot
fig, ax = setup_3d_plot(l)

# Improve plot aesthetics
color_pendulum = 'blue'
color_rope = 'black'
color_tail = 'red'
marker_pendulum = 'o'
marker_rope = '-'
marker_tail = '--'
linewidth_pendulum = 2
linewidth_rope = 1
linewidth_tail = 1

# Initialize the animation plot
pendulum, = ax.plot([], [], [], 
                    marker_pendulum + marker_rope, lw=linewidth_pendulum, 
                    color=color_pendulum, label='Pendulum')
rope, = ax.plot([], [], [], 
                marker_rope, lw=linewidth_rope, 
                color=color_rope, alpha=0.5, label='Rope')
tail, = ax.plot([], [], [],
                marker_tail, lw=linewidth_tail, 
                color=color_tail, alpha=0.5, label='Tail')    # Add a tail for the pendulum animation
time_text = ax.text2D(0.05, 0.95, '', transform=ax.transAxes) # Add a text object for displaying time

# Animation update function
def update(frame):
    """Update the pendulum animation for the current frame.
    
    Args:
        frame (int): The current frame number.

    Returns:
        pendulum, rope, tail (tuple): A tuple of the updated Line3D objects.
    """
    # Pendulum
    pendulum.set_data(x[frame], y[frame])
    pendulum.set_3d_properties(z[frame])

    # Rope
    rope.set_data(np.array([0, x[frame]]), np.array([0, y[frame]]))
    rope.set_3d_properties(np.array([0, z[frame]]))

    # Tail
    long_tail = 100
    if frame > 0 and frame < long_tail:
        tail.set_data(x[:frame-1], y[:frame-1])  # Update the tail
        tail.set_3d_properties(z[:frame-1])

    else:
        tail.set_data(x[frame-long_tail:frame-1], y[frame-long_tail:frame-1])  # Update the tail
        tail.set_3d_properties(z[frame-long_tail:frame-1])

    # Display time on the plot
    time_text.set_text('Time: {:.2f} s'.format(t[frame]))

    return pendulum, rope, tail, time_text,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(t), interval=1, blit=True)
# Add a legend
ax.legend()

# Show the animation
plt.show()