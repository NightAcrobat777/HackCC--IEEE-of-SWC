from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.assist.org", wait_until='networkidle')
    time.sleep(3)
    
    # Save HTML to file
    html = page.content()
    with open('/tmp/assist_org_page.html', 'w') as f:
        f.write(html)
    
    print("HTML saved to /tmp/assist_org_page.html")
    print(f"Page length: {len(html)} bytes")
    
    # Print some useful info
    inputs = page.query_selector_all('input')
    print(f"\nInputs found: {len(inputs)}")
    for i, inp in enumerate(inputs[:5]):
        attrs = page.evaluate(f'() => document.querySelectorAll("input")[{i}].attributes')
        print(f"  Input {i}: {attrs}")
    
    # Check for school/institution related elements
    print("\nSearching for school/institution related elements:")
    for selector in ['[placeholder*="school"]', '[placeholder*="institution"]', '[ng-reflect-placeholder*="select"]', '.school-selector']:
        elems = page.query_selector_all(selector)
        if elems:
            print(f"  {selector}: {len(elems)} found")
    
    # Check for year selector
    print("\nSearching for year selector:")
    for selector in ['select', '[ng-reflect-model]', '[formControlName*="year"]']:
        elems = page.query_selector_all(selector)
        if elems:
            print(f"  {selector}: {len(elems)} found")
    
    # Check body for data attributes
    body = page.query_selector('body')
    if body:
        print(f"\nBody inner HTML length: {len(body.inner_html())} bytes")
    
    browser.close()
    print("\nDone. Check /tmp/assist_org_page.html to inspect the page structure.")
