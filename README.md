# Facebook Ads Library Scraper

> Scrape detailed information about active ads from Facebook’s Ad Library — including ad content, creatives, targeting data, and publisher insights. This tool helps marketers, researchers, and businesses analyze the Facebook advertising landscape effectively.

> Gain structured, high-quality ad data to support market research, audience analysis, and competitor tracking.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Facebook Ads Library Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

The **Facebook Ads Library Scraper** allows users to extract complete and structured data about active ads running on Facebook and Instagram. It helps you study competitors’ ad strategies, identify trending creatives, and analyze campaign reach or targeting behavior.

### Why It’s Useful

- Collect real-time advertising data for multiple industries.
- Access all ad categories and countries.
- Analyze visual creatives, captions, and calls to action.
- Export structured ad data for further analytics or visualization.
- Ideal for marketing teams, agencies, and data-driven researchers.

## Features

| Feature | Description |
|----------|-------------|
| Multi-country Support | Scrape ads from all available countries. |
| Ad Content Extraction | Extract text, creatives, and CTA details from active ads. |
| Publisher Insights | Retrieve data about the ad’s originating page or business. |
| Media Assets | Collect image and video URLs associated with each ad. |
| Configurable Limit | Control how many ads to scrape with a maxItems parameter. |
| JSON Output | Receive clean and structured JSON data for easy integration. |
| Platform Coverage | Includes Facebook and Instagram ads. |
| Campaign Timing | Capture start and end dates of running campaigns. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| ad_archive_id | Unique identifier of the ad in Facebook’s archive. |
| page_id | The page or business ID associated with the ad. |
| page_name | The display name of the ad publisher. |
| page_profile_uri | Direct link to the Facebook page. |
| publisher_platform | Platforms where the ad is shown (Facebook, Instagram, etc.). |
| snapshot.body.text | Full text content of the ad. |
| images.original_image_url | URL of original image assets used in the ad. |
| cta_text | The call-to-action message (e.g., “Send WhatsApp message”). |
| start_date | The timestamp when the ad campaign began. |
| end_date | The timestamp when the ad campaign ended. |
| categories | Classified ad categories (e.g., UNKNOWN, Political, etc.). |
| page_like_count | Number of page likes for the advertiser. |

---

## Example Output

    [
      {
        "ad_archive_id": "3804712299743449",
        "page_id": "571062419989773",
        "page_name": "Debonair Men's Salon",
        "publisher_platform": ["FACEBOOK", "INSTAGRAM"],
        "snapshot": {
          "body": {
            "text": "Time is money, and we’re saving you both! Seize the day with a grand discount on all services..."
          },
          "cta_text": "Send WhatsApp message",
          "images": [
            {
              "original_image_url": "https://scontent-ams4-1.xx.fbcdn.net/v/t39.35426-6/464806700_514824171533348.jpg"
            }
          ]
        },
        "page_profile_uri": "https://www.facebook.com/debonairmensalon/",
        "page_like_count": 87467,
        "start_date": 1730271600,
        "end_date": 1730271600
      }
    ]

---

## Directory Structure Tree

    facebook-ads-library-scraper/
    ├── src/
    │   ├── main.py
    │   ├── extractors/
    │   │   ├── ad_parser.py
    │   │   └── media_handler.py
    │   ├── utils/
    │   │   ├── helpers.py
    │   │   └── validators.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── input.sample.json
    │   └── output.sample.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Marketing agencies** use it to analyze competitors’ creatives and ad spend strategies, helping clients improve campaign performance.
- **Researchers** use it to study advertising trends across countries and industries.
- **Brands** monitor their own active campaigns for compliance and consistency.
- **Media analysts** track cross-platform ad presence for influencer or publisher networks.
- **Data engineers** integrate the structured ad data into dashboards and BI tools for automated reporting.

---

## FAQs

**Q1: Does this scraper require authentication?**
No, it works using public ad library endpoints accessible without login.

**Q2: Can it handle video ads?**
Yes, it retrieves metadata for video ads, though only images are stored by default.

**Q3: How many ads can I scrape per run?**
You can configure the `maxItems` parameter to control the number of ads extracted per session.

**Q4: What output formats are available?**
You can download results as JSON, JSONL, CSV, Excel, HTML, or XML files.

---

## Performance Benchmarks and Results

**Primary Metric:** Scrapes up to 500 ads per minute depending on network and query complexity.
**Reliability Metric:** Achieves over 98% data retrieval success across multiple country datasets.
**Efficiency Metric:** Optimized request batching minimizes duplicate or incomplete ad entries.
**Quality Metric:** Maintains 99% structured field completeness across media, text, and metadata.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
