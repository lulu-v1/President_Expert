from PIL import Image, ImageTk

from PIL import Image, ImageTk

def load_and_resize_background(image_path, canvas_width, canvas_height):
    table_image = Image.open(image_path)
    # Redimensionar imagen de fondo para que sea un poco más pequeña que el tamaño del Canvas
    new_width = int(canvas_width * 1)
    new_height = int(canvas_height * 1)
    table_image = table_image.resize((new_width, new_height), Image.LANCZOS)
    table_photo = ImageTk.PhotoImage(table_image)
    return table_photo, new_width, new_height

