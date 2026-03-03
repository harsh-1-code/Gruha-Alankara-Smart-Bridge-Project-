class StyleSuggester:
    """Tool for suggesting interior design styles based on user preferences."""

    STYLES = [
        'modern', 'contemporary', 'minimalist', 'traditional',
        'rustic', 'industrial', 'bohemian', 'scandinavian',
        'mid-century modern', 'art deco', 'coastal', 'farmhouse'
    ]

    def __init__(self):
        pass

    def suggest_styles(self, preferences: dict) -> list:
        """Suggest design styles based on user preferences."""
        return self.STYLES[:3]

    def get_style_details(self, style: str) -> dict:
        """Get detailed information about a specific style."""
        return {
            "name": style,
            "description": f"Details about {style} interior design style.",
            "color_palette": [],
            "key_elements": [],
            "furniture_types": [],
            "example_images": []
        }

    def match_style_to_room(self, room_type: str, existing_elements: list) -> str:
        """Match the best style to a room based on existing elements."""
        return "modern"
