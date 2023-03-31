#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# Constants
G = 6.67430e-11  # Gravitational constant (m^3/kg/s^2)
c = 3.0e8  # Speed of light (m/s)
M1 = 1.989e30    # Mass of the first object (kg)
M2 = 5.972e24    # Mass of the second object (kg)

def equations_of_motion_1PN(t, y):
    y = np.array(y)
    pos1 = y[[0, 2, 4]]
    vel1 = y[[1, 3, 5]]
    pos2 = y[[6, 8, 10]]
    vel2 = y[[7, 9, 11]]

    r_vector = pos1 - pos2
    r = np.linalg.norm(r_vector)

    # Newtonian acceleration
    acceleration1_newtonian = -G * M2 * r_vector / r**3
    acceleration2_newtonian = G * M1 * r_vector / r**3

    # 1PN correction term
    vel_squared_sum = np.sum(vel1**2) + np.sum(vel2**2)
    vel_dot_r = np.dot(vel1, r_vector) - np.dot(vel2, r_vector)
    acceleration1_1PN = G * M2 / (c**2 * r**3) * (
        (4 * G * M1 / r - vel_squared_sum) * r_vector - 2 * vel_dot_r * vel1)
    acceleration2_1PN = G * M1 / (c**2 * r**3) * (
        (4 * G * M2 / r - vel_squared_sum) * r_vector + 2 * vel_dot_r * vel2)

    # Combine the Newtonian acceleration and 1PN correction terms
    acceleration1 = acceleration1_newtonian + acceleration1_1PN
    acceleration2 = acceleration2_newtonian + acceleration2_1PN

    dy_dt = np.empty_like(y)
    dy_dt[[0, 2, 4]] = vel1
    dy_dt[[1, 3, 5]] = acceleration1
    dy_dt[[6, 8, 10]] = vel2
    dy_dt[[7, 9, 11]] = acceleration2

    return dy_dt


def initial_conditions():
    x1, vx1, y1, vy1, z1, vz1 = 0, 0, 0, 0, 0, 0
    x2, vx2, y2, vy2, z2, vz2 = 1.496e11, 0, 0, 29.29e3, 0, 0
    return [x1, vx1, y1, vy1, z1, vz1, x2, vx2, y2, vy2, z2, vz2]


def time_settings():
    t_span = (0, 1e8)
    t_eval = np.linspace(t_span[0], t_span[1], int(1e4))
    return t_span, t_eval


def solve_system(t_span, initial_conditions, t_eval, eq_motion):
    solution = solve_ivp(eq_motion, t_span, initial_conditions, 
                         method='RK45', t_eval=t_eval)
    return solution


def animate_solution(solution):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x1, y1, z1 = solution.y[0], solution.y[2], solution.y[4]
    x2, y2, z2 = solution.y[6], solution.y[8], solution.y[10]

    point1, = ax.plot([], [], [], 'ro', label='M1', markersize=10)
    point2, = ax.plot([], [], [], 'bo', label='M2', markersize=8)

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')

    ax.set_xlim(np.min([x1, x2]), np.max([x1, x2]))
    ax.set_ylim(np.min([y1, y2]), np.max([y1, y2]))
    ax.set_zlim(np.min([z1, z2]), np.max([z1, z2]))

    ax.legend()

    def init():
        point1.set_data_3d([], [], [])
        point2.set_data_3d([], [], [])
        return point1, point2

    def update(frame):
        point1.set_data_3d(x1[frame], y1[frame], z1[frame])
        point2.set_data_3d(x2[frame], y2[frame], z2[frame])
        return point1, point2

    ani = FuncAnimation(fig, update, frames=range(len(x1)), interval=1, init_func=init, blit=True)
    plt.show()

t_span, t_eval = time_settings()
initial_values = initial_conditions()
solution = solve_system(t_span, initial_values, t_eval, equations_of_motion_1PN)
animate_solution(solution)