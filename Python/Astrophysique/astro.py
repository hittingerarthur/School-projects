import math

# Constants
G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

# Masses in kg
mass_sun = 2e30
mass_earth = 6e24
mass_moon = 7.4e22

# Radii in meters
radius_sun = 700_000 * 1e3
radius_earth = 6_400 * 1e3
radius_moon = 1_700 * 1e3

# Distance from Sun to Earth in meters
distance_sun_earth = 149 * 1e9

# Function to calculate escape velocity
def escape_velocity(mass, radius):
    return math.sqrt(2 * G * mass / radius) / 1e3  # Convert to km/s

# Calculate escape velocities
esc_vel_sun = escape_velocity(mass_sun, radius_sun)
esc_vel_earth = escape_velocity(mass_earth, radius_earth)
esc_vel_moon = escape_velocity(mass_moon, radius_moon)
esc_vel_sun_from_earth_orbit = escape_velocity(mass_sun, distance_sun_earth)

esc_vel_sun, esc_vel_earth, esc_vel_moon, esc_vel_sun_from_earth_orbit

print('sun=',esc_vel_sun, 'earth=', esc_vel_earth, 'moon=',esc_vel_moon, 'sun from earth=', esc_vel_sun_from_earth_orbit)

# Calculate Earth's orbital velocity
earth_orbital_velocity = math.sqrt(G * mass_sun / distance_sun_earth) / 1e3  # Convert to km/s
earth_orbital_velocity

print(earth_orbital_velocity)