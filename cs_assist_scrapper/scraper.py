# scraper.py
# ASSIST CS -> UCLA / UCB / UCSD articulation scraper
# UI layout: Academic Year • Institution • Agreements with Other Institutions • View Agreements
# Headless by default, strict "Computer Science" major, latest academic year
import json

import argparse
import re
import sys
from dataclasses import dataclass
from typing import List, Dict

import pandas as pd
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PWTimeout,
    Error as PWError,
)

TOP_ALT_COMMUNITY_COLLEGES = [
    "Diablo Valley College",
    "Laney College",
    "De Anza College",
    "Foothill College",
    "Santa Monica College",
    "Pasadena City College",
    "City College of San Francisco",
    "San Diego Mesa College",
    "Irvine Valley College",
    "Mission College",
]


# Community colleges to search when the home CC has "No Course Articulated"
OTHER_COMMUNITY_COLLEGES = [
    "Diablo Valley College",
    "De Anza College",
    "Santa Monica College",
    "San Diego Mesa College",
    "Pasadena City College",
    "Foothill College",
    "Irvine Valley College",
    "Mission College",
    "City College of San Francisco",
]

UNIVERSITY_ONLY_PATTERN = re.compile(
    r"this\s*course\s*must\s*be\s*taken\s*at\s*the\s*university\s*after\s*transfer",
    re.I,
)

def is_university_only(cc_course: str) -> bool:
    """
    Detect rows like 'This course must be taken at the university after transfer'
    even if they've been normalized/squashed (e.g. THISCOURSEMUSTBETAKENATTHEUNIVERSITYAFTERTRANSFER).
    """
    s = (cc_course or "").strip()
    if not s:
        return False
    return bool(UNIVERSITY_ONLY_PATTERN.search(s.lower()))


NO_ARTICULATION_PATTERN = re.compile(r"no\s*course\s*articulated", re.I)

def is_no_articulation(cc_course: str) -> bool:
    s = (cc_course or "").strip()
    if not s:
        return False
    s_norm = re.sub(r"\s+", " ", s)
    return bool(NO_ARTICULATION_PATTERN.search(s_norm))



UC_TARGETS = [
    ("University of California, Los Angeles", "ucla.csv"),
    ("University of California, Berkeley", "ucb.csv"),
    ("University of California, San Diego", "ucsd.csv"),
]

MAJOR_EXACT = "Computer Science"

UC_NAME_ALIASES = {
    "uc berkeley": "University of California, Berkeley",
    "university of california, berkeley": "University of California, Berkeley",

    "ucla": "University of California, Los Angeles",
    "uc la": "University of California, Los Angeles",
    "university of california, los angeles": "University of California, Los Angeles",

    "ucsd": "University of California, San Diego",
    "uc san diego": "University of California, San Diego",
    "university of california, san diego": "University of California, San Diego",
}

def normalize_uc_name(name: str) -> str:
    key = name.strip().lower()
    return UC_NAME_ALIASES.get(key, name)



@dataclass
class MappingRow:
    cc_course: str
    uc_course: str
    note: str
    uc_campus: str


# ------------------ helpers ------------------ #

def log(msg: str):
    print(msg, flush=True)


def nz(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def normalize_course(s: str) -> str:
    s = nz(s).upper()
    # "CS   61 A" -> "CS 61A"
    s = re.sub(r"(\D)\s+(\d)", r"\1 \2", s)
    s = re.sub(r"\s+([A-Z0-9])", r"\1", s)
    return s


def dataframe_from_rows(rows: List[MappingRow]) -> pd.DataFrame:
    df = pd.DataFrame(
        [
            {
                "uc_campus": r.uc_campus,
                "cc_course": normalize_course(r.cc_course),
                "uc_course": normalize_course(r.uc_course),
                "note": nz(r.note),
            }
            for r in rows
        ]
    )
    if not df.empty:
        df = df[(df["cc_course"] != "") & (df["uc_course"] != "")]
        df = df.drop_duplicates()
    return df


# ------------------ navigation ------------------ #

def go_home(page):
    # Load homepage
    page.goto("https://assist.org/", wait_until="load")
    # Give SPA time to hydrate
    page.wait_for_timeout(1500)

    # ✅ Only wait for Institution + Agreements dropdowns
    # Use .first to avoid strict mode when multiple matches exist
    page.get_by_label("Institution").first.wait_for(timeout=15000)
    page.get_by_label("Agreements with Other Institutions").first.wait_for(timeout=15000)


def get_all_community_colleges(page) -> List[str]:
    """
    Use the ASSIST 'Institution' dropdown to collect all California community colleges.
    We treat any option containing 'College' as a CC (ASSIST is CA-only).
    """
    go_home(page)  # make sure we’re on the home page

    # Open the Institution combobox (same one we use for select_cc_institution)
    combo = page.get_by_role(
        "combobox",
        name=re.compile(r"^Institution$", re.I)
    ).first

    combo.click()
    page.wait_for_timeout(500)

    # Try to force-load as many options as possible (virtualized lists)
    for _ in range(30):
        page.keyboard.press("End")
        page.wait_for_timeout(100)

    # Collect visible option texts
    option_texts = page.get_by_role("option").all_text_contents()
    colleges = sorted(
        {nz(t) for t in option_texts if "College" in t}
    )

    log(f"[INFO] Detected {len(colleges)} community colleges from ASSIST.")
    return colleges


def select_academic_year(page):
    """
    Pick the latest academic year for the AGREEMENTS flow.
    We avoid strict get_by_label() and just click the first dropdown
    associated with agreements-by-year.
    """
    try:
        # Prefer the "agreements" academic year search box
        # (Playwright showed its accessible name as "Search agreements by academic")
        combo = page.get_by_role(
            "textbox",
            name=re.compile("Search agreements by academic", re.I)
        ).first

        if combo.count():
            combo.click()
            page.wait_for_timeout(200)
            # Choose first option (latest year)
            page.locator("[role='option']").first.click(timeout=8000)
            page.wait_for_timeout(200)
            return
    except Exception:
        pass

    # Fallback: click any thing labelled Academic Year and pick first option
    try:
        label = page.locator("label:has-text('Academic Year')").first
        if label.count():
            for_id = label.get_attribute("for")
            if for_id:
                el = page.locator(f"#{for_id}")
            else:
                el = label
            el.click()
            page.wait_for_timeout(200)
            page.locator("[role='option']").first.click(timeout=8000)
            page.wait_for_timeout(200)
    except Exception:
        # If everything fails, just move on; some flows already have a year selected
        pass



def select_cc_institution(page, cc_name: str):
    """
    Select student's community college using the 'Institution' dropdown.
    Tries several strategies (combobox role, label+for, placeholder).
    """
    tried = []

    # 1) Try ARIA combobox with accessible name "Institution"
    try:
        combo = page.get_by_role(
            "combobox",
            name=re.compile(r"^Institution$", re.I)
        ).first
        if combo.count():
            combo.click()
            # Try inner input if present
            inner_input = combo.locator("input").first
            if inner_input.count():
                inner_input.fill(cc_name)
            else:
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(cc_name, delay=20)
            page.get_by_role(
                "option",
                name=re.compile(re.escape(cc_name), re.I)
            ).first.click(timeout=8000)
            return
        tried.append("combobox: Institution")
    except Exception:
        tried.append("combobox: Institution")

    # 2) Fallback: label + for attribute
    try:
        inst_label = page.locator(
            "label",
            has_text=re.compile(r"^Institution$", re.I)
        ).first
        if inst_label.count():
            for_id = inst_label.get_attribute("for")
            if for_id:
                combo = page.locator(f"#{for_id}")
            else:
                # If no 'for', clicking the label usually focuses the control
                inst_label.click()
                combo = page.locator("input").filter(
                    has=inst_label
                ).first
            combo.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.type(cc_name, delay=20)
            page.get_by_role(
                "option",
                name=re.compile(re.escape(cc_name), re.I)
            ).first.click(timeout=8000)
            return
        tried.append("label+for: Institution")
    except Exception:
        tried.append("label+for: Institution")

    # 3) Fallback: first "Search for an institution" field
    try:
        boxes = page.get_by_placeholder(
            re.compile("Search for an institution", re.I)
        )
        if boxes.count() >= 1:
            box = boxes.nth(0)
            box.click()
            box.fill(cc_name)
            page.get_by_role(
                "option",
                name=re.compile(re.escape(cc_name), re.I)
            ).first.click(timeout=8000)
            return
        tried.append("placeholder[0]")
    except Exception:
        tried.append("placeholder[0]")

    raise RuntimeError(
        f"Could not select CC institution '{cc_name}' using methods: {tried}"
    )



def select_uc_institution(page, uc_name: str):
    """
    Select target UC using the 'Agreements with Other Institutions' dropdown.
    """
    tried = []

    # 1) ARIA combobox by accessible name
    try:
        combo = page.get_by_role(
            "combobox",
            name=re.compile(r"Agreements with Other Institutions", re.I)
        ).first
        if combo.count():
            combo.click()
            inner_input = combo.locator("input").first
            if inner_input.count():
                inner_input.fill(uc_name)
            else:
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.type(uc_name, delay=20)
            page.get_by_role(
                "option",
                name=re.compile(re.escape(uc_name), re.I)
            ).first.click(timeout=8000)
            return
        tried.append("combobox: Agreements with Other Institutions")
    except Exception:
        tried.append("combobox: Agreements with Other Institutions")

    # 2) Label + for attribute
    try:
        inst_label = page.locator(
            "label",
            has_text=re.compile(r"Agreements with Other Institutions", re.I)
        ).first
        if inst_label.count():
            for_id = inst_label.get_attribute("for")
            if for_id:
                combo = page.locator(f"#{for_id}")
            else:
                inst_label.click()
                combo = page.locator("input").filter(
                    has=inst_label
                ).first
            combo.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            page.keyboard.type(uc_name, delay=20)
            page.get_by_role(
                "option",
                name=re.compile(re.escape(uc_name), re.I)
            ).first.click(timeout=8000)
            return
        tried.append("label+for: Agreements with Other Institutions")
    except Exception:
        tried.append("label+for: Agreements with Other Institutions")

    # 3) Fallback: second "Search for an institution" field
    try:
        boxes = page.get_by_placeholder(
            re.compile("Search for an institution", re.I)
        )
        if boxes.count() >= 2:
            box = boxes.nth(1)
            box.click()
            box.fill(uc_name)
            page.get_by_role(
                "option",
                name=re.compile(re.escape(uc_name), re.I)
            ).first.click(timeout=8000)
            return
        tried.append("placeholder[1]")
    except Exception:
        tried.append("placeholder[1]")

    raise RuntimeError(
        f"Could not select UC institution '{uc_name}' using methods: {tried}"
    )



def click_view_agreements(page):
    """
    Click 'View Agreements' button after year + institutions are selected.
    Wait until it becomes enabled.
    """
    btn = page.get_by_role(
        "button", name=re.compile("View Agreements", re.I)
    ).first
    # Wait up to ~30 seconds for it to become enabled
    for _ in range(60):
        try:
            if btn.is_enabled():
                btn.click()
                page.wait_for_timeout(800)
                return
        except Exception:
            pass
        page.wait_for_timeout(500)
    raise RuntimeError("View Agreements button never became enabled.")


def go_to_major_view(page):
    """
    After 'View Agreements', try to get to a page that lists majors.
    We look for tabs/buttons/links mentioning 'Major' or 'By Major'.
    If nothing is found, we assume we're already there.
    """
    # 1) Try tabs first
    for pattern in [r"By Major", r"Major Agreements", r"Articulation by Major", r"Majors"]:
        tab = page.get_by_role("tab", name=re.compile(pattern, re.I)).first
        if tab.count() and tab.is_visible():
            try:
                tab.click()
                page.wait_for_timeout(600)
                return
            except Exception:
                pass

    # 2) Try buttons
    for pattern in [r"By Major", r"Major"]:
        btn = page.get_by_role("button", name=re.compile(pattern, re.I)).first
        if btn.count() and btn.is_visible():
            try:
                btn.click()
                page.wait_for_timeout(600)
                return
            except Exception:
                pass

    # 3) Try links
    for pattern in [r"By Major", r"Major"]:
        link = page.get_by_role("link", name=re.compile(pattern, re.I)).first
        if link.count() and link.is_visible():
            try:
                link.click()
                page.wait_for_timeout(600)
                return
            except Exception:
                pass

    # If nothing was clickable, we just proceed – some pages drop you straight into a major list.




def select_major_cs(page):
    """
    Select the pure 'Computer Science' major (not CSE/Engineering).

    Strategy:
      1. Use a 'Search majors' textbox if present to filter with 'Computer Science'.
      2. Among matches, prefer:
         - exact 'Computer Science'
         - then names starting with 'Computer Science'
         - avoid 'Engineering' when possible.
    """
    # 1. Try to locate a major search textbox
    major_search = None

    # (a) By accessible name like "Search majors" / "Search for a major"
    try:
        major_search = page.get_by_role(
            "textbox",
            name=re.compile(r"search.*major", re.I)
        ).first
        if major_search.count() == 0:
            major_search = None
    except Exception:
        major_search = None

    # (b) Fallback: placeholder text including "major"
    if major_search is None:
        try:
            major_search = page.get_by_placeholder(
                re.compile(r"search.*major", re.I)
            ).first
            if major_search.count() == 0:
                major_search = None
        except Exception:
            major_search = None

    # If we found a search box, type "Computer Science" into it
    if major_search is not None and major_search.is_visible():
        major_search.click()
        try:
            major_search.fill("")
        except Exception:
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
        major_search.type("Computer Science", delay=20)
        page.wait_for_timeout(500)

    # Helper to choose the best "Computer Science" entry
    def click_best(loc):
        count = loc.count()
        if count == 0:
            return False

        exact_idx = None
        prefix_idx = None
        any_idx = None

        for i in range(count):
            txt = nz(loc.nth(i).inner_text())
            lower = txt.lower()

            if "computer science" not in lower:
                continue

            # normalize for exact comparison
            norm = re.sub(r"\s+", " ", lower).strip()

            if norm == "computer science":
                exact_idx = i
                break  # best possible
            elif norm.startswith("computer science") and "engineering" not in norm:
                if prefix_idx is None:
                    prefix_idx = i
            elif "engineering" not in norm:
                if any_idx is None:
                    any_idx = i
            elif any_idx is None:
                # last resort: something with CS even if engineering is in it
                any_idx = i

        target = exact_idx
        if target is None:
            target = prefix_idx
        if target is None:
            target = any_idx

        if target is None:
            return False

        loc.nth(target).click(timeout=8000)
        page.wait_for_timeout(800)
        return True

    # 2. Try as links (most common)
    links = page.get_by_role("link", name=re.compile("Computer Science", re.I))
    if click_best(links):
        return

    # 3. Try as buttons
    btns = page.get_by_role("button", name=re.compile("Computer Science", re.I))
    if click_best(btns):
        return

    # 4. Try generic text nodes
    texts = page.get_by_text(re.compile("Computer Science", re.I))
    if click_best(texts):
        return

    # If we got here, nothing matched well enough
    raise RuntimeError("Major 'Computer Science' not found on the page (by text).")





def open_major_agreement(page):
    """
    After selecting the major, click 'View Agreement' if that button exists.
    """
    for pat in ["View Agreement", "View Details", "View"]:
        btn = page.get_by_role("button", name=re.compile(pat, re.I)).first
        if btn.count() and btn.is_visible():
            try:
                btn.click()
                page.wait_for_timeout(800)
                return
            except Exception:
                pass
    # Some flows auto-load the agreement; nothing to click in that case.



# ------------------ parsing ------------------ #

def parse_mappings(page, uc_name: str) -> List[MappingRow]:
    """
    Extract CC -> UC course mappings from the current agreement page.

    Primary strategy for ASSIST's 'articRow' structure:
      <div class="articRow">
        <div class="rowReceiving">   # UC side (prefixCourseNumber, title, units)
        <div class="rowDirection">   # arrow
        <div class="rowSending">     # CC side (course(s) or 'No Course Articulated')
      </div>

    Fallbacks: DataGrid/table/text heuristics if no .articRow found.
    """
    rows: List[MappingRow] = []

    def extract_from_frame(frame) -> List[MappingRow]:
        frame_rows: List[MappingRow] = []

        # ---------- 1) Preferred: explicit .articRow structure ----------
        try:
            artic_rows = frame.locator(".articRow")
            count = artic_rows.count()
            if count:
                seen = set()
                for i in range(count):
                    r = artic_rows.nth(i)

                    # UC side (receiving)
                    recv = r.locator(".rowReceiving")
                    if not recv.count():
                        continue

                    uc_code_el = recv.locator(".prefixCourseNumber").first
                    uc_code = nz(uc_code_el.inner_text()) if uc_code_el.count() else ""
                    if not uc_code:
                        # fallback: use entire receiving text
                        uc_code = nz(recv.inner_text())

                    uc_title_el = recv.locator(".courseTitle").first
                    uc_title = nz(uc_title_el.inner_text()) if uc_title_el.count() else ""

                    # CC side (sending)
                    send = r.locator(".rowSending")
                    if not send.count():
                        continue

                    # If there's a 'No Course Articulated' <p>, that defines cc_course
                    no_art_p = send.locator("p").filter(
                        has_text=re.compile("No Course Articulated", re.I)
                    )
                    if no_art_p.count():
                        cc_course = "No Course Articulated"
                    else:
                        # Otherwise try similar structure on CC side: prefixCourseNumber / text
                        cc_code_el = send.locator(".prefixCourseNumber").first
                        if cc_code_el.count():
                            cc_course = nz(cc_code_el.inner_text())
                        else:
                            cc_course = nz(send.inner_text())

                    if not cc_course or not uc_code:
                        continue

                    key = (cc_course, uc_code)
                    if key in seen:
                        continue
                    seen.add(key)

                    note = uc_title  # store UC title as note (optional)
                    frame_rows.append(MappingRow(cc_course, uc_code, note, uc_name))

                if frame_rows:
                    return frame_rows
        except Exception:
            pass

        # ---------- 2) DataGrid-style (role=rowgroup/row/cell) fallback ----------
        try:
            rowgroup = frame.locator('[role="rowgroup"]')
            if rowgroup.count():
                datarows = rowgroup.locator('[role="row"]')
                rc = datarows.count()
                if rc:
                    start_idx = 1 if rc > 1 else 0
                    for i in range(start_idx, rc):
                        r = datarows.nth(i)
                        cells = r.locator('[role="cell"]')
                        if cells.count() >= 2:
                            cc = nz(cells.nth(0).inner_text())
                            uc = nz(cells.nth(1).inner_text())
                            note = nz(cells.nth(2).inner_text()) if cells.count() >= 3 else ""
                            if cc and uc:
                                frame_rows.append(MappingRow(cc, uc, note, uc_name))
            if frame_rows:
                return frame_rows
        except Exception:
            pass

        # ---------- 3) Classic <table><tr><td> fallback ----------
        try:
            tables = frame.locator("table")
            if tables.count():
                for ti in range(tables.count()):
                    t = tables.nth(ti)
                    trs = t.locator("tr")
                    if trs.count() < 2:
                        continue
                    for ri in range(1, trs.count()):  # skip header row
                        r = trs.nth(ri)
                        tds = r.locator("td")
                        if tds.count() >= 2:
                            cc = nz(tds.nth(0).inner_text())
                            uc = nz(tds.nth(1).inner_text())
                            note = nz(tds.nth(2).inner_text()) if tds.count() >= 3 else ""
                            if cc and uc:
                                frame_rows.append(MappingRow(cc, uc, note, uc_name))
            if frame_rows:
                return frame_rows
        except Exception:
            pass

        # ---------- 4) Very loose text-based fallback ----------
        try:
            blocks = frame.locator(
                "[data-testid*='Articulation'], .articulation, .MuiPaper-root, .card, .MuiTable-root"
            )
            for i in range(blocks.count()):
                text = blocks.nth(i).inner_text()
                for line in text.splitlines():
                    line = nz(line)
                    if not line:
                        continue
                    if "—" in line or " - " in line:
                        parts = re.split(r"[—-]+", line)
                        if len(parts) >= 2:
                            cc, uc = nz(parts[0]), nz(parts[1])
                            if len(cc) > 1 and len(uc) > 1:
                                frame_rows.append(MappingRow(cc, uc, "", uc_name))
        except Exception:
            pass

        return frame_rows

    # ---------- Try main page first ----------
    rows = extract_from_frame(page)
    if rows:
        return rows

    # ---------- Then try all iframes ----------
    for frame in page.frames:
        if frame is page.main_frame:
            continue
        try:
            frame_rows = extract_from_frame(frame)
            if frame_rows:
                rows.extend(frame_rows)
        except Exception:
            continue

    return rows





# ------------------ high-level scraping ------------------ #

def scrape_one_campus(page, cc_name: str, uc_name: str) -> pd.DataFrame:
    go_home(page)
    select_academic_year(page)
    select_cc_institution(page, cc_name)
    select_uc_institution(page, uc_name)
    click_view_agreements(page)

    # Now we are on a page with agreement types / or directly by major
    go_to_major_view(page)
    select_major_cs(page)
    open_major_agreement(page)

    page.wait_for_timeout(1000)
    data = parse_mappings(page, uc_name)
    df = dataframe_from_rows(data)

    # 🔍 DEBUG: if no rows, dump the current page HTML for inspection
    if df.empty:
        html = page.content()
        safe_campus = re.sub(r"[^A-Za-z0-9]+", "_", uc_name)
        debug_file = f"debug_{safe_campus}.html"
        with open(debug_file, "w", encoding="utf-8") as f:
            f.write(html)
        log(f"[DEBUG] {uc_name}: no rows parsed, wrote {debug_file}")

    return df




def compute_overlap(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Intersection of CC courses across all campuses, ignoring 'No Course Articulated'.
    This is the core of the student's plan at their home CC.
    """
    if not dfs:
        return pd.DataFrame(columns=["cc_course", "campus_count"])

    sets = []
    for campus, df in dfs.items():
        if df.empty or "cc_course" not in df.columns:
            return pd.DataFrame(columns=["cc_course", "campus_count"])
        cc_set = {
            c
            for c in df["cc_course"].tolist()
            if not is_no_articulation(c)
        }
        sets.append(cc_set)

    common = set.intersection(*sets) if sets else set()
    return pd.DataFrame(
        sorted(
            [{"cc_course": c, "campus_count": len(dfs)} for c in common],
            key=lambda x: x["cc_course"],
        )
    )

def find_missing_and_alternatives(
    page,
    home_cc_name: str,
    dfs: Dict[str, pd.DataFrame],
    alt_cc_list: List[str],
) -> pd.DataFrame:
    """
    For each UC campus, find rows where the home CC shows 'No Course Articulated'.
    For each such UC course, search alt_cc_list and return ONLY the first CC
    that provides an articulation.

    Returns a DataFrame with columns:
      uc_campus, required_uc_course, home_cc, alt_cc, alt_cc_course
    """
    results = []
    cache: Dict[tuple, pd.DataFrame] = {}

    for uc_name, df in dfs.items():
        if df.empty:
            continue

        for _, row in df.iterrows():
            cc_course = row["cc_course"]
            uc_course = row["uc_course"]

            # Only examine gaps where home CC has no articulation
            if not is_no_articulation(cc_course):
                continue
            if not uc_course or is_no_articulation(uc_course):
                continue

            # Search alt CCs until we find the first valid alternative
            for alt_cc in alt_cc_list:
                if alt_cc.strip().lower() == home_cc_name.strip().lower():
                    continue  # skip student's own CC

                key = (alt_cc, uc_name)
                if key not in cache:
                    try:
                        log(f"  [SEARCH] {alt_cc} for {uc_name} (to cover {uc_course}) …")
                        alt_df = scrape_one_campus(page, alt_cc, uc_name)
                    except Exception as e:
                        log(f"    [SKIP] {alt_cc} for {uc_name}: {e}")
                        alt_df = pd.DataFrame()
                    cache[key] = alt_df

                alt_df = cache[key]
                if alt_df.empty:
                    continue

                # Find any row where this UC course is articulated
                matches = alt_df[
                    (alt_df["uc_course"] == uc_course)
                    & (~alt_df["cc_course"].apply(is_no_articulation))
                ]

                if not matches.empty:
                    m = matches.iloc[0]   # ✅ FIRST valid alternative only
                    results.append(
                        {
                            "uc_campus": uc_name,
                            "required_uc_course": uc_course,
                            "home_cc": home_cc_name,
                            "alt_cc": alt_cc,
                            "alt_cc_course": m["cc_course"],
                        }
                    )
                    break  # ✅ stop searching alt CCs after first valid hit

    return pd.DataFrame(results)
    






# ------------------ CLI entry ------------------ #

def main():
    ap = argparse.ArgumentParser(
        description="ASSIST CS articulation scraper for a single UC campus."
    )
    ap.add_argument(
        "--cc",
        required=True,
        help="Home community college name, e.g. 'Santa Monica College'",
    )
    ap.add_argument(
        "--uc",
        required=True,
        help="Target UC campus, e.g. 'UC Berkeley' or 'University of California, Berkeley'",
    )
    ap.add_argument(
        "--visible",
        action="store_true",
        help="Run with visible browser window (for debugging).",
    )
    args = ap.parse_args()

    home_cc = args.cc
    uc_input = normalize_uc_name(args.uc)

    # Use a slug for the campus CSV filename
    uc_slug = re.sub(r"[^A-Za-z0-9]+", "_", uc_input).lower()
    campus_csv = f"{uc_slug}.csv"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=(not args.visible),
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context()
        page = context.new_page()

        results: Dict[str, pd.DataFrame] = {}

        # ------------------ 1) SCRAPE MAIN CAMPUS ------------------ #
        try:
            log(f"Scraping {uc_input} …")
            df = scrape_one_campus(page, home_cc, uc_input)
            log(f"[OK] {uc_input}: {len(df)} rows")
            df.to_csv(campus_csv, index=False)
            log(f"Saved {campus_csv}")
            results[uc_input] = df
        except (PWTimeout, PWError, RuntimeError) as e:
            log(f"[ERROR] {uc_input}: {e}")
            df = pd.DataFrame()

        # ------------------ 2) COMPUTE OVERLAP ------------------ #
        if not df.empty:
            overlap_df = df[
                (~df["cc_course"].apply(is_no_articulation))
                & (~df["cc_course"].apply(is_university_only))
            ].copy()
            overlap_courses = sorted(overlap_df["cc_course"].unique().tolist())
        else:
            overlap_courses = []

        # ------------------ 3) SET ALT CC LIST ------------------ #
        alt_cc_list = [
            cc for cc in TOP_ALT_COMMUNITY_COLLEGES
            if cc.strip().lower() != home_cc.strip().lower()
        ]
        log(f"[INFO] Using {len(alt_cc_list)} top alt community colleges for gap search.")

        # ------------------ 4) FIND ALTERNATIVES ------------------ #
        no_course_alts = []
        if results and uc_input in results:
            try:
                missing_df = find_missing_and_alternatives(
                    page, home_cc, results, alt_cc_list
                )
                if not missing_df.empty:
                    missing_df.to_csv(
                        "no_course_articulated_alternatives.csv", index=False
                    )
                    no_course_alts = missing_df.to_dict(orient="records")
                    log(
                        f"Saved no_course_articulated_alternatives.csv ({len(missing_df)} rows)"
                    )
                else:
                    log("No 'No Course Articulated' gaps found with alternatives.")
            except Exception as e:
                log(f"[ERROR] while finding alternatives: {e}")

        context.close()
        browser.close()

    # ------------------ 5) BUILD FINAL JSON ------------------ #
    if not df.empty:
        articulations_json = {uc_input: df.to_dict(orient="records")}
    else:
        articulations_json = {uc_input: []}

    student_plan = {
        "current_school": home_cc,
        "to_school": uc_input,
        "articulations": articulations_json,
        "overlap_courses": overlap_courses,
        "no_course_articulated_alternatives": no_course_alts,
    }

    with open("student_plan.json", "w", encoding="utf-8") as f:
        json.dump(student_plan, f, indent=2)

    log("Saved student_plan.json")




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
