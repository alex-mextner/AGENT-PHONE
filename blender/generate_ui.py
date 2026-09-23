from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "blender" / "ui"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1200, 408

FONT_CANDIDATES = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]

def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/SFNSDisplayCondensed-Bold.otf" if bold else "",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
    ] + FONT_CANDIDATES
    for p in candidates:
        if p and Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F_BIG = font(92, True)
F_H = font(38, True)
F_M = font(30, False)
F_S = font(24, False)
F_XS = font(19, False)

BG = (4, 6, 9)
PANEL = (14, 18, 25)
PANEL2 = (20, 25, 34)
WHITE = (238, 242, 247)
MUTED = (145, 155, 170)
CYAN = (83, 220, 255)
GREEN = (87, 218, 139)
ORANGE = (255, 180, 85)
PURPLE = (170, 110, 255)

def canvas():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)

def rr(d, box, fill=PANEL, radius=26, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def pill(d, box, text, color=CYAN):
    rr(d, box, fill=tuple(max(0, c//5) for c in color), radius=22)
    d.text((box[0]+20, box[1]+10), text, fill=color, font=F_S)

def save(im, name):
    im.save(OUT / f"{name}.png", quality=95)

def home():
    im,d = canvas()
    d.text((40, 32), "10:24", fill=WHITE, font=F_BIG)
    d.text((45, 145), "WED · 23 SEP", fill=MUTED, font=F_S)
    rr(d,(330,34,610,184))
    d.text((355,54),"11:00",fill=CYAN,font=F_H)
    d.text((355,104),"Design review",fill=WHITE,font=F_M)
    d.text((355,145),"Calendar · confirmed",fill=MUTED,font=F_XS)
    rr(d,(630,34,900,184))
    d.text((654,54),"FOOD",fill=GREEN,font=F_S)
    d.text((654,92),"12 min",fill=WHITE,font=F_H)
    d.text((654,145),"Courier is close",fill=MUTED,font=F_XS)
    rr(d,(920,34,1160,184))
    d.text((944,54),"AI",fill=PURPLE,font=F_S)
    d.text((944,92),"Researching",fill=WHITE,font=F_M)
    d.text((944,145),"3 / 5 sources",fill=MUTED,font=F_XS)
    pill(d,(330,220,610,280),"Next: 13:30 · call",CYAN)
    pill(d,(630,220,900,280),"Home · all normal",GREEN)
    pill(d,(920,220,1160,280),"Battery · 72%",ORANGE)
    d.text((40,330),"Input: pinch · silent speech · voice",fill=MUTED,font=F_S)
    save(im,"home")

def marketplace():
    im,d=canvas()
    d.text((40,28),"Market",fill=WHITE,font=F_H)
    rr(d,(42,92,360,355),fill=(12,16,22))
    d.ellipse((125,125,275,275),fill=(34,41,51),outline=(90,100,115),width=3)
    d.arc((145,145,255,255),20,330,fill=CYAN,width=12)
    d.text((410,88),"Nova Buds",fill=WHITE,font=F_H)
    d.text((410,145),"Adaptive audio · 28 h",fill=MUTED,font=F_S)
    d.text((410,204),"$129",fill=WHITE,font=F_BIG)
    rr(d,(805,202,1145,322),fill=(235,240,245),radius=30)
    d.text((900,236),"Buy",fill=(8,10,13),font=F_H)
    d.text((410,320),"Arrives tomorrow · free returns",fill=MUTED,font=F_S)
    save(im,"marketplace")

def chat():
    im,d=canvas()
    d.text((36,28),"‹",fill=CYAN,font=F_H)
    d.text((90,30),"Lena",fill=WHITE,font=F_H)
    d.text((230,40),"online",fill=GREEN,font=F_XS)
    rr(d,(70,105,700,200),fill=PANEL2)
    d.text((98,128),"Can we meet at 19:00?",fill=WHITE,font=F_M)
    rr(d,(430,225,1128,326),fill=(17,42,58))
    d.text((462,246),"Yes — I'll send the place.",fill=WHITE,font=F_M)
    d.text((1010,300),"10:22",fill=MUTED,font=F_XS)
    d.text((48,360),"Telekinesis ready · pinch to reply",fill=MUTED,font=F_XS)
    save(im,"chat")

def split():
    im,d=canvas()
    d.line((600,18,600,H-18),fill=(45,52,65),width=2)
    d.text((32,28),"Lena",fill=WHITE,font=F_H)
    rr(d,(38,92,558,180),fill=PANEL2)
    d.text((62,112),"Look at these from yesterday",fill=WHITE,font=F_S)
    rr(d,(208,210,558,286),fill=(17,42,58))
    d.text((232,232),"The second one 👌",fill=WHITE,font=F_S)
    d.text((634,28),"Photos",fill=WHITE,font=F_H)
    colors=[(42,65,88),(87,74,57),(46,78,65),(73,54,86)]
    boxes=[(635,92,875,218),(890,92,1130,218),(635,234,875,360),(890,234,1130,360)]
    for b,c in zip(boxes,colors):
        rr(d,b,fill=c,radius=18)
        d.ellipse((b[0]+55,b[1]+25,b[0]+110,b[1]+80),fill=(225,195,120))
        d.polygon([(b[0]+15,b[3]-18),(b[0]+100,b[1]+60),(b[2]-15,b[3]-18)],fill=(45,110,95))
    save(im,"split")

def remote():
    im,d=canvas()
    d.text((38,26),"Home",fill=WHITE,font=F_H)
    cards=[(40,95,390,350),(425,95,775,350),(810,95,1160,350)]
    labels=[("TV","Living room"),("AC","23° · cooling"),("LIGHT","3 of 5 on")]
    accents=[CYAN,CYAN,ORANGE]
    for b,(title,sub),a in zip(cards,labels,accents):
        rr(d,b,fill=PANEL)
        d.text((b[0]+30,b[1]+28),title,fill=a,font=F_H)
        d.text((b[0]+30,b[1]+85),sub,fill=WHITE,font=F_M)
    d.text((80,270),"▶  Pause",fill=WHITE,font=F_M)
    d.text((473,270),"−   23   +",fill=WHITE,font=F_H)
    d.text((855,270),"Dim  64%",fill=WHITE,font=F_M)
    save(im,"remote")

def blind_input():
    im,d=canvas()
    d.ellipse((42,176,58,192),fill=CYAN)
    d.text((82,163),"composing privately",fill=(92,105,120),font=F_XS)
    d.text((930,163),"6 words",fill=(66,76,90),font=F_XS)
    save(im,"blind-input")

for fn in [home, marketplace, chat, split, remote, blind_input]:
    fn()
print(f"Generated UI textures in {OUT}")
