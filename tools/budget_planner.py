class BudgetPlanner:
    """Tool for planning and managing interior design budgets."""

    def __init__(self):
        self.budget_categories = {
            'furniture': 0.40,
            'lighting': 0.15,
            'decor': 0.20,
            'flooring': 0.15,
            'paint': 0.10,
        }

    def allocate_budget(self, total_budget: float) -> dict:
        """Allocate budget across different design categories."""
        allocation = {}
        for category, percentage in self.budget_categories.items():
            allocation[category] = round(total_budget * percentage, 2)
        return allocation

    def get_recommendations(self, budget: float, room_type: str) -> list:
        """Get budget-appropriate recommendations for a room."""
        allocation = self.allocate_budget(budget)
        return [
            {
                "category": category,
                "allocated": amount,
                "recommendations": []
            }
            for category, amount in allocation.items()
        ]

    def estimate_cost(self, items: list) -> float:
        """Estimate total cost for a list of items."""
        return sum(item.get('price', 0) for item in items)
