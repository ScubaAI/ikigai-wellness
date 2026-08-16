from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "images" / "products"
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {
    "bg": (250, 243, 224),
    "sand": (244, 228, 193),
    "soul": (247, 147, 26),
    "souldeep": (194, 65, 12),
    "jade": (0, 168, 107),
    "cenote": (13, 148, 136),
    "copal": (128, 0, 128),
    "obsidian": (44, 24, 16),
    "sun": (255, 215, 0),
    "clay": (210, 105, 30),
    "white": (255, 255, 255),
}

PRODUCTS = [
    {
        "id": "temazcal-completo",
        "title": "Temazcal • Rapé • Cenote",
        "subtitle": "pago completo",
        "accent": "soul",
        "bg_grad": [(247, 147, 26), (255, 215, 0)],
    },
    {
        "id": "cacao-completo",
        "title": "Cacao & Baño",
        "subtitle": "de Sonido",
        "accent": "copal",
        "bg_grad": [(128, 0, 128), (255, 215, 0)],
    },
    {
        "id": "cenote-completo",
        "title": "Cenote &",
        "subtitle": "Breathwork",
        "accent": "cenote",
        "bg_grad": [(13, 148, 136), (0, 168, 107)],
    },
    {
        "id": "rape-10g",
        "title": "Rapé ceremonial",
        "subtitle": "frasco 10g",
        "accent": "earth",
        "bg_grad": [(139, 69, 19), (210, 105, 30)],
    },
    {
        "id": "cacao-criollo-500g",
        "title": "Cacao criollo",
        "subtitle": "500g",
        "accent": "jade",
        "bg_grad": [(0, 168, 107), (13, 148, 136)],
    },
    {
        "id": "charla-btc-bienestar",
        "title": "Bitcoin &",
        "subtitle": "Bienestar",
        "accent": "souldeep",
        "bg_grad": [(194, 65, 12), (247, 147, 26)],
    },
]


def make_gradient(size, c1, c2):
    img = Image.new("RGB", size, c1)
    draw = ImageDraw.Draw(img)
    for y in range(size[1]):
        t = y / max(1, size[1]-1)
        r = int(c1[0] + (c2[0]-c1[0]) * t)
        g = int(c1[1] + (c2[1]-c1[1]) * t)
        b = int(c1[2] + (c2[2]-c1[2]) * t)
        draw.line((0, y, size[0], y), fill=(r, g, b))
    return img


def add_noise(img, amount=12000):
    pixels = img.load()
    w, h = img.size
    for _ in range(amount):
        x = random.randint(0, w-1)
        y = random.randint(0, h-1)
        c = img.getpixel((x, y))
        r = max(0, min(255, c[0] + random.randint(-12, 12)))
        g = max(0, min(255, c[1] + random.randint(-12, 12)))
        b = max(0, min(255, c[2] + random.randint(-12, 12)))
        pixels[x, y] = (r, g, b)
    return img


def add_mandala(img, accent):
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, h // 2
    main = accent + (80,)
    ring = accent + (36,)
    for radius in range(130, 30, -18):
        draw.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=ring, width=3)
    for i in range(12):
        a = i * 30
        rad = a * 3.14159 / 180
        x1 = cx + 140 * __import__('math').cos(rad)
        y1 = cy + 140 * __import__('math').sin(rad)
        x2 = cx + 220 * __import__('math').cos(rad)
        y2 = cy + 220 * __import__('math').sin(rad)
        draw.line((x1, y1, x2, y2), fill=main, width=3)
    draw.ellipse((cx-90, cy-90, cx+90, cy+90), outline=accent + (120,), width=8)
    return img


def add_symbol(img, kind):
    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size
    cx, cy = w // 2, h // 2
    if kind in {"temazcal-completo", "cacao-completo", "cenote-completo"}:
        # geometric sun/lotus motif
        for i in range(10):
            ang = i * 36 * 3.14159 / 180
            x1 = cx + 30 * __import__('math').cos(ang)
            y1 = cy + 30 * __import__('math').sin(ang)
            x2 = cx + 120 * __import__('math').cos(ang)
            y2 = cy + 120 * __import__('math').sin(ang)
            draw.line((x1, y1, x2, y2), fill=(255,255,255,120), width=4)
        draw.ellipse((cx-60, cy-60, cx+60, cy+60), fill=(255,255,255,70))
    elif kind in {"rape-10g", "cacao-criollo-500g"}:
        # jar / herb packet illustration
        draw.rounded_rectangle((cx-90, cy-60, cx+90, cy+110), radius=18, fill=(255,255,255,120))
        draw.rounded_rectangle((cx-60, cy-95, cx+60, cy+20), radius=12, fill=(255,255,255,80))
        draw.line((cx-70, cy-25, cx+70, cy-25), fill=(255,255,255,150), width=6)
    else:
        # bitcoin + lotus motif
        draw.ellipse((cx-90, cy-90, cx+90, cy+90), fill=(255,255,255,70))
        draw.text((cx-16, cy-12), "₿", font=None, fill=(255,255,255,220))
        draw.text((cx-70, cy+40), "Ikigai", fill=(255,255,255,180))
    return img


def make_product_image(product_id, title, subtitle, accent_name, bg_grad, size=(1200, 1200)):
    accent = COLORS[accent_name if accent_name in COLORS else "soul"]
    base = make_gradient(size, bg_grad[0], bg_grad[1])
    base = add_noise(base, 14000)
    base = add_mandala(base, accent)
    overlay = Image.new("RGBA", size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle((120, 120, 1080, 1080), radius=80, fill=(255,255,255,26))
    draw.rounded_rectangle((180, 180, 1020, 900), radius=60, fill=(255,255,255,18))
    base = Image.alpha_composite(base.convert("RGBA"), overlay)
    base = add_symbol(base, product_id)

    draw = ImageDraw.Draw(base, "RGBA")
    draw.text((150, 170), title, fill=(255,255,255,255), anchor=None)
    draw.text((150, 260), subtitle, fill=(255,255,255,220), anchor=None)

    # Accent chip
    draw.rounded_rectangle((150, 880, 440, 960), radius=30, fill=accent + (180,))
    draw.text((200, 900), "IKIGAI", fill=(255,255,255,255))

    out = OUT / f"{product_id}.png"
    base.convert("RGB").save(out, quality=90)
    print(f"✅ Generado: {out.name}")


if __name__ == "__main__":
    for product in PRODUCTS:
        make_product_image(
            product["id"],
            product["title"],
            product["subtitle"],
            product["accent"],
            product["bg_grad"],
        )
    print("\n✨ Productos listos para BTCPay / POS")
