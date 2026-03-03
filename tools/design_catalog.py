class DesignCatalog:
    """Tool for managing and browsing the interior design catalog."""

    def __init__(self):
        self.catalog_items = []

    def get_all_items(self, filters: dict = None) -> list:
        """Retrieve all catalog items, optionally filtered."""
        return self.catalog_items

    def get_item_by_id(self, item_id: int) -> dict:
        """Retrieve a catalog item by its ID."""
        for item in self.catalog_items:
            if item.get('id') == item_id:
                return item
        return {}

    def search_items(self, query: str) -> list:
        """Search catalog items by name, style, or category."""
        query = query.lower()
        return [
            item for item in self.catalog_items
            if query in item.get('name', '').lower()
            or query in item.get('style', '').lower()
            or query in item.get('category', '').lower()
        ]

    def get_items_by_style(self, style: str) -> list:
        """Get all catalog items matching a specific style."""
        return [
            item for item in self.catalog_items
            if item.get('style', '').lower() == style.lower()
        ]

    def get_items_by_budget(self, max_price: float) -> list:
        """Get catalog items within a given budget."""
        return [
            item for item in self.catalog_items
            if item.get('price', 0) <= max_price
        ]
