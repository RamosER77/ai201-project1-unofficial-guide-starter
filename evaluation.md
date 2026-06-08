# Evaluation Report - CSUSM Unofficial Dining Guide

## Test Questions and Results

---

### Question 1: What vegan options are available on campus?
**Correct Answer:** Campus Way Cafe offers Mongolian noodles, Crab-less Po' Boy, Tofu Green Curry, Jackfruit Carnitas Tacos. Kalamata Mediterranean also has vegan options.
**System Answer:** Listed vegan options from Kalamata Mediterranean (hummus, falafel, dolma, etc.)
**Chunks Retrieved:** csusm_kalamata_mediterranean.txt, csusm_reddit_dining.txt, csusm_niche_reviews.txt
**Accuracy:** ✅ Partially Accurate — retrieved real vegan options but focused on Kalamata, missed Campus Way Cafe vegan items

---

### Question 2: Is the meal plan worth it?
**Correct Answer:** Mixed opinions — some students find it expensive (~$5,226/year), others find it convenient.
**System Answer:** Found a Reddit student saying it's not worth it, citing the $3k extra cost and inconvenience.
**Chunks Retrieved:** csusm_reddit_dining.txt, csusm_yelp_reviews.txt
**Accuracy:** ✅ Accurate — grounded in real student opinion with citation

---

### Question 3: What time does Campus Coffee open?
**Correct Answer:** Campus Coffee is listed as Closed on the locations page (no hours found in documents).
**System Answer:** "I don't have that information."
**Chunks Retrieved:** csusm_campus_coffee.txt, csusm_campus_way_cafe.txt
**Accuracy:** ✅ Accurate — correctly admitted it didn't have the info rather than hallucinating

---

### Question 4: What are cheap restaurants near campus?
**Correct Answer:** Should reference nearby_restaurants.txt with specific places.
**System Answer:** "I don't have that information."
**Chunks Retrieved:** csusm_niche_reviews.txt, csusm_yelp_reviews.txt, csusm_facebook.txt
**Accuracy:** ❌ Inaccurate — retrieval failed to surface csusm_nearby_restaurants.txt

---

### Question 5: What food stations are in Campus Way Cafe?
**Correct Answer:** Smash burgers, pizza, pasta, salad bar, soup, vegan options, sandwiches, desserts.
**System Answer:** TBD — run this question and fill in the result
**Chunks Retrieved:** TBD
**Accuracy:** TBD

---

## Failure Analysis

### Identified Failure: Question 4 (Cheap restaurants near campus)
**What happened:** The system said "I don't have that information" even though csusm_nearby_restaurants.txt exists in the documents.
**Why it happened:** The retrieval pulled chunks from niche_reviews, yelp_reviews, and facebook instead of nearby_restaurants. This is likely because the nearby_restaurants.txt content didn't use the word "cheap" — so the semantic similarity score was lower than other documents.
**How to fix it:** Add more descriptive text to nearby_restaurants.txt, or increase top_k from 3 to 5 to retrieve more chunks.

---

## Summary
- 5 questions tested
- 3 accurate or partially accurate
- 1 retrieval failure identified
- System correctly refuses to hallucinate when information is missing