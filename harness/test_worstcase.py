import json
from playwright.sync_api import sync_playwright

URL = "file:///Users/leejinhyeok/Desktop/Project/MakeLearning/%EB%B9%9B%EC%9D%98%EA%B5%B4%EC%A0%88%EA%B3%A8%EB%93%A0%EB%B2%A8-%EC%B4%886%EA%B3%BC%ED%95%99.html"

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for vw, vh in [(1920,1080),(1280,800)]:
        worst_overflow = 0
        fig_fail = 0
        fig_total = 0
        nofig_fail = 0
        # multiple runs to cover all figure types across shuffles
        for run in range(6):
            ctx = browser.new_context(viewport={"width":vw,"height":vh})
            page = ctx.new_page()
            page.goto(URL); page.wait_for_load_state("networkidle")
            page.click("#btnStart"); page.wait_for_selector("#screen-play.active")
            for i in range(12):
                page.click("#btnReveal"); page.wait_for_selector("#btnYes:visible")
                hasfig = page.locator("#figureWrap").is_visible()
                yb = page.locator("#btnYes").bounding_box()
                bottom = yb["y"]+yb["height"]
                over = bottom - vh
                if over > worst_overflow: worst_overflow = over
                infn = bottom <= vh
                if hasfig:
                    fig_total += 1
                    if not infn: fig_fail += 1
                else:
                    if not infn: nofig_fail += 1
                page.click("#btnYes")
                if i<11: page.wait_for_selector("#btnReveal:visible")
            ctx.close()
        results.append({"vp":[vw,vh],"worst_btn_overflow_px":round(worst_overflow,1),
                        "figure_q_cutoff_count":fig_fail,"figure_q_total":fig_total,
                        "nofig_q_cutoff_count":nofig_fail})
    browser.close()
print(json.dumps(results,ensure_ascii=False,indent=2))
