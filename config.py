
sample = 50 #Number of nodes required. This is used within the LLM prompt. 
avgspeed = 50 #kmph
duration = 3 #seconds max

prompt = f"""<context> Goal: Return a 2-dimensional array as JSON of latitude/longitude pairs representing **{sample}** distinct places in the **continental USA** (lower 48 + DC; exclude Alaska, Hawaii, territories, and water-only points). Definitions: “Pair” = [latitude, longitude] where latitude is first and longitude is second. “Continental USA bounds (approx)”:
Latitude: 24.5 to 49.5 (inclusive)
Longitude: −124.8 to −66.9 (inclusive)
</context>
<constraints> - Count: **exactly {sample} pairs, no more, no less**. - Domain: All points must fall within the continental USA bounds above. - Diversity: Spread points across multiple states and regions (West, Southwest, Mountain, Midwest, South, Mid-Atlantic, Northeast). No more than 3 pairs from the same metro area (judged by ~50 km radius). - Type: Use plausible land locations (cities/towns/parks/landmarks), not oceans/lakes only or obvious out-of-range places. - Order: Unsorted/randomized is fine; do **not** include indices. - Uniqueness: All pairs must be unique (no duplicates). - Format/Precision: - Each pair: `[lat, lon]` with 4–6 decimal places. - Use **decimal degrees** only; no N/S/E/W suffixes. - Use standard JSON array syntax: commas between pairs, square brackets enclosing the whole list. - **No trailing comma** after the last pair. - Output-only rule: **Respond with the array only**. Do **not** include any extra text, titles, code fences, explanations, or units. - Validity: No `null`, `NaN`, strings, or objects—just numbers in arrays. </constraints>
<output_format>
An example of the required structure with two dummy pairs (do not reuse these values and do not echo this example):
[
  [LAT1, LON1],
  [LAT2, LON2]
]"""
