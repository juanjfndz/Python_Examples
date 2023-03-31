#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
M1 = 1.989e30    # Mass of the first object (kg)
M2 = 5.972e24    # Mass of the second object (kg)


def equations_of_motion(t, y):
    r = np.sqrt((y[0] - y[4])**2 + (y[2] - y[6])**2)
    dy_dt = [
        y[1],
        -G * M2 * (y[0] - y[4]) / r**3,
        y[3],
        -G * M2 * (y[2] - y[6]) / r**3,
        y[5],
        G * M1 * (y[0] - y[4]) / r**3,
        y[7],
        G * M1 * (y[2] - y[6]) / r**3
    ]
    return dy_dt


def initial_conditions():
    x1, vx1, y1, vy1 = 0, 0, 0, 0
    x2, vx2, y2, vy2 = 1.496e11, 0, 0, 29.29e3
    return [x1, vx1, y1, vy1, x2, vx2, y2, vy2]


def time_settings():
    t_span = (0, 1e7)
    t_eval = np.linspace(t_span[0], t_span[1], 1000)
    return t_span, t_eval


def solve_system(t_span, initial_conditions, t_eval):
    solution = solve_ivp(equations_of_motion, t_span, initial_conditions, 
                         method='RK45', t_eval=t_eval)
    return solution


def setup_plot():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-1.5e11, 1.5e11)
    ax.set_ylim(-1.5e11, 1.5e11)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis='both', which='both', length=0)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    return fig, ax


def init():
    object1.set_data([], [])
    object2.set_data([], [])
    time_label.set_text('')
    return object1, object2, time_label,


def update(frame):
    object1.set_data(solution.y[0, frame], solution.y[2, frame])
    object2.set_data(solution.y[4, frame], solution.y[6, frame])
    time_label.set_text(f'Time: {t_eval[frame]:.1e} s')
    return object1, object2, time_label,


# Set initial conditions and time settings
initial_conds = initial_conditions()
t_span, t_eval = time_settings()

# Solve the system
solution = solve_system(t_span, initial_conds, t_eval)

# Set up the plot
fig, ax = setup_plot()
# set the figure size
fig.set_figwidth(8)  # set the width to 8 inches
fig.set_figheight(6)  # set the height to 6 inches

object1, = ax.plot([], [], 'ro', markersize=10)
object2, = ax.plot([], [], 'bo', markersize=5)
time_label = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Create the animation
ani = FuncAnimation(fig, update, frames=len(t_eval), interval=1, init_func=init, blit=True)

# Show the plot
plt.show()