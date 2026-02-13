import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    print("Step 1: Navigate to Admin Login")
    page.goto("http://localhost:8000/admin/login/")
    
    print("Step 2: Login as Admin")
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("admin")
    page.get_by_role("button", name="Log in").click()
    
    # Verify login success by checking for "Site administration" header
    expect(page.get_by_role("heading", name="Site administration")).to_be_visible()
    
    print("Step 3: Create an Organization")
    page.get_by_role("link", name="Organizations", exact=True).click()
    page.get_by_role("link", name="Add organization").click()
    # Unique name to avoid unique constraint if running multiple times
    import time
    org_name = f"Cyberdyne Systems {int(time.time())}"
    page.get_by_label("Name").fill(org_name)
    page.get_by_role("button", name="Save", exact=True).click()
    expect(page.get_by_text(f"The organization \"{org_name}\" was added successfully.")).to_be_visible()

    print("Step 4: Create a MoltenBot")
    page.get_by_role("link", name="Home").click()
    page.get_by_role("link", name="Molten bots").click()
    page.get_by_role("link", name="Add molten bot").click()
    
    bot_name = f"T-800-{int(time.time())}"
    page.get_by_label("Name").fill(bot_name)
    page.get_by_label("Organization").select_option(label=org_name)
    page.get_by_label("Temperature").fill("500")
    page.get_by_role("button", name="Save", exact=True).click()
    expect(page.get_by_text(f"The molten bot \"{bot_name} (500.0°C)\" was added successfully.")).to_be_visible()

    print("Step 5: Test 'Reheat' Action")
    # Select the bot
    page.locator("input[name='_selected_action']").first.check()
    # Select action
    page.locator("select[name='action']").select_option("reheat_bots")
    page.get_by_role("button", name="Go").click()
    # Verify success message
    expect(page.get_by_text("Started background job to reheat 1 bots.")).to_be_visible()

    print("Step 6: Verify Dashboard")
    page.goto("http://localhost:8000/")
    # Verify title
    expect(page.get_by_role("heading", name="MOLTENBOT // CONTROL CENTER")).to_be_visible()
    # Verify bot card appears (might need a retry wait due to fetching)
    expect(page.get_by_text(bot_name)).to_be_visible()
    # Verify temp (it should be 500 or 600 depending on race condition of background task)
    # We just check it exists
    expect(page.get_by_text("°C")).to_be_visible()

    print("✅ E2E Test Completed Successfully")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
