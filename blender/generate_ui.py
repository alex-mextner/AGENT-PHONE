from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "blender" / "ui"
CANVAS_SIZE = (1400, 660)
W, H = CANVAS_SIZE
REQUIRED_TEXTURES = (
    "home", "chat", "marketplace", "split", "remote",
    "blind-input", "research", "handoff", "navigation", "camera",
)

BG = (3, 5, 8)
PANEL = (15, 20, 28)
PANEL_2 = (24, 31, 42)
PANEL_3 = (32, 42, 56)
WHITE = (241, 245, 249)
MUTED = (139, 151, 168)
DIM = (85, 97, 113)
CYAN = (78, 212, 255)
BLUE = (72, 143, 255)
GREEN = (78, 218, 136)
ORANGE = (255, 178, 72)
PURPLE = (174, 112, 255)
RED = (255, 104, 104)

FONT_CANDIDATES = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/SFNSRounded.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]

def font(size, bold=False):
    candidates = []
    if bold:
        candidates.extend([
            "/System/Library/Fonts/SFNSDisplayCondensed-Bold.otf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ])
    candidates.extend(FONT_CANDIDATES)
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()

F_TIME = font(84, True)
F_XL = font(48, True)
F_L = font(38, True)
F_M = font(30, True)
F_BODY = font(27)
F_S = font(22)
F_XS = font(18)

def canvas():
    image = Image.new("RGB", CANVAS_SIZE, BG)
    return image, ImageDraw.Draw(image)

def rr(draw, box, fill=PANEL, radius=24, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def line(draw, xy, fill=DIM, width=2):
    draw.line(xy, fill=fill, width=width)

def label(draw, xy, text, fill=MUTED, f=F_XS):
    draw.text(xy, text, fill=fill, font=f)

def save(image, out, name):
    out.mkdir(parents=True, exist_ok=True)
    image.save(out / f"{name}.png", optimize=True)

def draw_top_status(draw, title=None):
    label(draw, (36, 18), "19:26", WHITE, F_S)
    if title:
        label(draw, (116, 18), title, MUTED, F_S)
    label(draw, (1240, 18), "5G", MUTED, F_S)
    rr(draw, (1294, 18, 1362, 45), fill=(19, 67, 37), radius=12)
    label(draw, (1312, 20), "58", GREEN, F_XS)

def home(out):
    im, d = canvas()
    draw_top_status(d)
    label(d, (40, 78), "10:24", WHITE, F_TIME)
    label(d, (46, 176), "WED 23 SEP", MUTED, F_S)
    rr(d, (300, 72, 690, 246), fill=PANEL)
    label(d, (326, 96), "NEXT", CYAN, F_XS)
    label(d, (326, 130), "11:00  Design review", WHITE, F_M)
    label(d, (326, 178), "Danny · Saba · Niko", MUTED, F_S)
    label(d, (326, 210), "Confirmed · 42 min", GREEN, F_XS)
    rr(d, (712, 72, 1020, 246), fill=PANEL)
    label(d, (738, 96), "FOOD", GREEN, F_XS)
    label(d, (738, 132), "Arrives in 12 min", WHITE, F_M)
    label(d, (738, 180), "Courier picked up", MUTED, F_S)
    rr(d, (1042, 72, 1360, 246), fill=PANEL)
    label(d, (1068, 96), "DEEP RESEARCH", PURPLE, F_XS)
    label(d, (1068, 132), "37% · 12 sources", WHITE, F_M)
    label(d, (1068, 180), "Comparing display tech", MUTED, F_S)
    rr(d, (300, 278, 1360, 438), fill=(10, 13, 19))
    label(d, (326, 304), "NOW", MUTED, F_XS)
    label(d, (326, 342), "No urgent notifications", WHITE, F_L)
    label(d, (326, 396), "Raise, tilt, or pinch only when you need the screen.", MUTED, F_S)
    label(d, (44, 566), "72%  ·  eSIM  ·  glasses nearby  ·  ring connected", DIM, F_S)
    save(im, out, "home")

def chat(out):
    im, d = canvas()
    draw_top_status(d, "Messages")
    # Left chat list.
    rr(d, (24, 64, 414, 632), fill=(8, 11, 16), radius=28)
    label(d, (48, 86), "CHATS", MUTED, F_XS)
    chats = [
        ("Lena", "Can we meet at 19:00?", "2"),
        ("Danny", "Sent the design notes", ""),
        ("Family", "Photo", "1"),
        ("Niko", "Yep, tomorrow works", ""),
    ]
    y = 132
    for i, (name, preview, unread) in enumerate(chats):
        fill = PANEL_2 if i == 0 else PANEL
        rr(d, (42, y, 394, y + 104), fill=fill, radius=22)
        d.ellipse((60, y + 19, 122, y + 81), fill=(44 + i*10, 62, 82 + i*8))
        label(d, (140, y + 18), name, WHITE, F_M)
        label(d, (140, y + 58), preview, MUTED, F_XS)
        if unread:
            d.ellipse((348, y + 35, 378, y + 65), fill=BLUE)
            label(d, (358, y + 38), unread, WHITE, F_XS)
        y += 116
    # Strong divider: tests sample x=430.
    d.rectangle((428, 64, 432, 632), fill=(58, 67, 82))
    # Conversation pane.
    label(d, (462, 82), "Lena", WHITE, F_L)
    label(d, (574, 91), "online", GREEN, F_XS)
    rr(d, (470, 150, 956, 244), fill=PANEL_2, radius=26)
    label(d, (496, 176), "Can we meet at 19:00?", WHITE, F_BODY)
    label(d, (844, 212), "19:18", DIM, F_XS)
    rr(d, (730, 278, 1318, 382), fill=(18, 58, 82), radius=28)
    label(d, (756, 307), "Yes — I’ll send the place.", WHITE, F_BODY)
    label(d, (1214, 350), "19:20", (128, 172, 194), F_XS)
    rr(d, (470, 430, 1110, 516), fill=PANEL, radius=24)
    label(d, (496, 457), "Draft silently…", DIM, F_BODY)
    rr(d, (1130, 430, 1320, 516), fill=(24, 73, 58), radius=24)
    label(d, (1180, 456), "Send", GREEN, F_M)
    label(d, (468, 574), "Telekinesis armed · pinch to confirm", MUTED, F_S)
    save(im, out, "chat")

def marketplace(out):
    im, d = canvas()
    draw_top_status(d, "Market")
    rr(d, (32, 78, 410, 610), fill=(9, 12, 17), radius=30)
    d.ellipse((98, 156, 344, 402), fill=(31, 38, 49), outline=(71, 83, 101), width=4)
    d.arc((138, 196, 304, 362), 20, 335, fill=CYAN, width=18)
    label(d, (72, 502), "Sony WH-1000XM6", WHITE, F_M)
    label(d, (72, 548), "Black · in stock", GREEN, F_S)
    label(d, (458, 96), "Best match for your flight", MUTED, F_S)
    label(d, (458, 146), "$448", WHITE, F_TIME)
    label(d, (458, 248), "Prime delivery · tomorrow", WHITE, F_M)
    label(d, (458, 292), "30-day returns · 2-year warranty", MUTED, F_S)
    rr(d, (458, 370, 832, 474), fill=(234, 240, 246), radius=28)
    label(d, (584, 400), "Buy", (8, 10, 14), F_L)
    rr(d, (858, 370, 1270, 474), fill=PANEL_2, radius=28)
    label(d, (930, 400), "Compare 3", WHITE, F_L)
    label(d, (458, 542), "Why this?  Better ANC, arrives before departure, within budget.", MUTED, F_S)
    save(im, out, "marketplace")

def split(out):
    im, d = canvas()
    draw_top_status(d, "Split")
    line(d, (700, 70, 700, 628), fill=(57, 68, 84), width=3)
    label(d, (34, 84), "Lena", WHITE, F_L)
    rr(d, (34, 150, 624, 246), fill=PANEL_2)
    label(d, (58, 178), "Look at these from yesterday", WHITE, F_BODY)
    rr(d, (226, 280, 652, 370), fill=(18, 58, 82))
    label(d, (250, 307), "The second one.", WHITE, F_BODY)
    label(d, (738, 84), "Photos · yesterday", WHITE, F_L)
    boxes=[(738,150,1016,354),(1032,150,1310,354),(738,372,1016,602),(1032,372,1310,602)]
    cols=[(31,61,79),(66,75,56),(48,64,92),(72,54,74)]
    for idx,(b,c) in enumerate(zip(boxes,cols)):
        rr(d,b,fill=c,radius=20)
        d.ellipse((b[0]+58,b[1]+34,b[0]+110,b[1]+86),fill=(224,190,112))
        d.polygon([(b[0]+18,b[3]-20),(b[0]+120,b[1]+82),(b[2]-18,b[3]-20)],fill=(39,110,91))
        label(d,(b[0]+18,b[3]-48),f"{idx+1}/4",WHITE,F_XS)
    save(im, out, "split")

def remote(out):
    im, d = canvas()
    draw_top_status(d, "Living room")
    cards=[
        ((34,100,438,590),"TV","Playing · 42 min",CYAN),
        ((466,100,870,590),"AC","23°C · cooling",BLUE),
        ((898,100,1302,590),"LIGHTS","3 of 5 on",ORANGE),
    ]
    for box,title,sub,accent in cards:
        rr(d,box,fill=PANEL,radius=30)
        label(d,(box[0]+32,box[1]+30),title,accent,F_M)
        label(d,(box[0]+32,box[1]+86),sub,WHITE,F_BODY)
    label(d,(86,310),"◀   II   ▶",WHITE,F_XL)
    label(d,(536,310),"−   23   +",WHITE,F_XL)
    label(d,(970,310),"Dim  64%",WHITE,F_L)
    label(d,(84,500),"Volume 38%",MUTED,F_S)
    label(d,(536,500),"Auto",MUTED,F_S)
    label(d,(970,500),"Warm",MUTED,F_S)
    save(im, out, "remote")

def blind_input(out):
    im, d = canvas()
    d.ellipse((56, 306, 78, 328), fill=CYAN)
    label(d, (100, 295), "composing privately", (74, 86, 102), F_S)
    label(d, (1168, 295), "6 words", (53, 63, 76), F_S)
    # Tiny waveform and confidence tick; keep the rest black.
    for i,h in enumerate((8,16,26,12,30,18,10)):
        x=625+i*18
        d.rectangle((x,330-h//2,x+4,330+h//2),fill=(35,72,85))
    save(im, out, "blind-input")

def research(out):
    im,d=canvas()
    draw_top_status(d,"Deep research")
    label(d,(44,88),"Battery architecture",WHITE,F_L)
    label(d,(44,144),"37% complete · 12 sources read · 3 hypotheses",MUTED,F_S)
    rr(d,(44,216,954,302),fill=PANEL)
    d.rectangle((70,250,386,266),fill=PURPLE)
    d.rectangle((386,250,910,266),fill=(39,43,55))
    label(d,(1010,228),"ETA",MUTED,F_XS)
    label(d,(1010,260),"~6 min",WHITE,F_L)
    rr(d,(44,344,654,566),fill=PANEL)
    label(d,(70,370),"Current finding",PURPLE,F_XS)
    label(d,(70,414),"Curved cells help packaging,",WHITE,F_BODY)
    label(d,(70,456),"but split flat cells are safer for P0.",WHITE,F_BODY)
    rr(d,(684,344,1344,566),fill=PANEL)
    label(d,(710,370),"Next",CYAN,F_XS)
    label(d,(710,414),"Compare LTPO OLED suppliers",WHITE,F_BODY)
    label(d,(710,456),"and controller availability.",WHITE,F_BODY)
    save(im,out,"research")

def handoff(out):
    im,d=canvas()
    draw_top_status(d,"Move to display")
    label(d,(42,88),"Travel plan",WHITE,F_L)
    rr(d,(42,154,520,500),fill=PANEL)
    label(d,(70,184),"ROME · 4 DAYS",CYAN,F_XS)
    label(d,(70,242),"Flight  JU 404",WHITE,F_M)
    label(d,(70,294),"Hotel  Trastevere",WHITE,F_M)
    label(d,(70,346),"6 saved places",WHITE,F_M)
    label(d,(600,250),"→  →  →",CYAN,F_TIME)
    rr(d,(900,154,1340,500),fill=(11,17,25),outline=(64,95,120),width=3)
    label(d,(972,218),"Living-room TV",WHITE,F_L)
    label(d,(1000,292),"Open there",CYAN,F_M)
    label(d,(946,390),"Ring release to send",MUTED,F_S)
    save(im,out,"handoff")

def navigation(out):
    im,d=canvas()
    draw_top_status(d,"Walk")
    # Stylized dark map.
    for x in range(70,1330,160):
        line(d,(x,92,x-160,620),fill=(26,32,40),width=14)
    for y in range(140,620,130):
        line(d,(20,y,1380,y+55),fill=(22,29,37),width=10)
    line(d,(168,530,360,420,520,356,710,260,936,220,1160,122),fill=CYAN,width=14)
    d.ellipse((1144,106,1178,140),fill=CYAN)
    rr(d,(44,92,356,206),fill=(5,8,12),radius=24)
    label(d,(72,116),"8 min · 620 m",WHITE,F_M)
    label(d,(72,160),"Turn right in 90 m",MUTED,F_S)
    save(im,out,"navigation")

def camera(out):
    im,d=canvas()
    draw_top_status(d,"Agent Camera")
    # Viewfinder image proxy.
    rr(d,(26,70,1050,632),fill=(24,37,42),radius=26)
    d.ellipse((318,160,728,570),fill=(72,92,76))
    d.rectangle((558,190,986,570),fill=(44,63,78))
    label(d,(1080,118),"1×",WHITE,F_L)
    label(d,(1080,190),"HDR",GREEN,F_S)
    label(d,(1080,246),"AF locked",CYAN,F_S)
    d.ellipse((1128,350,1284,506),outline=WHITE,width=8)
    d.ellipse((1162,384,1250,472),fill=WHITE)
    label(d,(1080,548),"Ring: squeeze",MUTED,F_XS)
    label(d,(1080,578),"to capture",MUTED,F_XS)
    save(im,out,"camera")

def generate_all(out=DEFAULT_OUT):
    out = Path(out)
    renderers = {
        "home": home,
        "chat": chat,
        "marketplace": marketplace,
        "split": split,
        "remote": remote,
        "blind-input": blind_input,
        "research": research,
        "handoff": handoff,
        "navigation": navigation,
        "camera": camera,
    }
    for name in REQUIRED_TEXTURES:
        renderers[name](out)
    return [out / f"{name}.png" for name in REQUIRED_TEXTURES]

if __name__ == "__main__":
    generated = generate_all()
    print(f"Generated {len(generated)} UI textures in {DEFAULT_OUT}")
