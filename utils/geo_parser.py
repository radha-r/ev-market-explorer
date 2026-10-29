import re


def extract_coordinates(point_text):
    if point_text is None:
        return None, None

    match = re.search(
        r"POINT\s+\(([-\d.]+)\s+([-\d.]+)\)",
        str(point_text)
    )

    if not match:
        return None, None

    longitude = float(match.group(1))
    latitude = float(match.group(2))

    return latitude, longitude