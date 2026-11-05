from pathlib import Path
import math
import random

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# TRACE//X — CyberEye Chapter 02
# A cinematic, simulated cybersecurity investigation sequence.
# All activity shown is fictional/simulated; this does not monitor a live network.

W, H = 1280, 720
FPS = 24
DURATION = 36
TOTAL_FRAMES = FPS * DURATION

BG = (5, 12, 24)
PANEL = (9, 23, 39)
CYAN = (54, 220, 245)
BLUE = (45, 130, 210)
PALE = (205, 235, 242)
MUTED = (100, 151, 171)
AMBER = (255, 177, 76)
RED = (255, 99, 105)

def load_font(size):
    candidates = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()

F = {s: load_font(s) for s in (12, 14, 16, 18, 20, 22, 26, 30, 36, 44, 54, 66, 72)}

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def smooth(a, b, x):
    q = clamp((x - a) / (b - a))
    return q * q * (3 - 2 * q)

def mix(a, b, t):
    return int(a + (b - a) * clamp(t))

def centered(draw, text, y, font, fill, x=W // 2):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((x - (box[2] - box[0]) / 2, y), text, font=font, fill=fill)

def background():
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - W * 0.53) / 700) ** 2 + ((yy - H * 0.48) / 520) ** 2) * 2.0)
    for c, base in enumerate(BG):
        arr[:, :, c] = np.clip(base + glow * (8 if c == 1 else 14 if c == 2 else 3), 0, 255)
    im = Image.fromarray(arr, "RGB").convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    for x in range(0, W, 40):
        d.line((x, 0, x, H), fill=(35, 92, 116, 22), width=1)
    for y in range(0, H, 40):
        d.line((0, y, W, y), fill=(35, 92, 116, 18), width=1)
    return im

BGIMG = background()

def glow(im, layer, blur=13):
    base = im.convert("RGBA")
    blurred = layer.filter(ImageFilter.GaussianBlur(blur))
    base = Image.alpha_composite(base, blurred)
    base = Image.alpha_composite(base, layer)
    return base.convert("RGB")

def frame_shell(im, t, section):
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((25, 22, W - 25, H - 22), radius=17, outline=(55, 160, 190, 95), width=1)
    d.text((49, 39), "CYBEREYE  /  CHAPTER 02", font=F[16], fill=(125, 205, 220, 230))
    d.text((W - 290, 42), "TRACE//X  •  SIMULATION", font=F[14], fill=(95, 155, 175, 220))
    d.text((50, H - 57), f"{section}  //  {t:05.2f}s", font=F[14], fill=(100, 165, 183, 220))
    d.line((50, H - 29, W - 50, H - 29), fill=(35, 85, 105, 150), width=2)
    d.line((50, H - 29, 50 + (W - 100) * t / DURATION, H - 29), fill=(*CYAN, 235), width=3)
    return im

def dot(draw, x, y, r, color, alpha=255):
    draw.ellipse((x-r, y-r, x+r, y+r), fill=(*color, alpha))

def intro(t):
    im = BGIMG.copy().convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    scan_y = int(150 + (t / 5.0) * 420)
    d.rectangle((85, scan_y - 2, W - 85, scan_y + 2), fill=(40, 200, 235, 100))
    dot(d, W // 2, scan_y, 7, CYAN, 230)
    im = glow(im, layer, 12)
    d = ImageDraw.Draw(im, "RGBA")
    q = smooth(0.3, 1.7, t)
    centered(d, "CYBEREYE", 236, F[72], (65, 220, 255, int(255*q)))
    centered(d, "SIGNAL DETECTED", 337, F[26], (190, 230, 238, int(245*q)))
    centered(d, "INVESTIGATION INITIATED", 390, F[18], (105, 185, 200, int(230*q)))
    if t > 3.2:
        centered(d, "HANDOFF TO TRACE//X", 500, F[20], (*AMBER, int(240*smooth(3.2, 4.5, t))))
    return frame_shell(im, t, "SIGNAL HANDOFF")

def tunnel(t):
    im = BGIMG.copy().convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    cx, cy = W // 2, H // 2
    for i in range(22):
        z = (i / 22 + (t * 0.23) % 1.0) % 1.0
        scale = 0.08 + z * 1.25
        rw, rh = int(95 * scale + 15), int(55 * scale + 10)
        alpha = int(22 + z * 90)
        d.rounded_rectangle((cx-rw, cy-rh, cx+rw, cy+rh), radius=8, outline=(40, 180, 220, alpha), width=2)
    rng = random.Random(12)
    for i in range(95):
        x0 = rng.randint(0, W)
        y0 = rng.randint(0, H)
        x = (x0 + int((t * 38) * (0.25 + (i % 7) / 8))) % W
        y = (y0 + int(math.sin(t * 1.5 + i) * 13)) % H
        dot(d, x, y, 1 + (i % 3 == 0), CYAN, 70 + i % 100)
    im = glow(im, layer, 9)
    d = ImageDraw.Draw(im, "RGBA")
    centered(d, "TRACE//X", 290, F[66], PALE)
    centered(d, "FOLLOWING THE SIGNAL", 375, F[20], CYAN)
    centered(d, "SIMULATED EVENT STREAM", 420, F[14], MUTED)
    return frame_shell(im, t, "SIGNAL TRACE")

def network(t):
    im = BGIMG.copy().convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    nodes = [
        (170, 190), (365, 115), (565, 215), (790, 125), (1065, 205),
        (230, 470), (465, 390), (690, 520), (930, 410), (1110, 535),
        (640, 340), (870, 285)
    ]
    edges = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,2),(6,7),(7,8),(8,4),(8,9),(2,10),(10,11),(11,4),(10,7),(1,6),(3,11)]
    for a, b in edges:
        d.line((*nodes[a], *nodes[b]), fill=(48, 130, 170, 95), width=2)
    for k, (a, b) in enumerate(edges):
        x1, y1 = nodes[a]; x2, y2 = nodes[b]
        p = (t * 0.42 + k * 0.137) % 1
        px, py = x1 + (x2-x1)*p, y1 + (y2-y1)*p
        dot(d, int(px), int(py), 4, CYAN, 230)
    pulse = 0.5 + 0.5 * math.sin(t * 4)
    ax, ay = nodes[10]
    d.ellipse((ax-28, ay-28, ax+28, ay+28), outline=(*AMBER, 180), width=3)
    d.ellipse((ax-42, ay-42, ax+42, ay+42), outline=(*AMBER, int(45+50*pulse)), width=2)
    for i, (x, y) in enumerate(nodes):
        col = AMBER if i == 10 else CYAN
        dot(d, x, y, 8 if i == 10 else 6, col, 245)
    im = glow(im, layer, 10)
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((820, 70, 1160, 170), radius=12, fill=(8, 22, 37, 230), outline=(*AMBER, 180), width=2)
    d.text((845, 91), "ANOMALY FLAGGED", font=F[20], fill=AMBER)
    d.text((845, 125), "Behaviour deviation • simulated", font=F[14], fill=PALE)
    d.text((82, 90), "NETWORK EVENT MAP", font=F[22], fill=PALE)
    d.text((82, 123), "12 NODES  /  17 LINKS  /  LIVE SIMULATION", font=F[14], fill=MUTED)
    return frame_shell(im, t, "BEHAVIOUR ANALYSIS")

def forensic(t):
    im = BGIMG.copy().convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")
    d.text((82, 95), "FORENSIC EVENT TRAIL", font=F[30], fill=PALE)
    d.text((82, 137), "A transparent record of the simulated investigation", font=F[16], fill=MUTED)
    events = [
        ("00:04.8", "SIGNAL RECEIVED", "CyberEye handoff initiated", CYAN),
        ("00:11.2", "PATTERN COMPARED", "Activity differs from baseline", CYAN),
        ("00:18.6", "ANOMALY FLAGGED", "Rule-based threshold reached", AMBER),
        ("00:25.1", "EVENT CORRELATED", "Related events grouped for review", CYAN),
        ("00:31.4", "TRACE RECORDED", "Investigation trail preserved", CYAN),
    ]
    reveal = clamp((t - 20.0) / 11.0) * len(events)
    xline = 135
    d.line((xline, 205, xline, 585), fill=(45, 115, 145, 180), width=3)
    for i, (stamp, title, detail, color) in enumerate(events):
        y = 215 + i * 78
        visible = smooth(i * 0.75, i * 0.75 + 0.65, reveal)
        if visible <= 0:
            continue
        alpha = int(255 * visible)
        d.ellipse((xline-8, y-8, xline+8, y+8), fill=(*color, alpha))
        d.rounded_rectangle((175, y-27, 1095, y+39), radius=10, fill=(9, 25, 42, int(210*visible)), outline=(*color, int(90*visible)), width=1)
        d.text((200, y-13), stamp, font=F[16], fill=(*MUTED, alpha))
        d.text((330, y-16), title, font=F[18], fill=(*color, alpha))
        d.text((640, y-13), detail, font=F[14], fill=(*PALE, alpha))
    return frame_shell(im, t, "FORENSIC TIMELINE")

def outro(t):
    im = BGIMG.copy().convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    for i in range(9):
        r = 55 + i * 42 + int(5 * math.sin(t * 2 + i))
        d.ellipse((W//2-r, H//2-r, W//2+r, H//2+r), outline=(40, 170, 210, max(15, 90-i*8)), width=2)
    im = glow(im, layer, 12)
    d = ImageDraw.Draw(im, "RGBA")
    q = smooth(0.2, 1.5, t - 30)
    centered(d, "TRACE//X", 245, F[72], (75, 220, 250, int(255*q)))
    centered(d, "EVERY SIGNAL LEAVES A TRACE", 355, F[26], (220, 240, 245, int(250*q)))
    centered(d, "CYBEREYE  /  CHAPTER 02", 420, F[18], (110, 175, 190, int(230*q)))
    centered(d, "SIMULATED CYBERSECURITY VISUALISATION", 505, F[14], (95, 145, 165, int(220*q)))
    return frame_shell(im, t, "INVESTIGATION COMPLETE")

def make_frame(frame):
    t = frame / FPS
    if t < 5:
        im = intro(t)
    elif t < 12:
        im = tunnel(t - 5)
    elif t < 21:
        im = network(t - 12)
    elif t < 31:
        im = forensic(t)
    else:
        im = outro(t)
    return im.convert("RGB")

def render_video(output_path="output/TRACE_X_CyberEye_Chapter_02.mp4"):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = imageio.get_writer(
        str(path),
        fps=FPS,
        codec="libx264",
        macro_block_size=16,
        ffmpeg_params=[
            "-pix_fmt", "yuv420p",
            "-preset", "medium",
            "-crf", "18",
            "-movflags", "+faststart",
        ],
    )
    try:
        for frame in range(TOTAL_FRAMES):
            writer.append_data(np.asarray(make_frame(frame)))
            if frame % (FPS * 3) == 0:
                print(f"Rendering: {frame / TOTAL_FRAMES:.0%}")
    finally:
        writer.close()
    return path.resolve()
