from PIL import Image, ImageTk
from tkinter.ttk import Style
from tkinter import Tk, Label, Button, BOTTOM
import random
import os

# Specify the folder file path
folder_path = r"C:\Users\me\Pictures"


# Create a list of image filenames
image_filenames = [os.path.join(folder_path, f) for f in os.listdir(
    folder_path) if f.endswith(('.jpg', '.png', 'jpeg'))]

# Create a copy of the original list of image filenames
original_filenames = list(image_filenames)

# Create a Tkinter window
window = Tk()
# window.configure(bg="black")
window.configure(bg="black", bd=0, highlightthickness=0)

# Set the window to appear in full screen
# window.wm_attributes("-fullscreen", 1)
fullscreen = 0

# Create a dark mode style
style = Style()
style.theme_use("clam")

# Set the background color to black
style.configure(".", background="black")

# Set the button foreground and background colors
style.configure("TButton", foreground="#ffffff", background="#000000")

# Create a Label widget to display the current image
label = Label(window, background="black", anchor="center")
label.pack(side="top")


# Create a Button widget to go to the previous image
prev_button = Button(window, text="Previous",
                     command=lambda: display_image(-1))
# prev_button.pack(side="left", fill="y")

# Create a Button widget to go to the next image
next_button = Button(window, text="Next", command=lambda: display_image(1))
# next_button.pack(side="right", fill="y")

# Create a Button widget to shuffle the images
shuffle_button = Button(window, text="Shuffle",
                        command=lambda: shuffle_images())
# shuffle_button.pack(side="bottom", fill="x")

# Create a Button widget to un-shuffle the images
unshuffle_button = Button(window, text="Un-shuffle",
                          command=lambda: unshuffle_images())
# unshuffle_button.pack(side="bottom", fill="x")

# Create a Button widget to toggle Fullscreen
fullscreen_button = Button(window, text="Fullscreen",
                           command=lambda: toggle_fullscreen())

# Create a Button widget to close the window
close_button = Button(window, text="Close", command=lambda: close_window())

# Create a Button widget to zoom the window
zoom_button = Button(window, text="Zoom", command=lambda: zoom())

# Create a Button widget to move to next or previous with left click
click_button = Button(window, text="Click",
                      command=lambda: left_click_action())


# Create a variable to keep track of the current image index
current_index = 0

# Create a variable to control the zoom factor
zoom_factor = 1.1


def left_click_action(event):
    if event.x < label.winfo_width()/2:
        display_image(-1)
    else:
        display_image(1)


def display_image(offset):
    # Calculate the new index
    global current_index
    current_index += offset
    current_index %= len(image_filenames)

    # Open the image file
    image = Image.open(image_filenames[current_index])

    # Fix transparency
    # image.putalpha(0)

    # Scale the image to fit the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    image_width, image_height = image.size
    if image_width > screen_width or image_height > screen_height:
        scale = min(screen_width / image_width,
                    screen_height / image_height) * zoom_factor
        image_width = int(image_width * scale)
        image_height = int(image_height * scale)
        image = image.resize((image_width, image_height), Image.ANTIALIAS)

    # Convert the image to a PhotoImage object
    image = ImageTk.PhotoImage(image)

    # Update the label's image
    label.config(image=image)
    label.image = image

    # Set the window title to the name of the image file
    # window.title(os.path.basename(image_filenames[current_index]))
    update_title()


def update_title():
    global zoom_factor
    zoom_str = str(int(zoom_factor*100))
    if zoom_str != 100:
        window.title(os.path.basename(
            image_filenames[current_index]) + " " + zoom_str + "%")
    else:
        window.title(os.path.basename(image_filenames[current_index]))


def shuffle_images():
    # Shuffle the list of image filenames
    global image_filenames
    random.shuffle(image_filenames)

    # Display the first image
    display_image(0)


def unshuffle_images():

    # Find the index of the current image in the original list
    global current_index
    global image_filenames
    print(current_index, image_filenames[current_index], original_filenames.index(
        image_filenames[current_index]))
    current_index = original_filenames.index(image_filenames[current_index])

    # Revert to the original list of image filenames
    image_filenames = list(original_filenames)

    # Display the current image
    display_image(0)


def toggle_fullscreen():
    global fullscreen
    global screen_width
    global screen_height

    # Toggle the full screen state
    fullscreen = not fullscreen

    # Set the window's size and position
    if fullscreen:
        # window.geometry(f"{screen_width}x{screen_height}+0+0")
        window.wm_attributes("-fullscreen", 1)
    else:
        window.geometry("1024x768")
        window.wm_attributes("-fullscreen", 0)


def close_window():
    window.destroy()


def zoom(event):
    global zoom_factor

    # Zoom in if the mouse wheel is scrolled up, otherwise zoom out
    if event.delta > 0:
        zoom_factor *= 1.1
        print(zoom_factor)
        update_title()
    else:
        zoom_factor /= 1.1
        print(zoom_factor)
        update_title()

    # Display the current image
    display_image(0)


# Bind the left and right arrow keys to the previous and next buttons
window.bind("<Left>", lambda event: prev_button.invoke())
window.bind("<Right>", lambda event: next_button.invoke())

# Bind the space bar to the toggle_fullscreen function
window.bind("<space>", lambda event: fullscreen_button.invoke())

window.bind("<Control-w>", lambda event: close_button.invoke())

window.bind("<Button-1>", lambda event: left_click_action(event))
window.bind("<Button-3>", lambda event: left_click_action(event))

# window.bind("<MouseWheel>", lambda event: zoom(event))
window.bind("<MouseWheel>", lambda event: zoom(event))

window.bind("<Up>", lambda event: shuffle_button.invoke())
window.bind("<Down>", lambda event: unshuffle_button.invoke())

# Display the first image
display_image(0)

# Run the Tkinter event loop
window.mainloop()
