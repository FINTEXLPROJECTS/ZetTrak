import re
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8005"

# ──────────────────────────────────────────────
# Page Title & Header
# ──────────────────────────────────────────────

def test_page_title(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title(re.compile("ZetTrack"))

def test_logo_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.locator(".logo h2")).to_be_visible()
    expect(page.locator(".logo h2")).to_have_text("ZetTrack")

def test_navbar_links_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_role("link", name="Home")).to_be_visible()
    expect(page.get_by_role("link", name="Features")).to_be_visible()
    expect(page.get_by_role("link", name="About")).to_be_visible()
    expect(page.get_by_role("link", name="Pricing")).to_be_visible()
    expect(page.get_by_role("link", name="Contact")).to_be_visible()

def test_login_and_signup_buttons(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_role("link", name="Login")).to_be_visible()
    expect(page.get_by_role("link", name="Sign Up")).to_be_visible()

# ──────────────────────────────────────────────
# Hero Section
# ──────────────────────────────────────────────

def test_hero_section_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.locator(".hero")).to_be_visible()

def test_hero_heading(page: Page):
    page.goto(BASE_URL)
    expect(page.locator(".hero h1")).to_contain_text("Attendance")

def test_hero_get_started_button(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_role("link", name="Get Started")).to_be_visible()

def test_hero_watch_demo_button(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_role("link", name="Watch Demo")).to_be_visible()

# ──────────────────────────────────────────────
# About Section
# ──────────────────────────────────────────────

def test_about_section_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#about")).to_be_visible()

def test_about_heading(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#about h2")).to_contain_text("Revolutionizing HR Operations")

# ──────────────────────────────────────────────
# Features Section
# ──────────────────────────────────────────────

def test_features_section_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#features")).to_be_visible()

def test_feature_automated_payroll(page: Page):
    page.goto(BASE_URL)
    expect(page.locator(".feature-item h3").nth(0)).to_contain_text("Automated Payroll")

def test_feature_realtime_attendance(page: Page):
    page.goto(BASE_URL)
    expect(page.locator(".feature-item h3").nth(1)).to_contain_text("Real-time Attendance")

def test_feature_leave_management(page: Page):
    page.goto(BASE_URL)
    expect(page.locator(".feature-item h3").nth(2)).to_contain_text("Leave Management")

# ──────────────────────────────────────────────
# Contact Section
# ──────────────────────────────────────────────

def test_contact_section_visible(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#contact")).to_be_visible()

def test_contact_form_fields(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("input[type='text']").first).to_be_visible()
    expect(page.locator("input[type='email']")).to_be_visible()
    expect(page.locator("textarea")).to_be_visible()

def test_contact_form_submit_button(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_role("button", name="Send Message")).to_be_visible()

def test_contact_email_info(page: Page):
    page.goto(BASE_URL)
    expect(page.locator("#contact")).to_contain_text("info@zettrak.com")

# ──────────────────────────────────────────────
# Pricing Page (/pricing/)
# ──────────────────────────────────────────────

def test_pricing_page_loads(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page).to_have_url(re.compile("/pricing/"))

def test_pricing_page_title(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page.locator("h1")).to_contain_text("Transparent Pricing")

def test_pricing_free_plan_visible(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page.get_by_text("Free Forever")).to_be_visible()

def test_pricing_free_plan_price(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page.get_by_text("$0")).to_be_visible()

def test_pricing_pro_plan_visible(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page.get_by_text("Pro Plan", exact=True)).to_be_visible()

def test_pricing_pro_plan_price(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page.get_by_text("$99", exact=True)).to_be_visible()

def test_pricing_get_started_free_button(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page.get_by_role("link", name="Get Started Free")).to_be_visible()

def test_pricing_faq_visible(page: Page):
    page.goto(f"{BASE_URL}/pricing/")
    expect(page.get_by_text("Frequently Asked Questions")).to_be_visible()

# ──────────────────────────────────────────────
# Navigation Scroll (homepage anchors)
# ──────────────────────────────────────────────

def test_navbar_features_link_scrolls(page: Page):
    page.goto(BASE_URL)
    page.get_by_role("link", name="Features").click()
    expect(page.locator("#features")).to_be_in_viewport()

def test_navbar_contact_link_scrolls(page: Page):
    page.goto(BASE_URL)
    page.get_by_role("link", name="Contact").click()
    expect(page).to_have_url(re.compile("/contact"))
