from io import BytesIO

from django.core.files.base import ContentFile
from moviepy import VideoFileClip
from PIL import Image
import random

from . import models


def generate_preview(video_instance):
    file_clip = VideoFileClip(video_instance.video.path)
    preview_begin = file_clip.duration * 0.2
    preview_end = file_clip.duration * 0.8
    preview_time = random.uniform(preview_begin, preview_end)
    preview_frame = file_clip.get_frame(preview_time)
    preview_image = Image.fromarray(preview_frame)
    image_bytes = BytesIO()
    preview_image.save(image_bytes, format="JPEG")
    video_instance.preview.save(
        models.video_preview_upload_to(video_instance, "preview.jpeg"),
        ContentFile(image_bytes.getvalue()),
    )
