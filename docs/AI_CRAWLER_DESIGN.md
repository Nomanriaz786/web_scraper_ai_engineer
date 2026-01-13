# AI-Powered E-Commerce Crawler - System Design

## Executive Summary

This document outlines my approach to building an intelligent web crawler that can extract structured product data from any e-commerce website. The key innovation is using AI to generate CSS selectors once per site, then reusing those selectors for all product pages - making the system both intelligent and cost-effective.

---

## Problem Statement

Building crawlers for e-commerce sites presents several challenges:

- **Diverse HTML structures** across different platforms
- **Anti-bot protection** on major sites like Amazon
- **Manual selector maintenance** is time-consuming and error-prone
- **Multi-language content** requiring locale-aware extraction

My solution addresses these by combining AI-powered selector generation with traditional rule-based extraction.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INPUT LAYER                                 │
│   Product URLs  ──>  Site Detection  ──>  Profile Lookup            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                            │
│   URL Queue  ──>  Task Scheduler  ──>  Rate Limiter                 │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       CRAWLING ENGINE                               │
│   HTTP Fetcher (Static)  |  Browser Engine (JS/Anti-bot)            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
              ┌────────────────┴────────────────┐
              ▼                                 ▼
┌──────────────────────────┐     ┌──────────────────────────────────────┐
│    KNOWN SITE?           │     │     NEW SITE (AI ONBOARDING)         │
│                          │     │                                      │
│  Use selectors from      │     │  Send HTML to LLM ──> Generate       │
│  database                │     │  CSS selectors ──> Save in Database  │
└────────────┬─────────────┘     └───────────────┬──────────────────────┘
             │                                   │
             └───────────────┬───────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      EXTRACTION ENGINE                              │
│   Apply CSS Selectors  ──>  Parse Fields  ──>  Validate Data        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                  │
│   Product Store (JSON/DB)  |  Site Profiles  |  Raw HTML Cache      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Flow

### Step 1: Site Detection

When a URL is received, the system identifies the domain and checks if we have a stored profile with CSS selectors.

### Step 2: Fetch Page Content

Based on the site requirements, choose the appropriate fetcher:

| Fetcher | Technology | Use Case |
|---------|------------|----------|
| HTTP Fetcher | `requests` + `BeautifulSoup` | Static HTML sites |
| Browser Engine | SeleniumBase UC Mode | JavaScript-heavy, anti-bot sites |

### Step 3: AI Selector Generation (New Sites Only)

For new sites without a profile, I use AI to analyze a sample product page and generate CSS selectors:

### Step 4: Data Extraction

Apply the CSS selectors (either cached or AI-generated) to extract product data:

### Step 5: Validation & Storage

Validate extracted data against our pydantic mdoel and save to the product store.

---

## AI Integration Strategy

### When AI is Used

| Scenario | AI Role | Frequency |
|----------|---------|-----------|
| New site onboarding | Generate CSS selectors | Once per domain |
| Selector failure | Regenerate broken selectors | On-demand |
| Complex text parsing | Extract attributes from descriptions | Per-field fallback |

### Cost Analysis

| Approach | AI Calls | Cost |
|----------|----------|------|
| AI per page | 1000 pages × $0.01 | $10.00 |
| AI per site (my approach) | 1 call × $0.01 | $0.01 |

By generating selectors once and reusing them, I reduce AI costs by **99%** while maintaining extraction accuracy.

---

## Site Profile Schema

Each site has a stored profile containing its selectors:

---

## Data Model

Pydantic model will be used for the validation.

---

## Anti-Bot Handling

For protected sites like Amazon:

1. **SeleniumBase UC Mode** - Undetected ChromeDriver bypasses bot detection
2. **Realistic behavior** - Human-like wait times and scrolling
3. **Interstitial handling** - Automatically dismiss popups like "Continue shopping"
4. **Session reuse** - Single browser instance for batch crawls

---

## Scalability

| Component | Scaling Strategy |
|-----------|------------------|
| Crawler Workers | Horizontal scaling with containerized workers |
| URL Queue | Redis-backed distributed queue |
| Site Profiles | Cached in memory, persisted to database |
| Rate Limiting | Per-domain limits respecting robots.txt |

---

## Trade-offs

| Decision | Rationale |
|----------|-----------|
| AI for selector generation, not extraction | One-time cost vs per-page cost |
| Hidden inputs over visible elements | More stable, less affected by UI changes |
| Multi-language keyword matching | Supports international sites without code changes |
| Browser only for protected sites | HTTP is faster for static sites |

---

## Future Enhancements

1. **Self-healing selectors** - Detect when selectors break and auto-regenerate
2. **Visual AI** - Use vision models when HTML parsing fails
3. **Selector confidence scoring** - Track selector success rates
4. **Automatic site detection** - Identify e-commerce platforms automatically

---

## Conclusion

This architecture balances intelligence with cost-efficiency. By using AI strategically for one-time selector generation rather than per-page extraction, I achieve:

- **99% cost reduction** compared to per-page AI calls
- **Scalable extraction** using cached CSS selectors
- **Adaptability** for new sites with minimal manual work
- **Reliability** through hidden input extraction and stable selectors
