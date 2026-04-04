def filter_response(data: dict, fields: list[str]) -> dict:
    """
    Filters a car/variant response dict to only include requested fields.
    Always keeps 'model' or 'name' for context.
    """
    if not fields or not data:
        return data

    keep = set(fields) | {"model", "name"}  # always keep identifier
    return {k: v for k, v in data.items() if k in keep}


COLOR_MAP = {
    # Whites
    "pearl arctic white": "White",
    "arctic white": "White",
    "pearl white": "White",
    "white": "White",
    "pearl snow white": "White",           

    # Silvers
    "splendid silver": "Silver",
    "silky silver": "Silver",
    "silver": "Silver",
    "metallic premium silver": "Silver",   

    # Greys
    "grandeur grey": "Grey",
    "magma grey": "Dark Grey",
    "metallic grey": "Grey",
    "grey": "Grey",
    "metallic magma grey": "Dark Grey",    

    # Reds
    "sizzling red": "Red",
    "fiery red": "Red",
    "solid red": "Red",
    "opulent red": "Red",
    "pearl sangria red": "Red",  
    "auburn red": "Red",          

    # Khakis / Beiges / Browns
    "brave khaki": "Khaki",
    "earth gold": "Khaki",
    "golden beige": "Beige",
    "luxe beige": "Beige",
    "pearl dignity brown": "Brown",        

    # Blacks
    "bluish black": "Black",
    "midnight black": "Black",
    "solid black": "Black",
    "black": "Black",
    "pearl midnight black": "Black",       

    # Blues
    "exuberant blue": "Blue",
    "metallic blue": "Blue",
    "cerulean blue": "Blue",
    "nexa blue": "Blue",
    "blue": "Blue",                        

    # Dual Tones
    "dual tone white + black": "White with Black roof",
    "dual tone red + black": "Red with Black roof",
    "dual tone silver + black": "Silver with Black roof",
    "dual tone khaki + white": "Khaki with White roof",
    "dual tone blue + black": "Blue with Black roof",
    "dual tone grey + black": "Grey with Black roof",
}

def normalize_color(raw: str) -> str:
    """Convert marketing color name to human-readable form."""
    return COLOR_MAP.get(raw.lower().strip(), raw)  # fallback to original if not in map


def normalize_colors(colors: list[str]) -> list[str]:
    """Normalize a list of color names."""
    return [normalize_color(c) for c in colors]