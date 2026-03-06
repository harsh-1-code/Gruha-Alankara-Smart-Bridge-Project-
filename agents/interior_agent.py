"""
Gruha Alankara - Interior Design AI Agent
Activity 4.2: Unified AI design generation pipeline.

Orchestrates all tool modules to produce a complete, structured
design recommendation from a single room image and user preferences.
"""

import os
import hashlib
import logging

from tools.room_analyzer import RoomAnalyzer
from tools.style_suggester import StyleSuggester
from tools.furniture_optimizer import FurnitureOptimizer
from tools.budget_planner import BudgetPlanner
from tools.design_catalog import DesignCatalog
from tools.image_generator import ImageGenerator

logger = logging.getLogger(__name__)


class InteriorDesignAgent:
    """
    AI agent that orchestrates interior design recommendations.

    Pipeline:
      1. Image preprocessing & validation
      2. Room analysis (dimensions, colors, lighting)
      3. Style suggestion (palette, materials, characteristics)
      4. Furniture optimization (items, quantities, priorities)
      5. Budget planning (category-level allocation)
      6. Catalog matching (real products from the catalog)
      7. AI image generation (visual preview of the design)
      8. Design story (natural-language explanation)
    """

    def __init__(self):
        # ── Initialize all tool modules ──
        self.room_analyzer = RoomAnalyzer()
        self.style_suggester = StyleSuggester()
        self.furniture_optimizer = FurnitureOptimizer()
        self.budget_planner = BudgetPlanner()
        self.design_catalog = DesignCatalog()
        self.image_generator = ImageGenerator()

        # ── Simple in-memory cache ──
        self._cache = {}

    # ──────────────────────────────────────────
    # Main Pipeline
    # ──────────────────────────────────────────
    def generate_design(
        self,
        image_path: str,
        style_theme: str,
        budget: float,
        room_type: str
    ) -> dict:
        """
        Run the full AI design generation pipeline.

        Args:
            image_path:   Path to the uploaded room image.
            style_theme:  User-selected style (e.g. "modern", "rustic").
            budget:       Maximum budget in USD.
            room_type:    Type of room (e.g. "living_room", "bedroom").

        Returns:
            Structured dict with room analysis, style details,
            furniture recommendations, budget plan, catalog matches,
            generated image path, and a design story narrative.
        """

        # ── 11. Check cache first ──
        cache_key = self._build_cache_key(image_path, style_theme, budget, room_type)
        if cache_key in self._cache:
            logger.info("Returning cached design for key %s", cache_key)
            return self._cache[cache_key]

        try:
            # ── 2. Image preprocessing ──
            validated_path = self._preprocess_image(image_path)

            # ── 3. Room analysis ──
            room_analysis = self._analyze_room(validated_path)

            # ── 4. Style suggestions ──
            style_details = self._get_style_details(style_theme)

            # ── 5. Furniture optimization ──
            furniture_plan = self._optimize_furniture(
                room_analysis, style_details, room_type, budget
            )

            # ── 6. Budget planning ──
            budget_plan = self._plan_budget(budget, furniture_plan)

            # ── 7. Catalog matching ──
            catalog_matches = self._match_catalog(furniture_plan, style_theme, budget)

            # ── 8. AI image generation ──
            generated_image = self._generate_design_image(
                validated_path, style_theme, room_type
            )

            # ── 9. Build structured output ──
            design_story = self._compose_design_story(
                room_type, style_theme, budget,
                room_analysis, style_details, furniture_plan
            )

            result = {
                "status": "success",
                "room_analysis": room_analysis,
                "style": style_details,
                "furniture_recommendations": furniture_plan,
                "budget_plan": budget_plan,
                "catalog_matches": catalog_matches,
                "generated_design_image": generated_image,
                "design_story": design_story
            }

            # Store in cache
            self._cache[cache_key] = result
            return result

        except FileNotFoundError as e:
            logger.error("Image not found: %s", e)
            return self._error_response(f"Image not found: {e}")

        except ValueError as e:
            logger.error("Validation error: %s", e)
            return self._error_response(f"Validation error: {e}")

        except Exception as e:
            logger.error("AI generation failed: %s", e, exc_info=True)
            return self._error_response(f"AI generation failed: {e}")

    # ──────────────────────────────────────────
    # 2. Image Preprocessing
    # ──────────────────────────────────────────
    def _preprocess_image(self, image_path: str) -> str:
        """
        Validate and normalize the image path.
        Optionally resize the image for faster processing.
        """
        # Normalize the path
        normalized = os.path.normpath(image_path)

        # Verify the file exists
        if not os.path.isfile(normalized):
            raise FileNotFoundError(f"Image file does not exist: {normalized}")

        # Validate the file extension
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
        ext = os.path.splitext(normalized)[1].lower()
        if ext not in valid_extensions:
            raise ValueError(
                f"Unsupported image format '{ext}'. "
                f"Allowed: {', '.join(valid_extensions)}"
            )

        # Optionally resize to speed up analysis
        try:
            self.image_generator.resize_image(normalized, max_size=(1280, 1280))
        except Exception as e:
            logger.warning("Image resize skipped: %s", e)

        return normalized

    # ──────────────────────────────────────────
    # 3. Room Analysis
    # ──────────────────────────────────────────
    def _analyze_room(self, image_path: str) -> dict:
        """Analyze the room image for dimensions, colors, lighting."""
        try:
            room_features = self.room_analyzer.analyze(image_path)
            return room_features
        except Exception as e:
            logger.warning("Room analysis failed, using defaults: %s", e)
            return {
                "image_path": image_path,
                "room_type": "unknown",
                "dominant_colors": [],
                "detected_furniture": [],
                "lighting": {"type": "natural", "intensity": "medium"},
                "style": "modern"
            }

    # ──────────────────────────────────────────
    # 4. Style Suggestions
    # ──────────────────────────────────────────
    def _get_style_details(self, style_theme: str) -> dict:
        """Retrieve detailed style info including palette and materials."""
        try:
            style_details = self.style_suggester.get_style_details(style_theme)
            return style_details
        except Exception as e:
            logger.warning("Style suggestion failed, using defaults: %s", e)
            return {
                "name": style_theme,
                "description": f"A {style_theme} interior design style.",
                "color_palette": [],
                "key_elements": [],
                "furniture_types": [],
                "example_images": []
            }

    # ──────────────────────────────────────────
    # 5. Furniture Optimization
    # ──────────────────────────────────────────
    def _optimize_furniture(
        self,
        room_analysis: dict,
        style_details: dict,
        room_type: str,
        budget: float
    ) -> list:
        """
        Determine optimal furniture selection using room analysis,
        style preferences, and budget constraints.
        """
        try:
            # Use the optimizer's suggest_furniture method
            furniture_plan = self.furniture_optimizer.suggest_furniture(
                style=style_details.get("name", "modern"),
                room_type=room_type,
                budget=budget
            )

            # If no results, build a sensible default plan
            if not furniture_plan:
                furniture_plan = self._default_furniture_plan(room_type)

            return furniture_plan

        except Exception as e:
            logger.warning("Furniture optimization failed: %s", e)
            return self._default_furniture_plan(room_type)

    def _default_furniture_plan(self, room_type: str) -> list:
        """Provide default furniture recommendations by room type."""
        defaults = {
            "living_room": [
                {"item": "sofa", "quantity": 1, "priority": "high"},
                {"item": "coffee_table", "quantity": 1, "priority": "medium"},
                {"item": "bookshelf", "quantity": 1, "priority": "low"},
                {"item": "floor_lamp", "quantity": 2, "priority": "medium"},
            ],
            "bedroom": [
                {"item": "bed", "quantity": 1, "priority": "high"},
                {"item": "nightstand", "quantity": 2, "priority": "medium"},
                {"item": "wardrobe", "quantity": 1, "priority": "high"},
                {"item": "dresser", "quantity": 1, "priority": "low"},
            ],
            "kitchen": [
                {"item": "dining_table", "quantity": 1, "priority": "high"},
                {"item": "dining_chair", "quantity": 4, "priority": "high"},
                {"item": "kitchen_island", "quantity": 1, "priority": "medium"},
            ],
            "office": [
                {"item": "desk", "quantity": 1, "priority": "high"},
                {"item": "office_chair", "quantity": 1, "priority": "high"},
                {"item": "bookshelf", "quantity": 1, "priority": "medium"},
                {"item": "desk_lamp", "quantity": 1, "priority": "medium"},
            ],
        }
        return defaults.get(room_type, defaults["living_room"])

    # ──────────────────────────────────────────
    # 6. Budget Planning
    # ──────────────────────────────────────────
    def _plan_budget(self, budget: float, furniture_plan: list) -> dict:
        """Allocate the total budget across design categories."""
        try:
            allocation = self.budget_planner.allocate_budget(budget)

            # Estimate cost of recommended furniture
            estimated_cost = self.budget_planner.estimate_cost(
                [{"price": budget * 0.05} for item in furniture_plan]
            )

            allocation["estimated_furniture_cost"] = round(estimated_cost, 2)
            allocation["remaining"] = round(budget - estimated_cost, 2)
            allocation["total_budget"] = budget

            return allocation

        except Exception as e:
            logger.warning("Budget planning failed: %s", e)
            return {
                "total_budget": budget,
                "furniture": round(budget * 0.40, 2),
                "lighting": round(budget * 0.15, 2),
                "decor": round(budget * 0.20, 2),
                "flooring": round(budget * 0.15, 2),
                "paint": round(budget * 0.10, 2),
            }

    # ──────────────────────────────────────────
    # 7. Design Catalog Matching
    # ──────────────────────────────────────────
    def _match_catalog(
        self,
        furniture_plan: list,
        style_theme: str,
        budget: float
    ) -> list:
        """
        Match recommended furniture with real catalog entries
        filtered by style and budget.
        """
        try:
            # Get catalog items matching the style
            style_matches = self.design_catalog.get_items_by_style(style_theme)

            # Also filter by budget
            budget_matches = self.design_catalog.get_items_by_budget(budget)

            # Combine unique matches
            seen_ids = set()
            combined = []
            for item in style_matches + budget_matches:
                item_id = item.get('id')
                if item_id not in seen_ids:
                    seen_ids.add(item_id)
                    combined.append({
                        "name": item.get("name", ""),
                        "price": item.get("price", 0),
                        "image_url": item.get("image_url", ""),
                        "category": item.get("category", ""),
                        "style": item.get("style", "")
                    })

            return combined

        except Exception as e:
            logger.warning("Catalog matching failed: %s", e)
            return []

    # ──────────────────────────────────────────
    # 8. AI Image Generation
    # ──────────────────────────────────────────
    def _generate_design_image(
        self,
        image_path: str,
        style_theme: str,
        room_type: str
    ) -> str:
        """
        Generate a visual preview of the designed room.
        Returns the file path or URL of the generated image.
        """
        try:
            generated_path = self.image_generator.generate_design_preview(
                style=style_theme,
                room_type=room_type
            )
            return generated_path if generated_path else ""

        except Exception as e:
            logger.warning("Image generation failed: %s", e)
            return ""

    # ──────────────────────────────────────────
    # 9. Design Story Narrative
    # ──────────────────────────────────────────
    def _compose_design_story(
        self,
        room_type: str,
        style_theme: str,
        budget: float,
        room_analysis: dict,
        style_details: dict,
        furniture_plan: list
    ) -> str:
        """
        Generate a natural-language explanation of the design decisions.
        """
        # Build a human-readable furniture list
        furniture_names = [
            f"{item.get('quantity', 1)}x {item.get('item', 'item')}"
            for item in furniture_plan
        ]
        furniture_text = ", ".join(furniture_names) if furniture_names else "various furniture items"

        # Extract lighting info
        lighting = room_analysis.get("lighting", {})
        lighting_desc = f"{lighting.get('intensity', 'moderate')} {lighting.get('type', 'natural')} lighting"

        # Colors detected
        colors = room_analysis.get("dominant_colors", [])
        color_text = ", ".join(colors[:3]) if colors else "neutral tones"

        story = (
            f"For your {room_type.replace('_', ' ')}, we've crafted a "
            f"{style_theme} design within a ${budget:,.0f} budget. "
            f"The room features {lighting_desc} and dominant colors of {color_text}. "
            f"We recommend furnishing the space with {furniture_text}. "
            f"The {style_theme} style emphasizes "
            f"{style_details.get('description', 'clean lines and thoughtful layouts')}, "
            f"creating a cohesive and inviting atmosphere."
        )

        return story

    # ──────────────────────────────────────────
    # 10. Error Handling Helper
    # ──────────────────────────────────────────
    @staticmethod
    def _error_response(message: str) -> dict:
        """Return a structured error response."""
        return {
            "status": "error",
            "message": message
        }

    # ──────────────────────────────────────────
    # 11. Cache Key Builder
    # ──────────────────────────────────────────
    @staticmethod
    def _build_cache_key(
        image_path: str,
        style_theme: str,
        budget: float,
        room_type: str
    ) -> str:
        """Generate a deterministic hash key for caching."""
        raw = f"{image_path}|{style_theme}|{budget}|{room_type}"
        return hashlib.md5(raw.encode()).hexdigest()

    # ──────────────────────────────────────────
    # Legacy Methods (kept for backward compatibility)
    # ──────────────────────────────────────────
    def get_design_suggestions(self, room_type: str, style: str, budget: float) -> dict:
        """Generate quick design suggestions without a room image."""
        style_details = self._get_style_details(style)
        furniture_plan = self._optimize_furniture({}, style_details, room_type, budget)
        budget_plan = self._plan_budget(budget, furniture_plan)

        return {
            "room_type": room_type,
            "style": style_details,
            "budget_plan": budget_plan,
            "furniture_recommendations": furniture_plan,
            "design_story": self._compose_design_story(
                room_type, style, budget, {}, style_details, furniture_plan
            )
        }

    def analyze_room_image(self, image_path: str) -> dict:
        """Analyze a room image and provide design recommendations."""
        try:
            validated = self._preprocess_image(image_path)
            analysis = self._analyze_room(validated)
            return {
                "image_path": image_path,
                "analysis": analysis,
                "detected_elements": analysis.get("detected_furniture", []),
                "recommendations": []
            }
        except Exception as e:
            return self._error_response(str(e))
