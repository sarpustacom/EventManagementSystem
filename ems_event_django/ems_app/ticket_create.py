from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from . import models
import uuid as u
def create_ticket(attendee: models.AttendeeModel) -> str:
    # Load the image
    name = f"ticket_{u.uuid1()}.png"
    image_path = os.path.join(settings.MEDIA_ROOT, "uploads", "AttendeeTicket.png")
    output_path = os.path.join(settings.MEDIA_ROOT, "uploads", name)
    font_path = os.path.join(settings.BASE_DIR, "static", "ems_app", "fonts", "ArchivoBlack.ttf")
    font2_path = os.path.join(settings.BASE_DIR, "static", "ems_app", "fonts", "ArchivoNarrow.ttf")

    image = Image.open(image_path)
    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Load a font (Make sure arial.ttf exists or provide another path)
    font = ImageFont.truetype(font_path, 64)
    font2 = ImageFont.truetype(font2_path, 36)

    # Define text and position
    text = f"{attendee.name}"
    text2 = f"Event: {attendee.event.title}"
    text3 = f"Date & Time: {attendee.event.date} {attendee.event.time}"
    text4 = f"Location: {attendee.event.location}"
    position = (400, 200)  # (x, y) position of the text
    position2 = (400, 400) 
    position3 = (400, 440)  
    position4 = (400, 480)   # (x, y) position of the text
    text_color = (0, 0, 0)  # White text



    # Add text to image
    draw.text(position, text, fill=text_color, font=font)
    draw.text(position2, text2, fill=text_color, font=font2)
    draw.text(position3, text3, fill=text_color, font=font2)
    draw.text(position4, text4, fill=text_color, font=font2)

    # Save the processed image
    image.save(output_path)
    
    return f"/uploads/{name}"  # Return the saved file path

