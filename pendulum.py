import numpy as np
import pygame

pygame.init()
display = pygame.display.set_mode((500, 500))
font = pygame.font.SysFont("monospace", 12)
ORIGIN = (250, 250)
SCALE = 100.0


def round_point((x, y)):
    '''Round and change point to centered coordinate system'''
    return map(int, ((SCALE * x) + ORIGIN[0], -(SCALE * y) + ORIGIN[1]))


def unround_point((x, y)):
    '''Change center-origin coordinates to pygame coordinates'''
    return ((x - ORIGIN[0]) / SCALE, (-y + ORIGIN[1]) / SCALE)


dt = 0.05
g = 9.81
l = 1.0
c = g / l


def dynamics(X, u):
    A = np.array([
        [1 + (0.5 * (dt**2) * c), dt],
        [c * dt, 1]
    ])
    B = np.array([
        [0.5 * (dt ** 2)],
        [dt]
    ])
    Xn = np.dot(A, X) + np.dot(B, u)
    return Xn


def real_dynamics(X, u):
    # thetadotdot = (g * l * np.sin(X[0])) + u
    # Xn = np.array([X[0] + (X[1] * dt), X[1] + (thetadotdot * (0.5 * (dt ** 2)))])
    dt2 = dt ** 2
    theta, thetadot = X
    mglsth = g * l * np.sin(theta)
    theta_n = theta + (0.5 * dt2 * mglsth) + (dt * thetadot) + (0.5 * dt2 * u)
    theta_dot_n = (mglsth * dt) + thetadot - (0.02 * thetadot) + (dt * u)
    Xn = np.array([theta_n, theta_dot_n])

    return Xn


def circle(pos):
    pygame.draw.circle(
        display,
        (255, 0, 0),
        round_point(pos),
        5
    )


def draw_pend(X):
    end = (np.sin(X[0]), np.cos(X[0]))
    circle(end)
    pygame.draw.line(display, (255, 0, 255), round_point((0.0, 0.0)), round_point(end), 4)


if __name__ == '__main__':
    clock = pygame.time.Clock()

    X0 = np.array([1.5, 0.0])

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print 'mouseclick'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit(0)
        u = 0
        if X0[0] > 1.5:
            u = -20.0
        X0 = real_dynamics(X0, u)
        print X0

        draw_pend(X0)
        center = (250, 250)
        pygame.draw.circle(display, (0, 255, 0), center, 2)
        pygame.display.update()
        clock.tick(20)
        display.fill((0, 0, 0))
