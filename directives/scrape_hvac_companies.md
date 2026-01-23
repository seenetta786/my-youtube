# Scrape HVAC Companies in Texas - Directive

## Goal
Scrape 200 HVAC companies in Texas, verify email addresses, personalize contact information, and output results to a Google Sheet for outreach campaigns.

## Inputs
- **Target**: 200 HVAC companies
- **Location**: Texas
- **Data Fields**: Company name, contact person, email, phone, address, website
- **Personalization**: Basic company info to be used in email templates

## Execution Steps

### Phase 1: Scraping (Execution)
**Script**: `execution/scrape_hvac_texas.py`
- Use web scraping (BeautifulSoup, Selenium) to identify HVAC companies
- Target sources:
  - Google Maps (HVAC + Texas)
  - Yelp business listings
  - Local business directories
  - LinkedIn company search
  - Industry-specific databases
- Extract: company name, address, phone, website, contact email (if available)
- Store raw results in `.tmp/hvac_raw.json`
- Expected output: 200-250 records (accounting for duplicates/invalid data)

### Phase 2: Email Verification (Execution)
**Script**: `execution/verify_hvac_emails.py`
- Input: `.tmp/hvac_raw.json`
- Verification methods:
  - Hunter.io API (if available) or similar email finder service
  - Pattern matching from website domains
  - LinkedIn profile lookup
  - SMTP validation (graceful check without sending)
- Remove/flag records with unverifiable emails
- Store verified data in `.tmp/hvac_verified.json`
- Expected output: 150-180 verified records with confidence scores

### Phase 3: Personalization (Execution)
**Script**: `execution/personalize_hvac_data.py`
- Input: `.tmp/hvac_verified.json`
- Add personalization fields:
  - Contact person name (if found on website/LinkedIn)
  - Company services/specialties (from website scrape)
  - Company size estimate
  - Years in business
  - Google rating/reviews (if available)
- Generate personalization variables for email templates:
  - `[COMPANY_NAME]`
  - `[CONTACT_NAME]`
  - `[SERVICES]`
  - `[COMPANY_SIZE]`
- Store final data in `.tmp/hvac_final.json`

### Phase 4: Google Sheet Output (Execution)
**Script**: `execution/hvac_to_google_sheet.py`
- Create new Google Sheet: "HVAC Companies - Texas Outreach"
- Column structure:
  | Company Name | Contact Person | Email | Phone | Address | Website | Services | Company Size | Confidence Score | Notes |
- Format for readability:
  - Header row: bold, frozen
  - Email column: data validation for invalid formats
  - Confidence Score: color coding (green >90%, yellow 70-90%, red <70%)
- Share permissions: Set as needed
- Output: Google Sheet URL for access

## Outputs
1. **Google Sheet**: Linked, formatted, ready for outreach
2. **Backup JSON**: `.tmp/hvac_final.json` (local fallback)
3. **Quality Report**: 
   - Total scraped: X
   - Verified: Y (X% success rate)
   - Duplicates removed: Z

## Error Handling & Graceful Recovery

### Scraping Issues
- **No results from source**: Switch to alternative data source
- **Rate limiting**: Implement exponential backoff, pause if needed
- **Blocked by website**: Log and skip, continue with next source
- **Recovery**: Resume from last checkpoint in `.tmp/hvac_raw_checkpoint.json`

### Email Verification Issues
- **API quota exceeded**: Flag for manual verification, continue with found emails
- **No verification service available**: Use pattern matching as fallback
- **Invalid data**: Flag with low confidence score, include in sheet for manual review
- **Recovery**: Continue verification from last processed batch

### Google Sheet Issues
- **Authentication fails**: Check credentials in `.env` (GOOGLE_SHEETS_API_KEY, GOOGLE_SHEETS_ID)
- **Sheet creation fails**: Verify Google API is enabled, quotas not exceeded
- **Network timeout**: Retry with exponential backoff up to 3 times
- **Recovery**: Save data locally, wait, retry sheet creation

### Data Quality Issues
- **Duplicate records**: Hash company names + addresses, remove near-duplicates
- **Email format invalid**: Flag for manual review, assign low confidence
- **Missing critical fields**: Include in output but mark as incomplete
- **Personalization unavailable**: Use generic templates instead

## Notes & Constraints
- **Respect robots.txt**: Check website scraping policies
- **Rate limiting**: Be respectful to servers, add delays between requests
- **Data accuracy**: Prioritize quality over quantity; 150 verified > 200 unverified
- **Privacy**: Only collect publicly available information
- **Cost**: Use free email verification where possible; request approval for paid services

## Success Criteria
- ✅ 150+ companies with verified emails
- ✅ All critical fields populated (name, email, phone)
- ✅ Google Sheet formatted and accessible
- ✅ Personalization data added for 80%+ of records
- ✅ Confidence scores assigned to all records
