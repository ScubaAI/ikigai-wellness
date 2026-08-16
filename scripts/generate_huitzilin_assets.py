from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math
import random

# ==========================================
# CONFIGURACIÓN HUITZILIN
# ==========================================
COLORS = {
    "amate": (250, 243, 224),
    "sand": (244, 228, 193),
    "clay": (210, 105, 30),
    "earth": (139, 69, 19),
    "jade": (0, 168, 107),
    "obsidian": (44, 24, 16),
    "sun": (255, 215, 0),
}


def get_root() -> Path:
    root = Path(__file__).resolve().parents[1] / "public" / "images" / "huitzilin"
    root.mkdir(parents=True, exist_ok=True)
    return root


def generate_amate_texture(path: Path):
    """Genera una textura sutil de papel amate (fibroso y cálido)"""
    width, height = 800, 800
    img = Image.new("RGB", (width, height), COLORS["amate"])
    draw = ImageDraw.Draw(img)

    for _ in range(15000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        noise_color = (
            COLORS["amate"][0] + random.randint(-8, 8),
            COLORS["amate"][1] + random.randint(-8, 8),
            COLORS["amate"][2] + random.randint(-8, 8),
        )
        draw.point((x, y), fill=noise_color)

    img = img.filter(ImageFilter.GaussianBlur(0.8))
    img.save(path, quality=85)
    print(f"✅ Generado: {path.name}")


def generate_greca_pattern(path: Path):
    """Genera un patrón de greca mesoamericana suavizado"""
    size = 200
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    pattern_color = COLORS["jade"] + (25,)
    line_width = 4

    for i in range(0, size, 40):
        draw.line([(i, 0), (i, 20), (i + 20, 20), (i + 20, 40)], fill=pattern_color, width=line_width)
        draw.line([(0, i), (20, i), (20, i + 20), (40, i + 20)], fill=pattern_color, width=line_width)

    img.save(path)
    print(f"✅ Generado: {path.name}")


def generate_sunburst(path: Path):
    """Genera un resplandor solar (Tonalli) para usar de fondo decorativo"""
    size = 600
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    num_rays = 12
    for i in range(num_rays):
        angle = (360 / num_rays) * i
        rad = math.radians(angle)
        r_inner = 50
        r_outer = 250
        spread = 15

        p1 = (cx + r_inner * math.cos(rad - spread), cy + r_inner * math.sin(rad - spread))
        p2 = (cx + r_outer * math.cos(rad), cy + r_outer * math.sin(rad))
        p3 = (cx + r_inner * math.cos(rad + spread), cy + r_inner * math.sin(rad + spread))

        ray_color = COLORS["sun"] + (40,)
        draw.polygon([p1, p2, p3], fill=ray_color)

    draw.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=COLORS["sun"] + (60,))
    img = img.filter(ImageFilter.GaussianBlur(8))
    img.save(path)
    print(f"✅ Generado: {path.name}")


def generate_hummingbird_silhouette(path: Path):
    """Genera una silueta abstracta y minimalista de un colibrí (Huitzilin)"""
    size = 400
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    body_color = COLORS["earth"] + (200,)
    wing_color = COLORS["jade"] + (150,)

    wing_points = [
        (200, 200), (150, 120), (80, 140), (120, 220), (180, 240)
    ]
    draw.polygon(wing_points, fill=wing_color)

    body_points = [
        (200, 200), (240, 190), (280, 210), (260, 250), (220, 260), (190, 240)
    ]
    draw.polygon(body_points, fill=body_color)

    draw.line([(280, 210), (340, 200)], fill=body_color, width=4)

    img = img.filter(ImageFilter.GaussianBlur(1.5))
    img.save(path)
    print(f"✅ Generado: {path.name}")


# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    root = get_root()
    print("🪶 Forjando elementos visuales HUITZILIN...\n")

    generate_amate_texture(root / "amate_texture.png")
    generate_greca_pattern(root / "greca_pattern.png")
    generate_sunburst(root / "tonalli_glow.png")
    generate_hummingbird_silhouette(root / "huitzilin_icon.png")

    print("\n✨ ¡Assets listos! Úsalos en tu HTML/CSS para dar vida al sistema.")
