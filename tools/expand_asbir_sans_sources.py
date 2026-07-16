"""Add the editable Basic Latin foundation to all Asbir Sans UFO masters.

This is intentionally a foundation pass: every glyph remains editable in UFO
form and shares compatible construction across the Thin, Regular and Black
masters. It is not a substitute for a type designer's optical drawing pass.
"""
from pathlib import Path
from ufoLib2 import Font

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources' / 'asbir-sans'
MASTERS = [('AsbirSans-Thin.ufo', 30), ('AsbirSans-Regular.ufo', 64), ('AsbirSans-Black.ufo', 150)]
CAP, XH, ASC, DESC = 700, 555, 760, -210

def rect(p, x, y, w, h):
    p.moveTo((x, y)); p.lineTo((x + w, y)); p.lineTo((x + w, y + h)); p.lineTo((x, y + h)); p.closePath()

def poly(p, pts):
    p.moveTo(pts[0])
    for point in pts[1:]: p.lineTo(point)
    p.closePath()

def oval(p, cx, cy, rx, ry, reverse=False):
    k = .55228475
    if reverse:
        p.moveTo((cx + rx, cy)); p.curveTo((cx + rx, cy - k * ry), (cx + k * rx, cy - ry), (cx, cy - ry)); p.curveTo((cx - k * rx, cy - ry), (cx - rx, cy - k * ry), (cx - rx, cy)); p.curveTo((cx - rx, cy + k * ry), (cx - k * rx, cy + ry), (cx, cy + ry)); p.curveTo((cx + k * rx, cy + ry), (cx + rx, cy + k * ry), (cx + rx, cy)); p.closePath()
    else:
        p.moveTo((cx + rx, cy)); p.curveTo((cx + rx, cy + k * ry), (cx + k * rx, cy + ry), (cx, cy + ry)); p.curveTo((cx - k * rx, cy + ry), (cx - rx, cy + k * ry), (cx - rx, cy)); p.curveTo((cx - rx, cy - k * ry), (cx - k * rx, cy - ry), (cx, cy - ry)); p.curveTo((cx + k * rx, cy - ry), (cx + rx, cy - k * ry), (cx + rx, cy)); p.closePath()

def ring(p, cx, cy, rx, ry, t):
    oval(p, cx, cy, rx, ry)
    oval(p, cx, cy, max(8, rx-t), max(8, ry-t), reverse=True)

def diagonal(p, x1, y1, x2, y2, t):
    dx, dy = x2-x1, y2-y1
    length = max((dx*dx + dy*dy) ** .5, 1)
    ox, oy = -dy / length * t / 2, dx / length * t / 2
    poly(p, [(x1+ox,y1+oy), (x2+ox,y2+oy), (x2-ox,y2-oy), (x1-ox,y1-oy)])

def rounded_rect(p, x, y, w, h, r):
    """A quiet corner radius used for terminals, never a capsule."""
    r = min(r, w / 2, h / 2)
    k = .55228475
    p.moveTo((x + r, y)); p.lineTo((x + w - r, y))
    p.curveTo((x + w - r + k*r, y), (x + w, y + r - k*r), (x + w, y + r))
    p.lineTo((x + w, y + h - r))
    p.curveTo((x + w, y + h - r + k*r), (x + w - r + k*r, y + h), (x + w - r, y + h))
    p.lineTo((x + r, y + h))
    p.curveTo((x + r - k*r, y + h), (x, y + h - r + k*r), (x, y + h - r))
    p.lineTo((x, y + r))
    p.curveTo((x, y + r - k*r), (x + r - k*r, y), (x + r, y))
    p.closePath()

def arch(p, left, right, bottom, top, stem):
    """Draw a compact neo-grotesk shoulder as one continuous contour."""
    inner_left, inner_right = left + stem, right - stem
    inner_top = top - stem
    p.moveTo((left, bottom)); p.lineTo((left, top))
    p.curveTo((left + (right-left)*.34, top + 10), (right, top - (top-bottom)*.17), (right, top - (top-bottom)*.37))
    p.lineTo((right, bottom)); p.lineTo((inner_right, bottom))
    p.lineTo((inner_right, top - (top-bottom)*.37))
    p.curveTo((inner_right, top - stem*.55), (inner_left + (right-left)*.34, inner_top), (inner_left, inner_top))
    p.lineTo((inner_left, bottom)); p.closePath()

def open_c(p, cx, cy, rx, ry, t, opening=.29):
    """An open bowl with curved terminals, avoiding the former box-built C/c."""
    outer_r = cx + rx * (1 - opening)
    inner_r = cx + max(8, rx - t) * (1 - opening)
    p.moveTo((outer_r, cy + ry*.68))
    p.curveTo((cx + rx*.48, cy + ry), (cx - rx*.42, cy + ry), (cx - rx, cy + ry*.43))
    p.curveTo((cx-rx, cy-ry*.43), (cx-rx*.42, cy-ry), (cx+rx*.48, cy-ry))
    p.curveTo((cx+rx*.73, cy-ry*.75), (outer_r, cy-ry*.58), (outer_r, cy-ry*.50))
    p.lineTo((inner_r, cy-ry*.39))
    p.curveTo((cx+rx*.38, cy-ry+t), (cx-rx+t, cy-ry*.32), (cx-rx+t, cy))
    p.curveTo((cx-rx+t, cy+ry*.32), (cx+rx*.38, cy+ry-t), (inner_r, cy+ry*.39))
    p.closePath()

def smooth_s(p, cx, cy, w, h, t):
    """Single-contour, high-x-height s with open horizontal terminals."""
    l, r, top, bot = cx-w/2, cx+w/2, cy+h/2, cy-h/2
    p.moveTo((r-t*.35, top-t*.1))
    p.curveTo((cx+w*.1, top+t*.08), (l+t*.15, top-t*.08), (l+t*.1, cy+h*.12))
    p.curveTo((l+t*.05, cy+h*.01), (cx-w*.06, cy+t*.08), (cx-w*.01, cy))
    p.curveTo((cx+w*.1, cy-h*.12), (r-t*.04, cy-h*.03), (r-t*.08, cy-h*.21))
    p.curveTo((r-t*.12, bot+t*.05), (cx-w*.12, bot-t*.06), (l+t*.05, bot+t*.14))
    p.lineTo((l+t*.16, bot+t*.98))
    p.curveTo((cx-w*.1, bot+t*.62), (r-t*.65, bot+t*.85), (r-t*.58, cy-h*.23))
    p.curveTo((r-t*.54, cy-h*.05), (cx+w*.05, cy-h*.06), (cx-w*.04, cy+t*.03))
    p.curveTo((cx-w*.17, cy+t*.15), (l+t*.46, cy+t*.12), (l+t*.52, cy+h*.14))
    p.curveTo((l+t*.58, top-t*.62), (cx+w*.08, top-t*.45), (r-t*.32, top-t*.98))
    p.closePath()

def upper(p, char, s):
    w, t = 500, s
    if char == 'A':
        diagonal(p, 72, 0, 220, CAP, t)
        diagonal(p, 428, 0, 280, CAP, t)
        rounded_rect(p, 151, 286, 198, t*.82, min(16, t*.22))
    if char in 'ODQ':
        ring(p, 250, 350, 210, 350, t)
        if char == 'D': rect(p, 40, 0, t, CAP)
        if char == 'Q': diagonal(p, 295, 135, 460, -40, t)
    elif char == 'B':
        rect(p, 40, 0, t, CAP); ring(p, 245, 525, 190, 160, t); ring(p, 245, 175, 190, 160, t)
    elif char == 'C': open_c(p, 252, 350, 212, 350, t, .25)
    elif char in 'EF':
        rect(p, 40, 0, t, CAP); rect(p, 40, CAP-t, 390, t); rect(p, 40, 310, 310 if char == 'E' else 270, t)
        if char == 'E': rect(p, 40, 0, 390, t)
    elif char == 'G':
        open_c(p, 252, 350, 212, 350, t, .21)
        rounded_rect(p, 250, 294, 190, t, min(18, t*.28)); rounded_rect(p, 376, 132, t, 168, min(18, t*.28))
    elif char == 'H':
        rect(p, 40, 0, t, CAP); rect(p, 396, 0, t, CAP); rect(p, 40, 320, 420, t)
    elif char == 'I': rect(p, 218, 0, t, CAP)
    elif char == 'J':
        rounded_rect(p, 345, 150, t, CAP-150, min(18, t*.28))
        p.moveTo((409, 150)); p.curveTo((409, 42), (328, -8), (218, -8)); p.curveTo((110, -8), (48, 47), (48, 160)); p.lineTo((112, 160)); p.curveTo((112, 85), (147, 54), (218, 54)); p.curveTo((286, 54), (345, 83), (345, 150)); p.closePath()
    elif char == 'K':
        rect(p, 40, 0, t, CAP); diagonal(p, 430, CAP, 104, 350, t); diagonal(p, 104, 350, 440, 0, t)
    elif char == 'L': rect(p, 40, 0, t, CAP); rect(p, 40, 0, 400, t)
    elif char == 'M':
        rect(p, 40, 0, t, CAP); rect(p, 430, 0, t, CAP); diagonal(p, 104, CAP, 250, 350, t); diagonal(p, 396, CAP, 250, 350, t)
    elif char == 'N':
        rect(p, 40, 0, t, CAP); rect(p, 396, 0, t, CAP); diagonal(p, 104, CAP, 396, 0, t)
    elif char == 'P': rect(p, 40, 0, t, CAP); ring(p, 245, 525, 190, 160, t)
    elif char == 'R': rect(p, 40, 0, t, CAP); ring(p, 245, 525, 190, 160, t); diagonal(p, 250, 360, 440, 0, t)
    elif char == 'S': smooth_s(p, 250, 350, 370, 700, t)
    elif char == 'T': rect(p, 40, CAP-t, 420, t); rect(p, 218, 0, t, CAP)
    elif char == 'U':
        rounded_rect(p, 40, 210, t, CAP-210, min(18, t*.28)); rounded_rect(p, 396, 210, t, CAP-210, min(18, t*.28))
        p.moveTo((40, 210)); p.curveTo((40, 68), (127, -8), (250, -8)); p.curveTo((373, -8), (460, 68), (460, 210)); p.lineTo((396, 210)); p.curveTo((396, 104), (345, 54), (250, 54)); p.curveTo((155, 54), (104, 104), (104, 210)); p.closePath()
    elif char == 'V': diagonal(p, 75, CAP, 250, 0, t); diagonal(p, 425, CAP, 250, 0, t)
    elif char == 'W': diagonal(p, 45, CAP, 140, 0, t); diagonal(p, 455, CAP, 360, 0, t); diagonal(p, 140, 0, 250, 390, t); diagonal(p, 360, 0, 250, 390, t)
    elif char == 'X': diagonal(p, 70, CAP, 430, 0, t); diagonal(p, 430, CAP, 70, 0, t)
    elif char == 'Y': diagonal(p, 70, CAP, 250, 350, t); diagonal(p, 430, CAP, 250, 350, t); rect(p, 218, 0, t, 350)
    elif char == 'Z': rect(p, 50, CAP-t, 400, t); diagonal(p, 430, CAP-t/2, 70, t/2, t); rect(p, 50, 0, 400, t)

def lower(p, char, s):
    t = s
    if char == 'a':
        # The bowl meets the terminal stem directly. A separate top bridge
        # created duplicate path segments in the variable font and propagated
        # that geometry into every accented/script derivative of `a`.
        ring(p, 228, 244, 150, 244, t); rounded_rect(p, 344, 0, t, XH, min(18, t*.28))
    elif char == 'o': ring(p, 250, 278, 180, 278, t)
    elif char == 'c': open_c(p, 255, 278, 185, 278, t, .29)
    elif char == 'e':
        open_c(p, 250, 278, 180, 278, t, .23); rounded_rect(p, 92, 246, 310, t, min(16, t*.24))
    elif char == 's': smooth_s(p, 250, 278, 330, 555, t)
    elif char == 'n': rounded_rect(p, 60, 0, t, XH, min(18, t*.28)); arch(p, 124, 344, 0, XH, t)
    elif char == 'm':
        rounded_rect(p, 40, 0, t, XH, min(18, t*.28)); arch(p, 104, 250, 0, XH, t); arch(p, 239, 374, 0, XH, t)
    elif char == 'h': rounded_rect(p, 60, 0, t, ASC, min(18, t*.28)); arch(p, 124, 344, 0, XH, t)
    elif char == 'u':
        rounded_rect(p, 60, 190, t, XH-190, min(18, t*.28)); rounded_rect(p, 344-t, 0, t, XH, min(18, t*.28))
        p.moveTo((60, 190)); p.curveTo((60, 67), (125, -4), (234, -4)); p.curveTo((320, -4), (344, 67), (344, 190)); p.lineTo((280, 190)); p.curveTo((280, 91), (263, 54), (234, 54)); p.curveTo((201, 54), (124, 91), (124, 190)); p.closePath()
    elif char == 'r':
        rounded_rect(p, 60, 0, t, XH, min(18, t*.28)); p.moveTo((124, 305)); p.curveTo((154, 474), (270, 555), (390, 472)); p.lineTo((390, 400)); p.curveTo((284, 450), (205, 417), (188, 305)); p.closePath()
    elif char == 't': rounded_rect(p, 215, 0, t, ASC, min(18, t*.28)); rounded_rect(p, 105, 360, 270, t, min(16, t*.24))
    elif char == 'f': rounded_rect(p, 215, 0, t, ASC, min(18, t*.28)); p.moveTo((215, 500)); p.curveTo((215, 670), (294, 770), (398, 734)); p.lineTo((398, 670)); p.curveTo((325, 687), (279, 632), (279, 500)); p.closePath(); rounded_rect(p, 105, 350, 290, t, min(16, t*.24))
    elif char == 'i': rounded_rect(p, 218, 0, t, XH-100, min(18, t*.28)); oval(p, 250, XH-30, t*.55, t*.55)
    elif char == 'j': rounded_rect(p, 218, DESC+20, t, XH-DESC-120, min(18, t*.28)); oval(p, 250, XH-30, t*.55, t*.55); p.moveTo((282, DESC+20)); p.curveTo((282, DESC), (247, DESC), (201, DESC)); p.lineTo((177, DESC)); p.lineTo((177, DESC+25)); p.lineTo((201, DESC+25)); p.curveTo((212, DESC+25), (218, DESC+22), (218, DESC+20)); p.closePath()
    elif char == 'l': rounded_rect(p, 218, 0, t, ASC, min(18, t*.28))
    elif char in 'bdpq':
        if char in 'bd': rounded_rect(p, 60 if char == 'b' else 376-t, 0, t, ASC, min(18, t*.28))
        else: rounded_rect(p, 60 if char == 'p' else 376-t, DESC, t, XH-DESC, min(18, t*.28))
        ring(p, 250, 278, 180, 278, t)
    elif char == 'g':
        ring(p, 228, 260, 150, 240, t); rounded_rect(p, 344, DESC, t, XH-DESC, min(18, t*.28)); p.moveTo((408, 0)); p.curveTo((408, DESC), (324, DESC), (230, DESC)); p.curveTo((173, DESC), (139, DESC+25), (128, DESC+64)); p.lineTo((192, DESC+64)); p.curveTo((205, DESC+35), (221, DESC+30), (245, DESC+30)); p.curveTo((305, DESC+30), (344, DESC+72), (344, 0)); p.closePath()
    elif char == 'k': rounded_rect(p, 60, 0, t, ASC, min(18, t*.28)); diagonal(p, 124, 278, 370, XH, t); diagonal(p, 124, 278, 380, 0, t)
    elif char == 'v': diagonal(p, 75, XH, 250, 0, t); diagonal(p, 425, XH, 250, 0, t)
    elif char == 'w': diagonal(p, 45, XH, 130, 0, t); diagonal(p, 455, XH, 370, 0, t); diagonal(p, 130, 0, 250, 300, t); diagonal(p, 370, 0, 250, 300, t)
    elif char == 'x': diagonal(p, 70, XH, 430, 0, t); diagonal(p, 430, XH, 70, 0, t)
    elif char == 'y': diagonal(p, 75, XH, 250, 0, t); diagonal(p, 425, XH, 250, 0, t); rect(p, 218, DESC, t, 100)
    elif char == 'z': rect(p, 70, XH-t, 360, t); diagonal(p, 410, XH-t/2, 90, t/2, t); rect(p, 70, 0, 360, t)

def figure(p, char, s):
    t = s
    if char == '0': ring(p, 250, 350, 180, 350, t)
    elif char == '1': rounded_rect(p, 218, 0, t, CAP, min(18, t*.28)); diagonal(p, 105, 560, 218, CAP, t)
    elif char == '2':
        p.moveTo((85, 570)); p.curveTo((107, 676), (187, 720), (258, 720)); p.curveTo((361, 720), (425, 645), (425, 524)); p.curveTo((425, 410), (305, 240), (142, 64)); p.lineTo((425, 64)); p.lineTo((425, 0)); p.lineTo((75, 0)); p.curveTo((253, 198), (361, 370), (361, 521)); p.curveTo((361, 610), (326, 656), (258, 656)); p.curveTo((208, 656), (161, 625), (149, 570)); p.closePath()
    elif char == '3': smooth_s(p, 250, 350, 338, 700, t); rounded_rect(p, 235, 316, 120, t, min(16, t*.24))
    elif char == '4': rounded_rect(p, 350-t, 0, t, CAP, min(18, t*.28)); diagonal(p, 80, 280, 250, CAP, t); rounded_rect(p, 80, 280, 330, t, min(16, t*.24))
    elif char == '5':
        p.moveTo((104, 700)); p.lineTo((402, 700)); p.lineTo((402, 636)); p.lineTo((168, 636)); p.lineTo((168, 425)); p.curveTo((210, 454), (245, 468), (286, 468)); p.curveTo((378, 468), (430, 385), (430, 240)); p.curveTo((430, 83), (356, -10), (243, -10)); p.curveTo((143, -10), (80, 44), (70, 133)); p.lineTo((134, 133)); p.curveTo((147, 82), (185, 54), (243, 54)); p.curveTo((324, 54), (366, 118), (366, 240)); p.curveTo((366, 350), (331, 404), (280, 404)); p.curveTo((240, 404), (201, 387), (168, 351)); p.lineTo((104, 351)); p.closePath()
    elif char == '6': ring(p, 250, 190, 175, 190, t); p.moveTo((75, 190)); p.curveTo((75, 505), (188, 710), (352, 710)); p.lineTo((385, 646)); p.curveTo((250, 636), (139, 492), (139, 220)); p.closePath()
    elif char == '7': rounded_rect(p, 70, CAP-t, 360, t, min(16, t*.24)); diagonal(p, 410, CAP-t/2, 170, 0, t)
    elif char == '8': ring(p, 250, 525, 165, 160, t); ring(p, 250, 175, 165, 160, t)
    elif char == '9': ring(p, 250, 510, 175, 190, t); p.moveTo((425, 510)); p.curveTo((425, 194), (312, -10), (148, -10)); p.lineTo((115, 54)); p.curveTo((250, 64), (361, 208), (361, 480)); p.closePath()

def punctuation(p, ch, s):
    t = max(s, 36)
    if ch == ' ': return
    if ch in '.': oval(p, 250, 35, t/2, t/2)
    elif ch == ',': oval(p, 250, 35, t/2, t/2); diagonal(p, 250, 20, 210, DESC/2, t/2)
    elif ch == ':': oval(p, 250, 390, t/2, t/2); oval(p, 250, 35, t/2, t/2)
    elif ch == ';': oval(p, 250, 390, t/2, t/2); oval(p, 250, 35, t/2, t/2); diagonal(p, 250, 20, 210, DESC/2, t/2)
    elif ch in '-_': rect(p, 90, 260 if ch == '-' else 0, 320, t)
    elif ch in "'`": diagonal(p, 250, XH, 210 if ch == '`' else 290, XH-90, t/2)
    elif ch == '"': diagonal(p, 190, XH, 150, XH-90, t/2); diagonal(p, 310, XH, 350, XH-90, t/2)
    elif ch == '!': rect(p, 218, 130, t, XH-130); oval(p, 250, 35, t/2, t/2)
    elif ch == '?': rect(p, 105, XH-t, 250, t); rect(p, 355-t, 300, t, XH-300); rect(p, 215, 190, t, 110); oval(p, 250, 35, t/2, t/2)
    elif ch in '()[]{}':
        left = ch in '([{'
        x = 150 if left else 350-t
        rect(p, x, 80, t, 540)
        if ch in '[]': rect(p, x if left else x-t, 620, 100, t); rect(p, x if left else x-t, 80, 100, t)
    elif ch in '/\\': diagonal(p, 120 if ch == '/' else 380, 0, 380 if ch == '/' else 120, CAP, t)
    elif ch == '+': rect(p, 90, 300, 320, t); rect(p, 218, 140, t, 380)
    elif ch == '=': rect(p, 90, 230, 320, t); rect(p, 90, 390, 320, t)
    elif ch == '*': diagonal(p, 130, 160, 370, 540, t); diagonal(p, 370, 160, 130, 540, t); rect(p, 90, 330, 320, t)
    elif ch == '#': rect(p, 160, 80, t, 540); rect(p, 300, 80, t, 540); rect(p, 80, 240, 340, t); rect(p, 80, 400, 340, t)
    elif ch == '%': oval(p, 135, 520, 55, 55); oval(p, 365, 180, 55, 55); diagonal(p, 110, 80, 390, 620, t)
    elif ch == '&': ring(p, 220, 220, 130, 180, t); diagonal(p, 110, 580, 390, 0, t); oval(p, 300, 520, 100, 120)
    elif ch == '@': ring(p, 250, 350, 210, 280, t); ring(p, 260, 350, 100, 120, t); rect(p, 320, 290, t, 150)
    else: rect(p, 80, 0, 340, t); rect(p, 80, CAP-t, 340, t); rect(p, 80, 0, t, CAP); rect(p, 420-t, 0, t, CAP)

def glyph_name(ch):
    if ch == ' ': return 'space'
    return ch if ch.isalpha() else f'uni{ord(ch):04X}'

def width_for(ch):
    if ch == ' ': return 250
    if ch in 'ilI.,:;!|\'`': return 250
    if ch in 'mwMW@#': return 560
    if ch in '()[]{}': return 310
    return 500

def draw_char(p, ch, stem):
    if 'A' <= ch <= 'Z': upper(p, ch, stem)
    elif 'a' <= ch <= 'z': lower(p, ch, stem)
    elif '0' <= ch <= '9': figure(p, ch, stem)
    else: punctuation(p, ch, stem)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--redraw', action='append', default=[], help='Redraw only a named glyph in every master.')
    parser.add_argument('--all-basic', action='store_true', help='Redraw every printable Basic Latin glyph in every master.')
    args = parser.parse_args()
    charset = ''.join(chr(code) for code in range(32, 127))
    for filename, stem in MASTERS:
        path = SOURCE / filename
        font = Font.open(path)
        if 'uni0020' in font:
            del font['uni0020']
        for ch in charset:
            name = glyph_name(ch)
            if (args.all_basic or name in args.redraw) and name in font:
                del font[name]
            if name in font: continue
            glyph = font.newGlyph(name); glyph.width = width_for(ch); glyph.unicodes = [ord(ch)]
            draw_char(glyph.getPen(), ch, stem)
        # UFOLib infers a "smooth" flag from very heavy curve handles. Keep
        # it explicit and identical in every master; curves interpolate from
        # their geometry, not this editor convenience flag.
        if args.all_basic or args.redraw:
            for ch in charset:
                for contour in font[glyph_name(ch)].contours:
                    for point in contour.points:
                        point.smooth = False
        font.features.text = """feature kern {
  pos A V -55;
  pos A W -42;
  pos A Y -60;
  pos T o -40;
  pos T a -35;
  pos V a -50;
  pos W a -35;
  pos Y o -60;
} kern;"""
        font.save(path, overwrite=True)
        print(f'Expanded {filename} to {len(font)} glyphs')

if __name__ == '__main__':
    main()
