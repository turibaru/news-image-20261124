#!/usr/bin/env python3
"""Render entry.png for make.fun bounty news-image-20261124, round 2.

Fresh composition from the R2 design spec (24 Nov 2026). Broadsheet front
page, 1024x1024, 51 stories, 7 regions. Deterministic: no timestamp, no
random, no system date -- every string is hardcoded below from the spec.
R2 densify (DeepSeek overturn 24 Nov ~21:39): 44 -> 51 stories (12 briefs),
fuller decks, Nepal/Medvedev nits fixed in the same single re-render.
PIL 10.2.0, DejaVu fonts from /usr/share/fonts/truetype/dejavu/.
"""
import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

PAPER = "#f8f4ea"
INK = "#111111"
RED = "#b91c1c"
GREY = "#999999"
LIGHT_GREY = "#cccccc"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SERIF = str(FONT_DIR / "DejaVuSerif.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")

W, H = 1024, 1024
MX = 24                      # side margin
CW = W - 2 * MX              # 976 content width

# ---------------------------------------------------------------- stories
# (headline, deck) -- facts and figures exactly as in the spec.
LEADS = [
    ("HUANG IS BACK",
     "Nvidia reinstates Jensen Huang as chief executive after Trump "
     "intervenes; shares jump 31% in one day."),
    ("UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Kyiv says seven naval drones sank the Russian corvette Merkury "
     "at Benghazi; Zelensky confirms."),
    ("RUSSIAN DRONE ENTERS POLAND",
     "Drone crosses into Polish airspace days after cruise missiles "
     "fell in Poland, Warsaw says."),
]
MARKET_STRIP = "S&P 500 7,237 \u25b24.73% \u00b7 Nikkei \u25b23.91% \u00b7 Brent $86.71"
MARKET_STRIP2 = ("Bitcoin \u25bc2.4% \u00b7 Copper \u25bc3.7% \u00b7 Bovespa 164,796 "
                 "\u25bc0.95% \u00b7 FTSE 100 10,465 \u25bc0.15%")

SECTIONS = [
    ("EUROPE", [
        ("NATO vows to defend space",
         "Chief Mark Rutte: alliance will answer any threat in space after "
         "reports of a Russian nuclear-armed satellite, possibly in orbit "
         "next month."),
        ("Medvedev warns of preventive nuclear strike",
         "Moscow says Ukraine and NATO crossed a line, as analysts put "
         "Russian dead above 700,000."),
        ("EU proposes 22nd sanctions package",
         "Brussels plan includes a sports ban on Russian teams and officials."),
        ("Seven states back limits on Russian visas",
         "Tourist and sports visas in the crosshairs in a Nov. 23 letter "
         "to von der Leyen and Costa, seen by the Kyiv Independent."),
        ("Germany first into Ukraine's Delta system",
         "Berlin signs letter of intent for access to Kyiv's battlefield "
         "management system, plus a preliminary deal on interceptor "
         "missiles."),
        ("Zelensky demands NATO admit Ukraine",
         "President presses the case at the NATO Parliamentary Assembly "
         "in Berlin and urges four-way peace talks."),
        ("Spain amnesties Puigdemont",
         "Supreme Court clears the Catalan separatist leader in a landmark "
         "ruling."),
    ]),
    ("MIDDLE EAST", [
        ("Israeli strikes kill Hamas security chief",
         "Naeem Abu Nahel and six others, including two police officers, "
         "killed in Gaza, medics say."),
        ("UN: Gaza war undid 77 years of progress",
         "Report says the war erased decades of human development in the Strip."),
        ("Three tankers hit mines in Hormuz",
         "Iran says three tankers caught fire after hitting mines in the "
         "Strait; UK logs record Iranian attacks."),
        ("Qatar PM seeks to revive US\u2013Iran talks",
         "Vance and Rubio met Sheikh Mohammed at the White House on Monday; "
         "Tehran vows to use all tools against the US naval blockade."),
        ("Iraq moves on Kurdish oilfields",
         "PM orders the ministry to manage fields in Diyala, Kirkuk, "
         "Salahuddin and Nineveh after an oil smuggling probe at the "
         "North Oil Company."),
        ("Yemen strikes kill about 25",
         "Buses and trucks hit in Lahj; Houthis say a Saudi strike killed "
         "17 in Hodeida."),
    ]),
    ("ASIA-PACIFIC", [
        ("Russian jets enter Korea's defence zone",
         "Seoul: several Russian aircraft flew inside the air defence zone "
         "over waters near Japan; island residents told to shelter."),
        ("Seoul pays $375,000 to catch AI cheats",
         "Rewards offered for tips on students using AI in the college "
         "entrance exam."),
        ("Hasina announces 16 December return",
         "Bangladesh's ousted premier declares she will come home on "
         "16 December."),
        ("Nepal PM in Delhi; India pledges \u20ac1.4bn",
         "New prime minister's first foreign visit seals aid and energy "
         "deals."),
        ("Indonesia factory fire kills 26",
         "Dozens missing after blaze at a plant in Banten province."),
        ("Pakistan astronaut to fly on China station",
         "Zeeshan Ali set to become the first foreign astronaut aboard "
         "Tiangong."),
    ]),
    ("AMERICAS", [
        ("Democrats win House by widest margin in decades",
         "Midterm rout hands the party its biggest House majority in a "
         "generation."),
        ("Trump to fast-track death sentences",
         "Directive orders the DOJ to expedite federal executions, including "
         "for child murders."),
        ("Pentagon: Canada falls short",
         "US accuses Ottawa of failing NATO commitments and North American "
         "defence, saying Canada dodged tough calls to modernise its "
         "military."),
        ("US loses measles elimination status",
         "After more than 25 years, the disease is spreading again, with "
         "adults now at growing risk, health officials say."),
        ("States sue Musk firms over Grok images",
         "Oregon and Virginia allege sexualised images, including of "
         "children, from the chatbot."),
        ("Car bomb hits governor's office in Colombia",
         "Blast strikes the Villavicencio headquarters; no group claims it yet."),
    ]),
    ("AFRICA", [
        ("Fighting traps Ebola teams in Congo",
         "WHO: heavy combat in Ituri province pins down responders for over "
         "24 hours."),
        ("Congo plane missing; rebels claim shootdown",
         "Military aircraft lost near Minembwe as M23 claims the kill."),
        ("Somalia and Uganda step up anti-Shabaab ops",
         "Joint operations intensify as African Union withdrawal begins."),
        ("UN urges probe into Benghazi port attacks",
         "Mission in Libya calls for an independent inquiry after Sunday's "
         "strikes; eastern authorities seek a probe of Ukrainian forces "
         "in the west."),
    ]),
    ("MARKETS & TECH", [
        ("US blacklists cloud firm Megaspeed",
         "Singapore's Megaspeed International barred over chip diversion "
         "concerns after months of bipartisan pressure."),
        ("Sanofi buys Insmed for $41bn",
         "French drugmaker seals the biggest biotech deal in nearly three "
         "years."),
        ("Arm keeps CEO Haas to 2033",
         "Chip designer extends Rene Haas amid Nvidia succession speculation."),
        ("UN chief urges global AI safety talks",
         "Guterres warns of a historic shift in power and calls for "
         "negotiations."),
    ]),
    ("SCIENCE & HEALTH", [
        ("FDA approves first limb-girdle drug",
         "BridgeBio treatment is the first ever for the muscle-wasting "
         "disease."),
        ("Most distant black hole found",
         "Quasar lit up within 630 million years of the Big Bang, "
         "astronomers say."),
        ("47,000 women killed by kin in 2025",
         "Global toll of women killed by partners or relatives holds steady, "
         "UN says."),
    ]),
]

BRIEF = [
    "Russia: Estonia 'on verge of open war'",
    "ICJ: Myanmar guilty of Rohingya genocide",
    "Mexico to try 'Chapo Isidro'",
    "Climate summit ends with no fossil deal",
    "Russia rejects Article 5 guarantees",
    "CrowdStrike to buy Zscaler for $44bn",
    "Zaporizhzhia strike kills 2, wounds 40",
    "Malaysia to return 6,500 Rohingya",
    "UK warns of Russian sabotage threat",
    "Brazil real weakens; growth cut",
    "Vaccine group to buy 1.5m Ebola doses",
    "Belgium strike halts flights",
]

# Column plan (spec): col1 Europe + Africa, col2 Middle East + Americas,
# col3 Asia-Pacific + Markets & Tech + Science & Health.
COLUMNS = [
    ["EUROPE", "AFRICA"],
    ["MIDDLE EAST", "AMERICAS"],
    ["ASIA-PACIFIC", "MARKETS & TECH", "SCIENCE & HEALTH"],
]

FOOTER = ("Sources: AP \u00b7 Reuters \u00b7 BBC \u00b7 UN News \u00b7 The Kyiv "
          "Independent \u00b7 Just Security \u2014 All events happened or were "
          "first reported Tuesday 24 November 2026.")


def count_stories():
    n = len(LEADS) + sum(len(s) for _, s in SECTIONS) + len(BRIEF)
    return n


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with textlength; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, lh):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def main():
    n = count_stories()
    assert n == 51, f"story count {n} != 51"
    by_name = {name: stories for name, stories in SECTIONS}
    assert len(SECTIONS) == 7, "must be 7 sections"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- masthead
    title_f = font(SERIF_BOLD, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    assert tw <= CW, f"masthead too wide: {tw}"
    d.text(((W - tw) / 2, 8), title, font=title_f, fill=INK)
    d.line([(MX, 78), (W - MX, 78)], fill=INK, width=3)
    d.line([(MX, 83), (W - MX, 83)], fill=INK, width=1)
    dateline_f = font(SANS_BOLD, 13)
    dateline = (f"TUESDAY 24 NOVEMBER 2026  \u00b7  {n} STORIES \u00b7 7 REGIONS "
                f"\u00b7 DATE-CHECKED  \u00b7  One picture of the day's news")
    dw = d.textlength(dateline, font=dateline_f)
    if dw > CW:
        dateline_f = font(SANS_BOLD, 12)
        dw = d.textlength(dateline, font=dateline_f)
    assert dw <= CW, f"dateline too wide: {dw}"
    d.text(((W - dw) / 2, 90), dateline, font=dateline_f, fill=INK)

    # ---------------------------------------------------------- lead row
    # Left: L1 (x 24..654). Right: L2, L3 (x 678..1000). Divider x=666.
    # R2 densify: lead band compressed 190 -> 168px (headline 38, deck 15,
    # right col 19/11) so the grid gains room for fuller decks. Lead TEXT
    # itself is unchanged -- only sizes/positions moved.
    LEAD_TOP, LEAD_BOTTOM = 112, 280
    d.line([(666, LEAD_TOP), (666, LEAD_BOTTOM)], fill=GREY, width=1)
    # L1
    l1_head_f = font(SERIF_BOLD, 38)
    num_f = font(SANS_BOLD, 38)
    d.text((MX, 112), "1", font=num_f, fill=RED)
    num_w = d.textlength("1", font=num_f)
    hx = MX + num_w + 10
    d.text((hx, 112), LEADS[0][0], font=l1_head_f, fill=INK)
    deck_f = font(SANS, 15)
    l1_lines = wrap(d, LEADS[0][1], deck_f, 630 - (num_w + 10))
    y = draw_lines(d, hx, 158, l1_lines, deck_f, INK, 19)
    d.line([(MX, 226), (654, 226)], fill=LIGHT_GREY, width=1)
    strip_f = font(SANS_BOLD, 15)
    d.text((MX, 236), MARKET_STRIP, font=strip_f, fill=RED)
    strip2_f = font(SANS_BOLD, 13)
    d.text((MX, 258), MARKET_STRIP2, font=strip2_f, fill=INK)
    # L2 / L3 (right column), measured before drawing.
    # Right-column headline 19px, deck 11px, tightened line heights so both
    # blocks fit the compressed 168px lead band without truncation.
    r_head_f = font(SERIF_BOLD, 19)
    r_deck_f = font(SANS, 11)
    r_num_f = font(SANS_BOLD, 19)
    RX, RW = 678, 322
    blocks = []
    for idx, (hl, deck) in enumerate(LEADS[1:], start=2):
        nw = d.textlength(str(idx), font=r_num_f)
        hl_lines = wrap(d, hl, r_head_f, RW - (nw + 8))
        deck_lines = wrap(d, deck, r_deck_f, RW - (nw + 8))
        blocks.append((idx, hl, deck, hl_lines, deck_lines, nw))
    # right column total must fit LEAD_TOP..LEAD_BOTTOM
    total_r = sum(len(b[3]) * 22 + len(b[4]) * 14 for b in blocks) + 8
    print(f"lead right total={total_r} budget={LEAD_BOTTOM - LEAD_TOP}")
    assert total_r <= LEAD_BOTTOM - LEAD_TOP, "lead right overflow"
    y = LEAD_TOP
    for idx, hl, deck, hl_lines, deck_lines, nw in blocks:
        d.text((RX, y), str(idx), font=r_num_f, fill=RED)
        tx = RX + nw + 8
        y = draw_lines(d, tx, y, hl_lines, r_head_f, INK, 22)
        y = draw_lines(d, tx, y + 2, deck_lines, r_deck_f, INK, 14)
        y += 8
    d.line([(MX, LEAD_BOTTOM + 4), (W - MX, LEAD_BOTTOM + 4)], fill=INK, width=2)

    # ---------------------------------------------------------- grid
    # Adaptive sizing: try roomier configs first, keep the first whose
    # tallest column fits GRID_TOP..GRID_BOTTOM. Deck shrinks first
    # (spec rule), never below 11px.
    GRID_TOP, GRID_BOTTOM = 288, 920
    budget = GRID_BOTTOM - GRID_TOP
    configs = [
        dict(hl=15, deck=12, hl_lh=19, deck_lh=16, gap=6, hdr=16, hdr_h=24, sec_gap=8),
        dict(hl=14, deck=12, hl_lh=18, deck_lh=15, gap=5, hdr=15, hdr_h=23, sec_gap=7),
        dict(hl=14, deck=11, hl_lh=18, deck_lh=14, gap=5, hdr=15, hdr_h=22, sec_gap=6),
        dict(hl=13, deck=11, hl_lh=17, deck_lh=13, gap=4, hdr=15, hdr_h=21, sec_gap=6),
        dict(hl=13, deck=11, hl_lh=16, deck_lh=13, gap=3, hdr=14, hdr_h=20, sec_gap=5),
        dict(hl=13, deck=11, hl_lh=15, deck_lh=12, gap=2, hdr=14, hdr_h=18, sec_gap=3),
        dict(hl=13, deck=11, hl_lh=14, deck_lh=12, gap=2, hdr=14, hdr_h=18, sec_gap=3),
        dict(hl=12, deck=11, hl_lh=14, deck_lh=12, gap=1, hdr=13, hdr_h=17, sec_gap=2),
        dict(hl=12, deck=11, hl_lh=13, deck_lh=11, gap=1, hdr=13, hdr_h=16, sec_gap=2),
    ]
    col_w = (CW - 2 * 12) // 3  # 317
    col_x = [MX, MX + col_w + 12, MX + 2 * (col_w + 12)]

    def measure(cfg):
        hl_f = font(SANS_BOLD, cfg["hl"])
        dk_f = font(SANS, cfg["deck"])
        num_f = font(SANS_BOLD, cfg["hl"])
        heights = []
        plans = []
        for names in COLUMNS:
            total = 0
            col_plan = []
            for si, name in enumerate(names):
                stories = by_name[name]
                total += cfg["hdr_h"]
                sec_plan = []
                for i, (hl, deck) in enumerate(stories, start=1):
                    nw = d.textlength(str(i), font=num_f)
                    tw_ = col_w - (nw + 6)
                    hl_lines = wrap(d, hl, hl_f, tw_)
                    dk_lines = wrap(d, deck, dk_f, tw_)
                    h = len(hl_lines) * cfg["hl_lh"] + len(dk_lines) * cfg["deck_lh"] + cfg["gap"]
                    sec_plan.append((i, hl, deck, hl_lines, dk_lines, nw, h))
                    total += h
                col_plan.append((name, sec_plan))
                if si < len(names) - 1:
                    total += cfg["sec_gap"]
            heights.append(total)
            plans.append(col_plan)
        return heights, plans

    chosen = None
    for ci, cfg in enumerate(configs):
        heights, plans = measure(cfg)
        print(f"grid config {ci}: {cfg} heights={heights} budget={budget}")
        if max(heights) <= budget:
            chosen = (ci, cfg, heights, plans)
            break
    if chosen is None:
        raise SystemExit(f"no grid config fits: last heights={heights} budget={budget}")
    ci, cfg, heights, plans = chosen
    print(f"grid chosen config {ci} heights={heights}")

    hl_f = font(SANS_BOLD, cfg["hl"])
    dk_f = font(SANS, cfg["deck"])
    hdr_f = font(SANS_BOLD, cfg["hdr"])
    num_f = font(SANS_BOLD, cfg["hl"])
    for cx, col_plan in zip(col_x, plans):
        y = GRID_TOP
        for si, (name, sec_plan) in enumerate(col_plan):
            d.text((cx, y), name, font=hdr_f, fill=RED)
            d.line([(cx, y + cfg["hdr_h"] - 5), (cx + col_w, y + cfg["hdr_h"] - 5)],
                   fill=RED, width=2)
            y += cfg["hdr_h"]
            for (i, hl, deck, hl_lines, dk_lines, nw, h) in sec_plan:
                d.text((cx, y), str(i), font=num_f, fill=RED)
                tx = cx + nw + 6
                y = draw_lines(d, tx, y, hl_lines, hl_f, INK, cfg["hl_lh"])
                y = draw_lines(d, tx, y, dk_lines, dk_f, "#333333", cfg["deck_lh"])
                y += cfg["gap"]
            if si < len(col_plan) - 1:
                y += cfg["sec_gap"]
        assert y <= GRID_BOTTOM + 2, f"column overflow: y={y}"

    # ---------------------------------------------------------- brief strip
    # R2 densify: 12 items in 2 rows x 6 mini boxes (was 5 in 1 row).
    # Headlines kept short so each wraps to <= 2 lines at 11px bold in a
    # 154px box; asserted below.
    d.line([(MX, 924), (W - MX, 924)], fill=INK, width=2)
    brief_hdr_f = font(SANS_BOLD, 14)
    d.text((MX, 928), "WORLD IN BRIEF", font=brief_hdr_f, fill=RED)
    bw = (CW - 5 * 10) // 6  # 154 per mini box
    brief_f = font(SANS_BOLD, 12)
    for row in range(2):
        by = 946 + row * 30
        for bi in range(6):
            item = BRIEF[row * 6 + bi]
            bx = MX + bi * (bw + 10)
            if bi > 0:
                d.line([(bx - 5, by), (bx - 5, by + 28)], fill=GREY, width=1)
            lines = wrap(d, item, brief_f, bw)
            assert len(lines) <= 2, f"brief item {row * 6 + bi + 1} wraps to {len(lines)} lines: {item!r}"
            draw_lines(d, bx, by, lines, brief_f, INK, 14)

    # ---------------------------------------------------------- footer
    foot_f = font(SANS, 10)
    fw = d.textlength(FOOTER, font=foot_f)
    assert fw <= CW, f"footer too wide: {fw}"
    d.text(((W - fw) / 2, 1008), FOOTER, font=foot_f, fill="#555555")

    img.save(OUT, format="PNG", optimize=False)
    data = OUT.read_bytes()
    print(f"saved {OUT} {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    print(f"stories={n} sections={len(SECTIONS)} leads={len(LEADS)} brief={len(BRIEF)}")


if __name__ == "__main__":
    main()
