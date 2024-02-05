import pygame
import pygame_gui
import random
import math

# Set screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1200                        # Screen dimensions

# Star Min Max
MIN_STAR_COUNT = 10                                             # Minimum star count
MAX_STAR_COUNT = 3000                                           # Maximum star count

# Star speed constraints
MIN_INITIAL_STAR_SPEED = 0.1                                    # Minimum starting speed of star
MAX_INITIAL_STAR_SPEED = 2.0                                    # Maximum starting speed of star

# Star acceleration percentage
MIN_ACCEL_PERCENTAGE = 0                                        # Minimum acceleration percentage to apply on each render
MAX_ACCEL_PERCENTAGE = 100                                      # Maximum acceleration percentage to apply on each render



# Default values
DEFAULT_STAR_COUNT = 100                                        # Defaul start count
DEFAULT_MAX_STAR_TAIL_LENGTH = 20                               # default maximum tail length when parallax motion enabled
DEFAULT_CREATE_STARS_ON_MOUSE = False                           # Default create on mouse toggle
DEFAULT_ACCEL_PERCENTAGE = 10                                   # Default acceleration percentage
DEFAULT_PARALLAX_ENALBED = False                                # Default parallax motion blur setting
DEFAULT_PARALLAX_SLIDER_VALUE = 5                               # Default int to divide by for parallax motion blur distance
DEFAULT_PARALLAX_MOTION_START_DISTANCE = math.sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) / DEFAULT_PARALLAX_SLIDER_VALUE      # For calculating parallax vision effect

# Start colors
BLACK = (0, 0, 0)
RAND_COLOR = (int(random.randint(0, 255)), random.randint(0, 255), random.randint(0, 255)) # generates a random color for every run

# Center of screen (origin)
CENTER_X, CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2      # Ref to the center of the screen for determining origin



# Initialize Pygame and Pygame GUI
pygame.init()                                                   # Initialize pygame
pygame.display.set_caption("Star Travel Simulation")            # Set window caption
clock = pygame.time.Clock()                                     # Define clock for controlling frame rate

# Set screen and GUI manager dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))



# UI Components

## Star Count Slider

### Slider bar for adjusting star counts
star_count_slider = pygame_gui.elements.UIHorizontalSlider( relative_rect=pygame.Rect((5, 30), (150, 20)),
                                                     start_value=DEFAULT_STAR_COUNT,
                                                     value_range=(MIN_STAR_COUNT, MAX_STAR_COUNT),
                                                     manager=manager)

### Label for the star count slider
star_count_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5, 5), (100, 20)),
                                               text='Star Count:',
                                               manager=manager)

### Display the current value of star_count
star_count_value_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 5), (50, 20)),
                                                       text=str(DEFAULT_STAR_COUNT),
                                                       manager=manager)



## Star Acceleration Slider

### Slider bar for adjusting star acceleration over time
star_acceleration_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((5, 85), (150, 20)),
                                                                  start_value=DEFAULT_ACCEL_PERCENTAGE,
                                                                  value_range=(0, 100),
                                                                  manager=manager)

### Label for the star acceleration slider
star_acceleration_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5, 60), (100, 20)),
                                                      text="Accel (%):",
                                                      manager=manager)

### Display the current value of STAR_ACCELERATION
star_acceleration_value_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 60), (50, 20)),
                                                              text=str(DEFAULT_ACCEL_PERCENTAGE),
                                                              manager=manager)


## Parallax motion blur slider

### Slider for adjusting parallax start distance
parallax_motion_distance_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((5, 220), (150, 20)),
                                                                  start_value=DEFAULT_PARALLAX_SLIDER_VALUE,
                                                                  value_range=(1, 75),
                                                                  manager=manager)

### Label for parallax start distance
parallax_motion_distance_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5, 200), (100, 20)),
                                                      text="Parallax:",
                                                      manager=manager)

### Display the current value of parallax motion distance
parallax_motion_distance_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 200), (50, 20)),
                                                              text=str(DEFAULT_PARALLAX_SLIDER_VALUE),
                                                              manager=manager)


## Star tail length slider

### Slider for adjusting parallax blur distance
star_tail_length_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((5, 265), (150, 20)),
                                                                  start_value=DEFAULT_MAX_STAR_TAIL_LENGTH,
                                                                  value_range=(1, 100),
                                                                  manager=manager)

### Label for parallax blur distance
star_tail_length_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5, 245), (100, 20)),
                                                      text="Tail Len:",
                                                      manager=manager)

### Display the current value of parallax blur distance
star_tail_length_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 245), (50, 20)),
                                                              text=str(DEFAULT_MAX_STAR_TAIL_LENGTH),
                                                              manager=manager)

## Create star on mouse button

# Button for toggling star creation at mouse location
create_stars_on_mouse_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5, 120), (150, 30)),
                                                            text="On Mouse: OFF",
                                                            manager=manager)

# Button for toggling parallax motion blur
enable_parallax_motion_blur_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5, 165), (150, 30)),
                                                           text="Parallax: OFF",
                                                           manager=manager)



# Gets a new start at the origin location
def get_star(origin):
    x, y = origin
    angle = random.uniform(0, 2 * math.pi)
    speed = random.uniform(MIN_INITIAL_STAR_SPEED, MAX_INITIAL_STAR_SPEED)
    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed
    return [x, y, vx, vy]

# Function to create stars with positions and velocities
def create_stars(star_arr, num_stars):
    star_arr.clear()
    for _ in range(num_stars):
        x = CENTER_X #+ random.uniform(-10, 10)              # Adding a small random variation to the start position
        y = CENTER_Y #+ random.uniform(-10, 10)
        star_arr.append(get_star((x, y)))

# Function to update stars based on mouse position or center of screen
def update_stars(star_arr, star_accel, origin):
    for star in star_arr:
        # Update star position based on velocity
        star[0] += star[2]
        star[1] += star[3]

        # Apply acceleration to velocity
        star[2] *= 1.0 + star_accel / 1000
        star[3] *= 1.0 + star_accel / 1000
        
        # If star moves off-screen, get a new star at origin
        if star[0] < 0 or star[0] > SCREEN_WIDTH or star[1] < 0 or star[1] > SCREEN_HEIGHT:
            # get a new star and update the stars list in place
            new_star = get_star(origin)
            star[:] = new_star

# Function to draw stars
def draw_stars(stars, enable_parallax_motion_blur, parallax_motion_distance, max_tail_len, tail_opacity):
    for star in stars:
        # Star properties
        x, y, vx, vy = star

        # Draw the star
        pygame.draw.circle(screen, RAND_COLOR, (int(x), int(y)), 1)

        # Get star's distance from origin
        distance_from_center = math.sqrt((x - CENTER_X)**2 + (y - CENTER_Y)**2)

        if enable_parallax_motion_blur and distance_from_center >= parallax_motion_distance:
            # Tail properties based on velocity
            velocity = math.sqrt(vx**2 + vy**2)
            tail_length = min(velocity * 5, max_tail_len)
        
            # Calculate tail end position
            tail_end_x = x - (vx / velocity) * tail_length
            tail_end_y = y - (vy / velocity) * tail_length
        
            # Create a transparent surface
            # tail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

            # Draw the tail
            pygame.draw.line(screen, RAND_COLOR, (int(x), int(y)), (int(tail_end_x), int(tail_end_y)), 1)

            # Draw the tail on the transparent surface with the desired opacity
            #pygame.draw.line(tail_surface, (*RAND_COLOR, tail_opacity), (int(x), int(y)), (int(tail_end_x), int(tail_end_y)), 1)

            # Blit the transparent surface onto the main screen
            #screen.blit(tail_surface, (0, 0))


# Main loop
def main():
    star_count = DEFAULT_STAR_COUNT
    star_accel = DEFAULT_ACCEL_PERCENTAGE
    create_stars_on_mouse = DEFAULT_CREATE_STARS_ON_MOUSE
    enable_parallax_motion_blur = DEFAULT_PARALLAX_ENALBED
    parallax_motion_distance = DEFAULT_PARALLAX_MOTION_START_DISTANCE
    parallax_slider_value = DEFAULT_PARALLAX_SLIDER_VALUE
    max_tail_len = DEFAULT_MAX_STAR_TAIL_LENGTH
    stars = []
    
    create_stars(stars, star_count)

    running = True
    while running:
        time_delta = clock.tick(100)/1000.0     # Adjust to your desired fram rate

        # Event hanlding loop for sliders and buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                # Star Count slider event
                if event.ui_element == star_count_slider:
                    star_count = int(star_count_slider.get_current_value())
                    star_count_value_display.set_text(str(star_count))
                    create_stars(stars, star_count)

                # Star acceleration slider event
                if event.ui_element == star_acceleration_slider:
                    star_accel = star_acceleration_slider.get_current_value()
                    star_acceleration_value_display.set_text(str(round(star_accel, 2)))

                # Parallax motion blur slider event
                if event.ui_element == parallax_motion_distance_slider:
                    parallax_slider_value = parallax_motion_distance_slider.get_current_value()
                    parallax_motion_distance_display.set_text(str(parallax_slider_value))

                # Star tail (parallax blur) length
                if event.ui_element == star_tail_length_slider:
                    max_tail_len = star_tail_length_slider.get_current_value()
                    star_tail_length_display.set_text(str(max_tail_len)) 

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                # On mouse generate stars button
                if event.ui_element == create_stars_on_mouse_button:
                    create_stars_on_mouse = not create_stars_on_mouse
                    button_text = "On Mouse: ON" if create_stars_on_mouse else "On Mouse: OFF"
                    create_stars_on_mouse_button.set_text(button_text)
                
                # Parallax motion blur toggle
                if event.ui_element == enable_parallax_motion_blur_button:
                    enable_parallax_motion_blur = not enable_parallax_motion_blur
                    button_text = "Parallax: ON" if enable_parallax_motion_blur else "Parallax: OFF"
                    enable_parallax_motion_blur_button.set_text(button_text)

            manager.process_events(event)

        mouse_pos = pygame.mouse.get_pos()
        manager.update(time_delta)

        # Clear screen and draw black
        screen.fill(BLACK)

        # Update logic based on whether create_stars_on_mouse is True
        origin = mouse_pos if create_stars_on_mouse else (CENTER_X, CENTER_Y)
        update_stars(stars, star_accel, origin)
        parallax_motion_distance = math.sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) / parallax_slider_value
        draw_stars(stars, enable_parallax_motion_blur, parallax_motion_distance, max_tail_len, 120)

        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()