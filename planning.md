# Project 1 Planning: The Unofficial Guide

---

## Domain
Student experiences with on-campus dining and nearby food options at CSU San Marcos.
This knowledge is valuable because students need honest opinions about meal plans, food
quality, and which dining spots are worth visiting. Official channels like the CSUSM
dining website only show marketing content — they don't reflect student satisfaction,
value for money, or real wait times. The best tips only exist in Reddit posts, Yelp
reviews, and student community discussions.

---

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | CSUSM Dining Homepage | Official dining overview and meal plan info | https://www.csusm.edu/dining/index.html |
| 2 | CSUSM Dining Locations | All campus dining locations and hours | https://www.csusm.edu/dining/locations/index.html |
| 3 | Campus Way Cafe | Official menu page for main dining hall | https://www.csusm.edu/dining/locations/cafe.html |
| 4 | Campus Coffee Cart Yelp | 24 student reviews of on-campus coffee cart | https://www.yelp.com/biz/campus-coffee-cart-san-marcos |
| 5 | Reddit r/CSUSM | Student posts about dining, food, meal plans | https://www.reddit.com/r/CSUSM/ |
| 6 | Niche.com Reviews | Student reviews mentioning campus food (B+ rating, $5,226/yr meal plan) | https://www.niche.com/colleges/california-state-university-san-marcos/reviews/ |
| 7 | CSUSM Meal Plans | Official meal plan options and pricing | https://www.csusm.edu/dining/mealplans/index.html |
| 8 | Nearby Restaurants | Yelp listings of restaurants near campus | documents/csusm_nearby_restaurants.txt |
| 9 | CSUSM Yelp Reviews | Student reviews mentioning campus dining | https://www.yelp.com/biz/california-state-university-san-marcos-san-marcos |
| 10 | CSUSM Dining Facebook | Official dining announcements and student comments | https://www.facebook.com/CsusmDining/ |
| 11 | Kalamata Mediterranean | On-campus Mediterranean restaurant full menu | documents/csusm_kalamata_mediterranean.txt |
| 12 | Shake Smart | On-campus smoothie/protein bar info | documents/csusm_shake_smart.txt |

---

## Chunking Strategy

**Chunk size:** 300 words

**Overlap:** 50 words

**Reasoning:** My documents are a mix of short student reviews (50-200 words) and longer
official pages (500+ words). 300 words captures the full context of a single review or
a menu section without mixing unrelated content. The 50-word overlap prevents losing
context when a student opinion or menu description spans a chunk boundary. A review-heavy
corpus like this warrants smaller chunks than a long FAQ — each review is a single opinion
that should stay together rather than be split across multiple chunks.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (runs locally)

**Top-k:** 3 chunks per query

**Production tradeoff reflection:** For real users I would weigh several factors.
all-MiniLM-L6-v2 is fast, free, and runs locally with no API calls, but has a 256-token
context limit and is English-only. OpenAI's text-embedding-ada-002 offers better accuracy
on domain-specific text and a longer context window but costs money per token and adds
API latency on every query. For a multilingual campus community I would consider a
multilingual model like paraphrase-multilingual-MiniLM-L12-v2. For a high-traffic
production system I would also consider caching frequent query embeddings to reduce
latency.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What vegan options are available on campus? | Tofu Green Curry, Jackfruit Carnitas Tacos, Mongolian noodles at Campus Way Cafe; falafel and hummus at Kalamata |
| 2 | Is the meal plan worth it? | Mixed — costs ~$5,226/year, some students find it expensive and inconvenient, others find it convenient |
| 3 | What time does Campus Coffee open? | Hours not clearly documented in collected sources |
| 4 | What are cheap restaurants near campus? | Should list specific nearby restaurants from nearby_restaurants.txt |
| 5 | What food stations are in Campus Way Cafe? | Smash burgers, pizza, pasta, salad bar, soup, vegan station, sandwiches, desserts |

---

## Anticipated Challenges

1. **JavaScript-rendered content:** Some CSUSM dining pages load menu content dynamically
   with JavaScript. A basic requests/BeautifulSoup scraper only sees the static HTML and
   may collect very little text. This could result in nearly empty documents that produce
   useless chunks — exactly what happened with csusm_campus_way_cafe.txt (only 58 chars).

2. **Off-target retrieval for specific queries:** The embedding model may match a query
   to the wrong document if the vocabulary doesn't overlap well. For example, "cheap
   restaurants near campus" may not semantically match a document titled
   "csusm_nearby_restaurants.txt" if the document uses different vocabulary. This could
   cause the system to return irrelevant chunks and fail to answer questions that should
   be answerable.

---

## Architecture
---

## AI Tool Plan

**Milestone 3 — Ingestion and chunking:**
I gave Claude the list of 10 source URLs and asked it to write a scrape.py script using
requests and BeautifulSoup. It produced a working scraper. I added a User-Agent header
after the first version timed out on CSUSM's server. I verified the output by checking
file sizes with `ls documents/` and confirmed all files had content.

**Milestone 4 — Embedding and retrieval:**
I gave Claude the ChromaDB installation errors and asked it to suggest an alternative
vector store. It produced embed.py using a JSON file with numpy cosine similarity. I
verified it by checking that embeddings.json was created and running query.py with a
test question to confirm retrieval worked.

**Milestone 5 — Generation and interface:**
I gave Claude the query.py script and asked it to build a Flask web interface that calls
the ask() function. It produced app.py with a single-page HTML interface. I verified it
by running the app and clicking each example question button to confirm answers appeared
with source citations.

