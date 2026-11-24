#!/usr/bin/env python3
"""Build-time renderer for news-image-20261124 (round 1).

Renders entry.png (1024x1024) — a dense front page summing up the world's
news of Tuesday 24 November 2026. Deterministic: no timestamps, no random
seeds; two runs must be byte-identical.

Story list (41 total):
  Tier A (spec): 26 — happened and reported 24 Nov 2026.
  Tier A top-up (verified by builder, 24 Nov): 2 — Nvidia reinstates
    Jensen Huang as CEO (BBC, 24 Nov); CrowdStrike buys Zscaler for
    $44bn (Reuters, 24 Nov).
  Tier B (spec): 8 — first reported 24 Nov, event 23 Nov; small items only.
  Tier C verified by builder (24 Nov): 2 — Penny Wong AI speech delivered
    to the Senate, 24 Nov; Australia-Singapore leaders' meeting held in
    Canberra, 24 Nov, pacts signed.
  Tier C scheduled only (result not yet known at render time, labelled
    SCHEDULED TODAY, never stated as a result): 3 — World Chess Game 1
    (15:00 CET), Portugal budget vote (15:00 Lisbon), Huawei Mate X8
    launch (14:30 Beijing).
  Tier C dropped (no result before round 1 ends 19:00 WIB): CAS AFCON
    verdict (afternoon GMT, unconfirmed leak only), Progress MS-36 launch
    (17:13 WIB), Amazon Leo LE-04 launch (17:45 WIB).
  Hormuz item is attributed as an IRGC claim only, never stated as fact.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = H = 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)
RED = (185, 28, 28)
GREY = (90, 90, 90)
LEAD_BG = (245, 240, 230)

# (section, headline, summary) — headlines <= ~62 chars, summaries <= ~105.
LEADS = [
    ("LEAD 1 — EUROPE",
     "Russian drone briefly enters Polish airspace; NATO scrambles AWACS",
     "Poland does not shoot it down; alliance puts early-warning jets up in response."),
    ("LEAD 2 — EAST ASIA",
     "Russian jets enter Korea's defence zone; Ulleung evacuation alert",
     "Seoul scrambles fighters, warns islanders, then lifts the alert; summons Russian attache."),
    ("LEAD 3 — NORTH AMERICA",
     "US blacklists Megaspeed and six firms after Nvidia scandal",
     "Washington adds the AI firm at the centre of the Nvidia scandal to its trade blacklist."),
]

ITEMS = [
    # EUROPE (8)
    ("EUROPE", "Burnham: can he calm the EU debate?",
     "BBC asks if the new leader can quiet Britain's Europe row."),
    ("EUROPE", "No 10 North faces scrutiny as Burnham's 10-year plan nears",
     "Scrutiny grows ahead of the decade-long plan. (BBC, 24 Nov)"),
    ("EUROPE", "Green leader Polanski backs NATO and keeping nuclear arms",
     "Polanski endorses a report defending NATO membership."),
    ("EUROPE", "New £437m Museum of London opens its doors",
     "Guardian reviews the new museum, fatberg installation included."),
    ("EUROPE", "Macfarlane: faith in COP to deliver climate change is 'misplaced'",
     "Writer says COP31's failure shows the talks cannot deliver."),
    ("EUROPE", "Zelenskyy warns of new Russian strikes, urges more air defences",
     "Kyiv presses allies for more air-defence missiles."),
    ("EUROPE", "SCHEDULED TODAY: Chess title Game 1 opens in Geneva, 15:00 CET",
     "Champion Gukesh meets challenger Sindarov, both aged 20."),
    ("EUROPE", "SCHEDULED TODAY: Portugal votes on 2027 budget, 15:00 Lisbon",
     "Final parliament vote as unions strike and protest outside."),
    # EAST ASIA & PACIFIC (6)
    ("EAST ASIA & PACIFIC", "China sentences official to death for spying, leaking secrets",
     "Beijing: the official, surnamed Ma, passed state secrets. (AP)"),
    ("EAST ASIA & PACIFIC", "AI method maps membrane proteins to 2.7 angstroms",
     "Chinese team publishes the method in PNAS, 24 Nov."),
    ("EAST ASIA & PACIFIC", "Fiji shuts all schools for five days as El Nino drought deepens",
     "Closure runs 30 Nov–4 Dec to protect children."),
    ("EAST ASIA & PACIFIC", "Remote Kanton Island evacuated with a day's notice",
     "40–50 Kiribati residents moved to Tarawa."),
    ("EAST ASIA & PACIFIC", "Australia elevates AI to a national-security challenge",
     "Foreign Minister Penny Wong's major speech to parliament."),
    ("EAST ASIA & PACIFIC", "Australia and Singapore sign supply, carbon and AI pacts",
     "Canberra meeting yields two pacts and an AI statement."),
    # SOUTH ASIA (5)
    ("SOUTH ASIA", "Excavators in sacred Kashmir lake spark anger",
     "Machines at Sheshnag lake draw public fury. (Al Jazeera)"),
    ("SOUTH ASIA", "Delhi air 'poor' as AQI hits 242; Sirifort worst at 336",
     "Ten monitoring stations rated 'very poor' on Tuesday morning."),
    ("SOUTH ASIA", "Banten candy-factory fire toll rises to 26 dead, 34 missing",
     "DNA identification continues after the 21 Nov blaze."),
    ("SOUTH ASIA", "India holds No. 3 in Asia Power Index; Modi rated top leader",
     "Lowy Institute scores India 40.5, behind the US and China."),
    ("SOUTH ASIA", "Myanmar pushes green energy, digital trade at ASEAN-China Week",
     "Chongqing event promotes cooperation. (reported 24 Nov)"),
    # MIDDLE EAST (3)
    ("MIDDLE EAST", "Iran claims three tankers caught fire after hitting Hormuz mines",
     "IRGC claim only; no confirmation, no ship names."),
    ("MIDDLE EAST", "Qatar PM mediates Iran–US tensions after meeting Rubio",
     "Doha carries on mediation after Washington talks."),
    ("MIDDLE EAST", "Flydubai cleared to resume flights to Tel Aviv",
     "Airline gets approval to restart the route."),
]
ITEMS += [
    # AFRICA (7)
    ("AFRICA", "Borno school enrolment jumps to 1,418,279 pupils",
     "Nigeria's Borno state reports a surge in pupils."),
    ("AFRICA", "Abia governor orders probe after boy, 8, dies in school collapse",
     "Punch reports the inquiry into the 20 Nov collapse."),
    ("AFRICA", "Kenya takes on Sh233bn in new loans in four months",
     "Government borrowing revealed in new figures."),
    ("AFRICA", "Ghana hostel investors may wait 30 years to break even",
     "Developers' group GREDA warns on student housing returns."),
    ("AFRICA", "Prosecutors seek guilty verdict in Mapisa-Nqakula trial",
     "Ex-speaker's defence calls the claims 'fabricated'."),
    ("AFRICA", "Namibia pulls ahead of South Africa in Orange Basin oil race",
     "Offshore exploration contest heats up."),
    ("AFRICA", "Dust cuts visibility across Mali, 23–29 Nov",
     "Haze warning covers the week."),
    # AMERICAS (6)
    ("AMERICAS", "US appeals court revives Trump's bid to move hush-money case",
     "Court revives bid to shift the case to federal court."),
    ("AMERICAS", "Trump at DOJ: seek death penalty for murder, rape, child cases",
     "Also attacks Newsom's commutation of 548 death sentences."),
    ("AMERICAS", "Democrats widen Congress lead: 258 House seats, 56 in Senate",
     "Biggest House majority since 1992. (reported 24 Nov)"),
    ("AMERICAS", "Bukele names three Salvadoran soldiers killed in Haiti mission",
     "Troops died in the anti-gang mission last week."),
    ("AMERICAS", "Drone attack on Colombia police base injures 3, damages 60 homes",
     "Baby of 18 months hurt in Cucuta; 2nd strike in Curumani."),
    ("AMERICAS", "UN chief urges a global AI safety framework within a year",
     "Guterres speaks in Bridgetown, Barbados. (reported 24 Nov)"),
    # MARKETS & TECH (3)
    ("MARKETS & TECH", "Nvidia reinstates Jensen Huang as CEO after spy-affair row",
     "Trump says 'I made the deal' to bring him back. (BBC, 24 Nov)"),
    ("MARKETS & TECH", "CrowdStrike snaps up Zscaler in a $44bn deal",
     "Cyber deal announced as threats mount. (Reuters, 24 Nov)"),
    ("MARKETS & TECH", "SCHEDULED TODAY: Huawei launches Mate X8 foldable, 14:30 Beijing",
     "Mate 90 Air and Watch Air join the launch event."),
]

TIMELINE = ("STILL TO COME TODAY  •  14:30 Beijing: Huawei Mate X8  •  "
             "15:00 CET: Chess Game 1, Geneva  •  15:00 Lisbon: Portugal budget vote")


def font(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(draw, text, fnt, width, max_lines=None):
    """Greedy word wrap measured with the real font; deterministic."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # Ellipsis on the last line if it was cut.
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > width:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] += "…"
    return lines


def text_h(draw, lines, fnt, leading):
    return len(lines) * leading


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 22  # side margin

    # ---- Masthead ----
    f_mast = font(48, bold=True)
    d.text((W // 2, 10), "THE WORLD IN ONE DAY", font=f_mast, fill=INK, anchor="ma")
    f_date = font(33, bold=True)
    d.text((W // 2, 64), "TUESDAY 24 NOVEMBER 2026", font=f_date, fill=RED, anchor="ma")
    d.line([(mx, 110), (W - mx, 110)], fill=INK, width=3)
    d.line([(mx, 115), (W - mx, 115)], fill=INK, width=1)
    f_sub = font(13, bold=True)
    d.text((W // 2, 122), "41 STORIES  •  7 REGIONS  •  EVERY STORY DATED TUESDAY 24 NOVEMBER 2026",
           font=f_sub, fill=INK, anchor="ma")

    # ---- Three leads ----
    lead_y, lead_h = 146, 138
    col_w = (W - 2 * mx - 2 * 12) // 3
    f_tag = font(11, bold=True)
    f_lh = font(16, bold=True)
    f_ls = font(10)
    for i, (tag, head, summ) in enumerate(LEADS):
        x0 = mx + i * (col_w + 12)
        d.rectangle([x0, lead_y, x0 + col_w, lead_y + lead_h], fill=LEAD_BG,
                    outline=INK, width=2)
        d.text((x0 + 10, lead_y + 7), tag, font=f_tag, fill=RED)
        hl = wrap(d, head, f_lh, col_w - 20, max_lines=3)
        y = lead_y + 26
        for ln in hl:
            d.text((x0 + 10, y), ln, font=f_lh, fill=INK)
            y += 20
        sl = wrap(d, summ, f_ls, col_w - 20, max_lines=3)
        for ln in sl:
            d.text((x0 + 10, y), ln, font=f_ls, fill=INK)
            y += 13

    # ---- Body: 3 columns, greedy height-balanced packing ----
    body_y0, body_y1 = 290, 952
    body_h = body_y1 - body_y0
    col_xs = [mx, mx + 334, mx + 668]
    col_w2 = 312
    f_sec = font(12, bold=True)
    f_h = font(12, bold=True)
    f_s = font(10)
    SEC_H = 18
    ITEM_GAP = 4

    # Measure every item.
    measured = []
    for sec, head, summ in ITEMS:
        hl = wrap(d, head, f_h, col_w2, max_lines=2)
        sl = wrap(d, summ, f_s, col_w2, max_lines=1)
        h = len(hl) * 13 + len(sl) * 11 + ITEM_GAP
        measured.append((sec, hl, sl, h))

    # Greedy: place items in order into the currently shortest column.
    cols = [[], [], []]
    col_h = [0, 0, 0]
    col_sec = [None, None, None]
    for sec, hl, sl, h in measured:
        c = col_h.index(min(col_h))
        extra = SEC_H if col_sec[c] != sec else 0
        cols[c].append((sec, hl, sl, h, extra > 0))
        col_h[c] += h + extra
        col_sec[c] = sec
    assert max(col_h) <= body_h, f"body overflow: {col_h} > {body_h}"

    for ci, x0 in enumerate(col_xs):
        y = body_y0
        for sec, hl, sl, h, show_sec in cols[ci]:
            if show_sec:
                d.text((x0, y), sec, font=f_sec, fill=RED)
                d.line([(x0, y + 14), (x0 + col_w2, y + 14)], fill=INK, width=1)
                y += SEC_H
            for ln in hl:
                d.text((x0, y), ln, font=f_h, fill=INK)
                y += 13
            for ln in sl:
                d.text((x0, y), ln, font=f_s, fill=(40, 40, 40))
                y += 11
            y += ITEM_GAP

    # ---- Timeline strip (scheduled events, labelled as still to come) ----
    d.rectangle([mx, 956, W - mx, 982], fill=INK)
    f_tl = font(12, bold=True)
    d.text((W // 2, 960), TIMELINE, font=f_tl, fill=(255, 255, 255), anchor="ma")

    # ---- Footer: date repeated, giant ----
    d.line([(mx, 990), (W - mx, 990)], fill=INK, width=1)
    f_ft = font(13, bold=True)
    d.text((W // 2, 996), "TUESDAY 24 NOVEMBER 2026  •  THE WORLD IN ONE DAY  •  41 STORIES, 7 REGIONS",
           font=f_ft, fill=INK, anchor="ma")

    img.save(os.path.join(HERE, "entry.png"))
    print(f"rendered entry.png  cols={col_h}  stories={len(LEADS) + len(ITEMS)}")


if __name__ == "__main__":
    main()
