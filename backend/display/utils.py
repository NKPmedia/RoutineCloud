import io
import os

import cairosvg
import yaml
from PySide6.QtGui import QFont


def get_fa_path(name, version="free-6.7.2-desktop"):
    return f"assets/icons/fontawesome-{version}/svgs/{name}.svg"

def get_fa_base_path(version="free-6.7.2-desktop"):
    return f"assets/icons/fontawesome-{version}/"

class AwesomeFontProvider:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AwesomeFontProvider, cls).__new__(cls)
        return cls._instance

    def __init__(self, font_size: int = 32):
        # Prevent re-initialization
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.categories_path = os.path.join(get_fa_base_path(), "metadata", "categories.yml")
        self.icons_path = os.path.join(get_fa_base_path(), "metadata", "icons.yml")
        self.font_paths = {
            "brands": os.path.join(get_fa_base_path(), "otfs", "Font Awesome 6 Brands-Regular-400.otf"),
            "regular": os.path.join(get_fa_base_path(), "otfs", "Font Awesome 6 Free-Regular-400.otf"),
            "solid": os.path.join(get_fa_base_path(), "otfs", "Font Awesome 6 Free-Solid-900.otf"),
        }
        self.font_size = font_size
        self.default_type = "regular"

        with open(self.categories_path, "r", encoding="utf-8") as f:
            self.categories = yaml.safe_load(f)

        with open(self.icons_path, "r", encoding="utf-8") as f:
            self.icons = yaml.safe_load(f)

        self._initialized = True  # Prevent re-init

    def get_font(self, type: str = None, font_size: int = None) -> QFont:
        type = type or self.default_type
        if type not in self.font_paths:
            raise ValueError(f"Invalid font type '{type}'. Must be one of {list(self.font_paths.keys())}.")
        font_size = font_size or self.font_size
        return QFont(self.font_paths[type], font_size)

    def get_unicode(self, icon_name: str) -> str:
        icon_data = self.icons.get(icon_name)
        if not icon_data:
            raise ValueError(f"Icon '{icon_name}' not found.")
        return chr(int(icon_data["unicode"], 16))

    def get_categories(self) -> list:
        return list(self.categories.keys())

    def get_icons_in_category(self, category_name: str) -> list:
        category = self.categories.get(category_name)
        if not category:
            raise ValueError(f"Category '{category_name}' not found.")
        return category.get("icons", [])

fa_provider = AwesomeFontProvider()

if __name__ == "__main__":

    import pyrootutils
    root = pyrootutils.setup_root(cwd=True, search_from=".")

    font_provider = AwesomeFontProvider()
    print(font_provider.get_categories())
    print(font_provider.get_icons_in_category("alert"))
    print(font_provider.get_unicode("adn"))