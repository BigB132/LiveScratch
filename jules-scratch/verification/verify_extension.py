import os
import time
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        extension_path = os.path.abspath("extension")

        # Use a persistent context to load the extension
        context = p.chromium.launch_persistent_context(
            "",  # An empty string for user_data_dir means a temporary directory
            headless=True,
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )

        page = context.new_page()

        try:
            # Navigate to a different Scratch project page to avoid rate limiting
            page.goto("https://scratch.mit.edu/projects/99999999/")

            # Wait for the page to be mostly idle
            page.wait_for_load_state('networkidle')

            # Wait for the "Livescratch Share" button to be visible
            # This indicates that the content script has successfully injected the UI
            share_button = page.locator('text="LivescratchShare"')

            # The expect function will wait for the element to be visible
            expect(share_button).to_be_visible(timeout=30000) # 30 second timeout

            print("Livescratch button found!")

            # Take a screenshot to visually verify the changes
            page.screenshot(path="jules-scratch/verification/verification.png")
            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            # Save a screenshot even if it fails to help with debugging
            page.screenshot(path="jules-scratch/verification/error.png")
        finally:
            context.close()

if __name__ == "__main__":
    run_verification()