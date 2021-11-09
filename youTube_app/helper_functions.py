import string
import random
from youTube_app.models import VidData


# Generates a random 16char string of nums and letters for
# password reset url sent to the user after request is submitted
def string_generator():
    length = 16
    letters = string.ascii_lowercase
    numbers = string.digits
    url_snippet = ''.join(
        random.choice(letters + numbers) for i in range(length))
    return url_snippet


# Gets the VidData objects for display purposes
# takes in num_thumbs return only the desired amount of thumbnails
def thumbs_for_display(num_thumbs):
    thumb_list = []
    get_thumbs = VidData.objects.all()
    for thumb in get_thumbs:
        thumb_list.append((thumb.thumb, thumb.title))

    thumb_list.reverse()
    return thumb_list[:num_thumbs]
