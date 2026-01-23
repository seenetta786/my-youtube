## Directive: Scraping HVAC Companies, Email Verification, Personalization, and Google Sheet Export

**Objective:** To scrape information for 200 HVAC companies in Texas, including their names, addresses, and websites, then verify associated emails, personalize outreach messages, and finally export all data to a Google Sheet.

**I. Web Scraping (200 HVAC Companies in Texas)**

*   **Strategy:**
    *   Utilize Python libraries (e.g., `requests`, `BeautifulSoup4`) for web scraping.
    *   Target publicly available business directories (e.g., Yelp, Yellow Pages, local business listings) and potentially Google Maps (though direct scraping of Google Maps can be challenging due to dynamic content and terms of service).
    *   Focus on extracting: Company Name, Address, Phone Number, Website URL.
*   **Challenges:**
    *   Anti-scraping measures on websites.
    *   Variability in website structures requiring robust parsing logic.
    *   Need for proxies/VPNs if rate limits are encountered (outside current toolset).

**II. Email Discovery & Verification**

*   **Strategy:**
    *   **Discovery:** Attempt to find email addresses on company websites (contact pages, footers). If not found, infer common email patterns (e.g., info@company.com, sales@company.com).
    *   **Verification:** Integrate with an external email verification API. This step is crucial for deliverability and avoiding bounces.
*   **Cost Implications:** Email verification APIs typically involve costs based on the number of verifications.
*   **Tooling Consideration:** I do not have direct access to a pre-integrated email verification API. This will require selecting and integrating a suitable (potentially free tier) API.

**III. Email Personalization**

*   **Strategy:**
    *   Leverage an LLM (if available via API, e.g., Gemini, OpenAI) to generate a short, personalized outreach message for each company, incorporating their name, services (if discernible from their website), and location.
    *   If an LLM is not available, a templated personalization approach will be used (less effective).
*   **Cost Implications:** LLM usage incurs costs based on token usage.
*   **Tooling Consideration:** This will require secure access to an LLM API.

**IV. Google Sheet Export**

*   **Strategy:**
    *   Utilize a Python library (e.g., `gspread` for Google Sheets API) to authenticate and interact with Google Sheets.
    *   Create a new Google Sheet with appropriate headers (Company Name, Address, Phone, Website, Email, Verification Status, Personalized Email).
    *   Populate the sheet with the collected and processed data.
*   **Prerequisites:**
    *   Google Cloud Project setup with Google Sheets API enabled.
    *   Service account or OAuth 2.0 credentials (`credentials.json`, `token.json` might be relevant if user has existing Google API setup).
    *   User authorization for accessing their Google Sheets.

**Proposed Implementation Steps:**

1.  **Install necessary Python libraries** (`requests`, `BeautifulSoup4`, `gspread`, `oauth2client` or similar for Google API).
2.  **Develop a web scraping module** to collect company data.
3.  **Develop an email discovery and verification module** (integrating with an external API).
4.  **Develop an email personalization module** (integrating with an LLM if possible).
5.  **Develop a Google Sheets integration module** to export the final data.

**Seeking User Approval/Input:**

*   **Confirmation:** Do you approve this general approach?
*   **Google API Credentials:** Do you have existing Google API credentials (`credentials.json`, `token.json`) for Google Sheets integration? If so, I will investigate how to use them. If not, I will guide you on how to set them up.
*   **Email Verification API:** Do you have a preferred (or free tier) email verification API you'd like me to use, or should I research options?
*   **LLM for Personalization:** Do you have an LLM API key (e.g., Gemini, OpenAI) available for email personalization? If not, a templated approach will be used.