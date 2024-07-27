import re
from rest_framework import serializers

import re
from rest_framework import serializers


def validate_urls(value):
    youtube_pattern = r'https?://(www\.)?youtube\.com/.*|https?://(www\.)?youtu\.be/.*'

    if not re.match(youtube_pattern, value):
        raise serializers.ValidationError(
            f"Недопустимая ссылка: {value}. Разрешены только ссылки на youtube.com."
        )

    return value
