import json
from playwright.sync_api import sync_playwright

URL = "file:///Users/leejinhyeok/Desktop/Project/MakeLearning/%EB%B9%9B%EC%9D%98%EA%B5%B4%EC%A0%88%EA%B3%A8%EB%93%A0%EB%B2%A8-%EC%B4%886%EA%B3%BC%ED%95%99.html"
OUT = "/Users/leejinhyeok/Desktop/Project/MakeLearning/harness/output/screenshots/"

console_msgs = []
page_errors = []

def attach_logging(page):
    page.on("console", lambda m: console_msgs.append(f"[{m.type}] {m.text}"))
    page.on("pageerror", lambda e: page_errors.append(str(e)))

def vis(page, sel):
    loc = page.locator(sel)
    if loc.count() == 0:
        return None
    return loc.first.is_visible()

def bbox(page, sel):
    loc = page.locator(sel)
    if loc.count() == 0 or not loc.first.is_visible():
        return None
    return loc.first.bounding_box()

def figure_visible(page):
    return page.locator("#figureWrap").is_visible()

report = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # ============ RESOLUTION VISIBILITY TEST: 1920x1080 and 1280x800 ============
    for vw, vh, tag in [(1920, 1080, "1920"), (1280, 800, "1280")]:
        ctx = browser.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1)
        page = ctx.new_page()
        attach_logging(page)
        page.goto(URL)
        page.wait_for_load_state("networkidle")

        page.click("#btnStart")
        page.wait_for_selector("#screen-play.active")

        res = {"viewport": [vw, vh]}
        figure_qs = []  # questions with a figure

        # walk through questions until we find one with a figure; record judge btn bbox after reveal
        # We test the FIRST figure question (worst case for tall layout) AND a non-figure one.
        first_fig_captured = False
        first_nofig_captured = False
        q_index = 0
        while q_index < 12 and not (first_fig_captured and first_nofig_captured):
            q_index += 1
            page.click("#btnReveal")
            page.wait_for_selector("#btnYes:visible")
            has_fig = figure_visible(page)
            if has_fig:
                figure_qs.append(q_index)

            # Measure judge buttons (only capture detail for first fig + first nofig)
            capture = (has_fig and not first_fig_captured) or (not has_fig and not first_nofig_captured)
            if capture:
                yes = bbox(page, "#btnYes")
                no = bbox(page, "#btnNo")
                card = bbox(page, ".qcard")
                entry = {
                    "q_index": q_index,
                    "has_figure": has_fig,
                    "btnYes_bbox": yes,
                    "btnNo_bbox": no,
                    "qcard_bbox": card,
                    "viewport_height": vh,
                    "btnYes_bottom": (yes["y"] + yes["height"]) if yes else None,
                    "btnNo_bottom": (no["y"] + no["height"]) if no else None,
                }
                # in viewport without scroll?
                entry["btnYes_in_viewport"] = (yes is not None) and (yes["y"] >= 0) and (yes["y"] + yes["height"] <= vh)
                entry["btnNo_in_viewport"] = (no is not None) and (no["y"] >= 0) and (no["y"] + no["height"] <= vh)
                # also check page scroll height vs viewport
                entry["doc_scroll_height"] = page.evaluate("document.documentElement.scrollHeight")
                entry["needs_scroll"] = page.evaluate("document.documentElement.scrollHeight > window.innerHeight + 2")

                if has_fig:
                    page.screenshot(path=f"{OUT}light-{tag}-figure-judge.png")
                    res["figure_question"] = entry
                    first_fig_captured = True
                else:
                    page.screenshot(path=f"{OUT}light-{tag}-nofig-judge.png")
                    res["nofig_question"] = entry
                    first_nofig_captured = True

            # advance
            page.click("#btnYes")
            if q_index < 12:
                # may have landed on result if logic; but 12 q so fine
                try:
                    page.wait_for_selector("#btnReveal:visible", timeout=2000)
                except Exception:
                    break

        res["figure_questions_seen"] = figure_qs
        report[tag] = res
        ctx.close()

    # ============ FLOW + RESULT REVIEW TEST (1280x800) ============
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    page = ctx.new_page()
    attach_logging(page)
    page.goto(URL)
    page.wait_for_load_state("networkidle")

    flow = {"states": []}

    # start screen: only start visible
    flow["start_btnStart_visible"] = vis(page, "#btnStart")
    page.click("#btnStart")
    page.wait_for_selector("#screen-play.active")

    wrong_records = []  # (q_text, answer_text, explain) for questions we mark NO

    for i in range(12):
        # BEFORE reveal: only reveal btn visible, judge hidden
        st = {
            "q": i + 1,
            "before_reveal": {
                "btnReveal": vis(page, "#btnReveal"),
                "btnYes": vis(page, "#btnYes"),
                "btnNo": vis(page, "#btnNo"),
                "explainBox": vis(page, "#explainBox"),
            }
        }
        page.click("#btnReveal")
        page.wait_for_selector("#btnYes:visible")
        st["after_reveal"] = {
            "btnReveal": vis(page, "#btnReveal"),
            "btnYes": vis(page, "#btnYes"),
            "btnNo": vis(page, "#btnNo"),
            "explainBox": vis(page, "#explainBox"),
            "correct_choice_highlighted": page.locator("#choices .choice.correct").count() == 1,
        }
        # Decide judgement: mark NO on q index 1 and 3 (to get wrong records), YES otherwise
        mark_no = i in (1, 3)
        if mark_no:
            qtext = page.locator("#qText").inner_text()
            ans = page.locator("#explainAnswer").inner_text()
            expl = page.locator("#explainText").inner_text()
            wrong_records.append({"q": qtext, "answer": ans, "explain": expl})
            page.click("#btnNo")
        else:
            page.click("#btnYes")

        if i < 11:
            page.wait_for_selector("#btnReveal:visible")
        flow["states"].append(st)

    # Should now be on result screen
    page.wait_for_selector("#screen-result.active")
    flow["reached_result"] = page.locator("#screen-result.active").count() == 1
    flow["result_score"] = page.locator("#resultScore").inner_text()
    flow["btnAgain_visible"] = vis(page, "#btnAgain")

    review_html = page.locator("#reviewArea").inner_text()
    flow["review_text"] = review_html
    flow["wrong_records"] = wrong_records
    # check each wrong q appears in review with answer+explain
    checks = []
    for wr in wrong_records:
        qfrag = wr["q"][:20]
        # explain text fragment
        efrag = wr["explain"][:15]
        checks.append({
            "q_fragment": qfrag,
            "q_in_review": qfrag in review_html,
            "explain_in_review": efrag in review_html,
        })
    flow["review_checks"] = checks
    flow["review_item_count"] = page.locator(".review-item").count()

    page.screenshot(path=f"{OUT}light-result-review.png", full_page=True)
    report["flow"] = flow
    ctx.close()

    # ============ SVG RENDER VERIFICATION — capture each figure type ============
    # Run game and reveal each q, screenshot when each figure type first appears
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    attach_logging(page)
    page.goto(URL)
    page.wait_for_load_state("networkidle")
    page.click("#btnStart")
    page.wait_for_selector("#screen-play.active")
    figtypes = {}
    for i in range(12):
        page.click("#btnReveal")
        page.wait_for_selector("#btnYes:visible")
        if figure_visible(page):
            cap = page.locator("#figureCap").inner_text()
            svg_present = page.locator("#figureSvg svg").count() == 1
            # classify by caption keyword
            if "볼록" in cap:
                key = "convex"
            elif "오목" in cap:
                key = "concave"
            elif "물" in cap:
                key = "refract"
            else:
                key = cap[:8]
            if key not in figtypes:
                figtypes[key] = {"cap": cap, "svg_element_present": svg_present,
                                 "svg_path_count": page.locator("#figureSvg svg path").count(),
                                 "svg_line_count": page.locator("#figureSvg svg line").count()}
                page.locator("#figureWrap").screenshot(path=f"{OUT}light-svg-{key}.png")
        page.click("#btnYes")
        if i < 11:
            page.wait_for_selector("#btnReveal:visible")
    report["svg_figures"] = figtypes
    ctx.close()

    # ============ 390x844 MOBILE LAYOUT ============
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
    page = ctx.new_page()
    attach_logging(page)
    page.goto(URL)
    page.wait_for_load_state("networkidle")
    page.screenshot(path=f"{OUT}light-390-start.png", full_page=True)
    page.click("#btnStart")
    page.wait_for_selector("#screen-play.active")
    page.click("#btnReveal")
    page.wait_for_selector("#btnYes:visible")
    mob = {}
    mob["horizontal_overflow"] = page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1")
    mob["scrollWidth"] = page.evaluate("document.documentElement.scrollWidth")
    mob["innerWidth"] = page.evaluate("window.innerWidth")
    # check choices stack single column (grid-template-columns)
    mob["choice_count"] = page.locator("#choices .choice").count()
    page.screenshot(path=f"{OUT}light-390-question.png", full_page=True)
    report["mobile_390"] = mob
    ctx.close()

    browser.close()

report["console_msgs"] = console_msgs
report["page_errors"] = page_errors

print(json.dumps(report, ensure_ascii=False, indent=2))
