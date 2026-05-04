from pathlib import Path

BASE_PATH = Path(__file__).parents[1]

ASSETS_PATH = BASE_PATH / "assets"
COMPONENTS_PATH = BASE_PATH / "components"

IMAGE_PATH = ASSETS_PATH / "image"
STYLES_PATH = ASSETS_PATH / "style"
MARKDOWN_PATH = ASSETS_PATH / "markdown"
DATA_PATH = ASSETS_PATH / "data"


COLORS = {
    "gray_1":     "#CCCCCC",
    "gray_2":     "#888888",
    "gray_3":     "#444444",
    "blue_dark":  "#2E4057",
    "gray_light": "#D5D8DC",
    "pink":       "#FF6666",
    "purple_1":   "#777DA7",
    "purple_2":   "#1F0322",
}