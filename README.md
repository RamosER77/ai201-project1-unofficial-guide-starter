# The Unofficial Guide — Project 1

## Domain

Student experiences with on-campus dining and nearby food options at CSU San Marcos.
This knowledge is valuable because students need real, honest opinions about meal plans,
food quality, and dining options — not just the official marketing. Official channels like
the CSUSM dining website don't reflect student satisfaction, value for money, or which
spots are actually worth visiting. The best tips only exist in Reddit posts, Yelp reviews,
and student community discussions.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | CSUSM Dining Homepage | Official website | https://www.csusm.edu/dining/index.html |
| 2 | CSUSM Dining Locations | Official website | https://www.csusm.edu/dining/locations/index.html |
| 3 | Campus Way Cafe Menu | Official website | https://www.csusm.edu/dining/locations/cafe.html |
| 4 | Campus Coffee Cart | Yelp reviews | https://www.yelp.com/biz/campus-coffee-cart-san-marcos |
| 5 | Reddit r/CSUSM | Student posts | https://www.reddit.com/r/CSUSM/ (search: dining, food, meal plan) |
| 6 | Niche.com Reviews | Student reviews | https://www.niche.com/colleges/california-state-university-san-marcos/reviews/ |
| 7 | CSUSM Meal Plans | Official website | https://www.csusm.edu/dining/mealplans/index.html |
| 8 | Nearby Restaurants | Yelp listings | https://www.yelp.com/search?find_near=california-state-university-san-marcos-san-marcos |
| 9 | CSUSM Yelp Reviews | Yelp reviews | https://www.yelp.com/biz/california-state-university-san-marcos-san-marcos |
| 10 | CSUSM Dining Facebook | Social media | https://www.facebook.com/CsusmDining/ |
| 11 | Kalamata Mediterranean | On-campus menu | documents/csusm_kalamata_mediterranean.txt |
| 12 | Shake Smart | On-campus info | documents/csusm_shake_smart.txt |

---

## Chunking Strategy

**Chunk size:** 300 words

**Overlap:** 50 words

**Why these choices fit your documents:** My documents are a mix of short student reviews
and longer official pages. 300 words is large enough to capture the full context of a
review or a menu section, but small enough to stay focused on one topic. A 50-word overlap
prevents losing context when a review spans a chunk boundary — for example, a student
opinion that starts in one chunk and concludes in the next.

**Final chunk count:** 45 chunks across 12 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 (sentence-transformers, runs locally)

**Production tradeoff reflection:** For a real deployment I would weigh several factors.
all-MiniLM-L6-v2 is fast and free but has a 256-token context limit and is English-only,
which is fine for CSUSM student content but would fail for a multilingual campus community.
OpenAI's text-embedding-ada-002 offers better accuracy on domain-specific text and longer
context windows but costs money per token and requires an API call for every query, adding
latency. For a production system serving thousands of students, I would evaluate whether
the accuracy improvement of a paid model justifies the cost, and consider a multilingual
model if the campus has significant non-English speaking students.

---

## Grounded Generation

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:** Every retrieved chunk is prefixed
with `[Source: filename]` before being passed to the LLM as context. The model is
instructed to cite the source in its answer. The web interface also displays a "Sources
used" section below every answer showing which document files were retrieved.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What vegan options are available on campus? | Tofu Green Curry, Jackfruit Carnitas Tacos, Mongolian noodles (Campus Way Cafe) | Listed vegan items from Kalamata Mediterranean — hummus, falafel, dolma, etc. | Partially relevant | Partially accurate |
| 2 | Is the meal plan worth it? | Mixed opinions, ~$5,226/year, some find it inconvenient | Found Reddit student saying it's not worth the $3k extra cost | Relevant | Accurate |
| 3 | What time does Campus Coffee open? | Hours not clearly in documents | "I don't have that information" | Relevant | Accurate |
| 4 | What are cheap restaurants near campus? | Should list nearby restaurants from nearby_restaurants.txt | "I don't have that information" | Off-target | Inaccurate |
| 5 | What food stations are in Campus Way Cafe? | Burgers, pizza, pasta, salad bar, soup, vegan options | "I don't have that information — context only mentions food drive" | Off-target | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** "What food stations are in Campus Way Cafe?"

**What the system returned:** "I don't have that information. The provided context only
mentions Campus Way Cafe as a location for a food drive."

**Root cause (tied to a specific pipeline stage):** The failure happened at the ingestion
stage. The scraper collected only 58 characters from csusm_campus_way_cafe.txt because
the CSUSM website renders menu content dynamically with JavaScript — the static HTML
scraper couldn't see it. When this nearly-empty file was chunked and embedded, the
resulting vector had almost no meaningful content. Even though retrieval correctly
identified this file as relevant, the chunk contained no menu information for the LLM
to use.

**What you would change to fix it:** Use a headless browser like Selenium or Playwright
to scrape JavaScript-rendered pages. Alternatively, manually copy the full menu content
into the document file and re-run embed.py to rebuild the embeddings.

---

## Spec Reflection

**One way the spec helped you during implementation:** The spec's instruction to collect
documents before writing any pipeline code was genuinely useful. Reading through the
Reddit posts and Yelp reviews first helped me understand that the content was short,
opinion-based text — which directly informed my decision to use 300-word chunks rather
than larger ones. Without that upfront reading I might have used 500-word chunks and
lost the specificity of individual reviews.

**One way your implementation diverged from the spec, and why:** The spec recommended
ChromaDB as the vector store, but I ended up using a JSON-based embedding store with
numpy cosine similarity instead. ChromaDB had a hard dependency on onnxruntime which
had no compatible build for my Mac's Python 3.12 environment. The JSON approach works
well for 45 chunks and taught me how semantic search actually works under the hood,
which is more educational than using a black-box vector database.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The assignment spec and my domain choice (CSUSM campus dining)
- *What it produced:* A list of 10 specific source URLs for CSUSM dining content including
  Yelp, Reddit, Niche.com, and official CSUSM pages
- *What I changed or overrode:* I added 2 extra sources (Kalamata Mediterranean and
  Shake Smart) that I found myself while browsing the campus dining website, bringing
  the total to 12 documents

**Instance 2**

- *What I gave the AI:* The error messages from ChromaDB and FAISS installation failures
- *What it produced:* A JSON-based embedding store using numpy cosine similarity as a
  replacement vector store
- *What I changed or overrode:* I kept the same chunk and query interfaces so the rest
  of the pipeline didn't need to change. I also decided to keep this approach permanently
  rather than trying to fix ChromaDB, because it's simpler and sufficient for my dataset size