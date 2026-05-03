---
name: ecommerce-ctr-photography
description: >
  Use this skill whenever a seller wants to create AI-generated product photography
  specifically designed to increase Click-Through Rate (CTR) on e-commerce platforms
  like Flipkart, Amazon, Meesho, or Myntra. Triggers include: "write a prompt to
  increase my clicks", "help me create a hero image for my product listing", "my
  product isn't getting clicks", "generate a product photo prompt for Flipkart",
  "how should I photograph my clothes to stand out", "create a prompt for my trouser/
  kurti/dress/top listing", or any request that combines fashion photography with
  e-commerce performance goals. This skill goes beyond photorealism — it applies
  competitive grid analysis, pattern-interrupt theory, and platform-specific visual
  strategy BEFORE writing the prompt, ensuring every element (background, pose,
  expression, shoes, top) is chosen to stop the scroll. Always use this skill even
  if the user just uploads a product photo and says "make it look better" — they
  almost certainly mean "make it get more clicks."
---
 
# E-Commerce CTR Photography Skill
### Optimized for Flipkart / Indian marketplace sellers using gpt-image-2
 
This skill generates AI photography prompts that are engineered to win attention on
crowded e-commerce grids — not just look good in isolation. Every decision (background
color, pose, expression, shoes, top style) is made after analyzing the competitive
landscape the image will live in.
 
**This skill extends `/ai-fashion-photography-prompt`** — read that skill for all
photorealism mechanics (skin, fabric, anatomy, eyes). This skill handles the
strategy layer that comes BEFORE writing the prompt.
 
---
 
## THE CORE INSIGHT FROM REAL TESTING
 
> "Technically correct doesn't stop a thumb."
 
An image can be perfectly photorealistic and still fail at CTR. The reason: every
competitor is also technically correct. On a Flipkart mobile grid at ~150px thumbnail
size, **all technically correct images look identical.** The customer's thumb doesn't
stop for correct — it stops for different.
 
CTR is won before the customer consciously evaluates the product. It is won in 0.3
seconds by a single visual element that causes the brain to pause. This skill is
engineered to create that pause.
 
---
 
## STEP 1: ANALYZE INPUTS BEFORE WRITING ANYTHING
 
When the user provides a product photo or PDF (e.g., a Flipkart search results page),
extract the following before suggesting anything:
 
### A. Analyze the Product
From the raw product photo:
- **Color** — exact hue (pure white, off-white, cream, black, navy, etc.)
- **Fabric** — **Default: Tencel** (soft, breathable, natural drape, slight sheen, eco-premium feel). Only change this if the seller explicitly states a different fabric. Tencel drapes differently from ponte/scuba — it flows rather than holds structure, which affects fold language and lighting in the prompt.
- **Silhouette** — wide-leg, straight, tapered, flare, cigarette
- **Key design features** — pockets, waistband type, seam details, print, embellishment
- **Occasion signal** — casual, formal, office, party
- **What this product does well** — the one physical feature worth showcasing
### B. Analyze the Competitor Grid
From the e-commerce search result PDF or screenshot:
- **Dominant background colors** — what % of listings use white, grey, beige?
- **Dominant poses** — are they all standing straight, front-facing?
- **Dominant garment colors** — what colors are oversaturated vs rare?
- **Price tier** — **Fixed: mid-range (₹500–₹1000, typically ~₹800).** Do not re-assess this from the grid. Price positioning is already decided.
- **Footwear pattern** — what shoes are everyone using? (Note: sandals are never an option regardless of what competitors use — see Step 6.)
### C. Identify the Gap
The gap = what is ABSENT from the competitor grid. That absence becomes your advantage.
 
**Example from this skill's development:**
- Flipkart women's trousers grid: 95% white/grey/beige backgrounds, 95% standing-straight poses, dominant garment colors = black/beige/olive. **White trouser on deep green background with walking pose = zero competition.**
---
 
## STEP 2: BACKGROUND COLOR SELECTION
 
Background is the single highest-impact CTR lever. It must be chosen based on the
**contrast matrix** — what creates maximum pop of YOUR product color against the
competitor sea.
 
### The Contrast Matrix
 
| Product Color | Worst Background (blends in) | Best Background (CTR winner) |
|---|---|---|
| **Pure White** | White, grey, cream | Deep forest green, navy, terracotta |
| **Black** | Dark grey, navy | Warm beige, dusty rose, warm white |
| **Beige / Camel** | Beige, cream, white | Dusty sage, warm terracotta, slate |
| **Navy / Dark Blue** | White (too clinical), grey | Warm sand, rust, off-white |
| **Olive / Khaki** | Beige (merges), cream | Rust, burnt sienna, deep burgundy |
| **Grey** | Grey walls (obvious) | Warm ivory, blush, terracotta |
| **Red / Burgundy** | White (too high contrast, garish) | Deep charcoal, dark olive, cream |
| **Prints / Patterns** | Busy backgrounds | Deep solid — let the print breathe |
 
### Background Rules
1. **Never use the same color family as the product.** White trouser → never white wall.
2. **Choose matte over gloss.** Matte walls read as premium, glossy reads as budget studio.
3. **Add subtle texture.** Slightly aged paint, fine plaster texture — prevents CGI feel.
4. **Always signal a premium brand photoshoot.** This is non-negotiable. Use a richly draped fabric backdrop — floor-to-ceiling natural linen, heavy cotton muslin, or raw silk in a complementary tone, pooling softly at the base. This signals premium-brand production quality and immediately separates the listing from flat painted-wall budget shots. Draped fabric is an aspirational cue that elevates perceived price point at thumbnail size.
5. **The background color should be absent from the competitor grid.** If everyone uses terracotta, don't use terracotta.
### Proven Performers (tested in this project)
- **Deep forest green** (`#1A3C2A`) with white garment → highest contrast in Flipkart women's trouser grid
- **Burnt terracotta** with black/olive garment → warm, rare, stands out from cool-grey competitor palette
- **Deep navy** with beige/camel garment → premium signal, rare in budget category
---
 
## STEP 3: MODEL SELECTION
 
### Ethnicity Strategy
**Always use an international model with naturally white/light skin — regardless of price point, platform, or target market.** This is a fixed brand decision, not a variable. The aspiration signal of an international-looking model with naturally light skin tone consistently outperforms Indian or Asian models for CTR in the mid-range price tier on Flipkart.
 
**Fixed model descriptor (use this every time):**
```
Eastern European or Northern European woman, mid-20s to early 30s.
Naturally white skin with cool pink-neutral undertone — even, porcelain
surface, not tanned, not bronzed. Slight natural rosiness at the cheeks
and nose tip. The skin is naturally light — not filtered or artificially
brightened.
```
 
**Hair contrast note:** Keep hair dark (dark brown, chestnut) regardless of model
ethnicity when using dark backgrounds — the hair-to-background contrast matters for
thumbnail readability. Avoid blonde + dark background.
 
---
 
## STEP 4: POSE STRATEGY
 
Pose must be chosen based on **what the product needs to demonstrate** AND **what
creates visual energy vs. the competitor grid.**
 
### The Pose Decision Matrix
 
| If the competitor grid has... | Use this pose |
|---|---|
| All standing straight, front-facing | Walking mid-stride, 3/4 angle |
| All standing with hand in pocket | Weight-shift contrapposto, arms natural |
| All static, no energy | Walking with slight hair movement |
| All walking (rare) | Standing tall, confident, direct gaze |
 
### Pose Physics by Garment Type
 
**Straight/Slim trousers:** Walking mid-stride shows the trouser's movement, drape at
the hip crease, and fit across the thigh simultaneously. Static standing shows nothing.
 
**Wide-leg trousers:** Composed standing (weight on one leg, slight hip shift) is
actually better — it lets the wide leg panel fall in full architectural shape.
Walking collapses the wide-leg silhouette.
 
**Flare/Bootcut:** Walking slightly toward camera at 3/4 shows the flare at the hem.
This is the only pose that lets the hem shape read clearly.
 
**Formal/Cigarette trousers:** Composed standing, one hand in pocket, minimal movement.
The structure of the trouser IS the selling point.
 
### The Walking Pose (highest CTR performer for fitted trousers)
```
Walking mid-stride toward camera at a 3/4 angle — weight transitioning from back
foot to front foot, natural forward momentum in torso. Front knee slightly bent,
back foot lifted at heel. Hips in natural forward rotation from walking. Torso
has natural slight counter-rotation. Right arm slightly forward from stride, left
arm back — natural arm swing, relaxed. NOT posing. NOT standing. Mid-stride.
```
 
### The Composed Standing Pose (best for wide-leg, formal, architectural silhouettes)
```
Standing still in composed, tall posture. Body at a very subtle 3/4 angle —
approximately 10–15° turned toward camera left. Weight resting on right leg —
right hip very slightly elevated by 2–3cm. Left knee softly bent and relaxed.
She is NOT walking. Standing with complete composure and stillness. One hand
partially inside the slant pocket — fingers partially inside, thumb on pocket edge.
```
 
---
 
## STEP 5: EXPRESSION STRATEGY
 
Expression is the emotional bridge between the customer and the product. Choose based
on price point and target customer.
 
### Fixed Expression (always use this — no exceptions)
Price point is always mid-range (₹500–₹1500). The expression is therefore fixed:
 
```
A barely-there upward lift at the corners of the mouth — not a full smile,
not performing for camera. The expression that says "I know I look good."
Gaze directed 15–20° past the camera to camera right. Chin level. Alive,
present, not vacant.
```
 
**Do not use any other expression.** Specifically avoid:
- Full smile looking at camera = catalog signal, customers skip it
- Completely neutral / editorial = too cold for this price tier, creates distance
- Laughing or exaggerated joy = reads as cheap promotional content
- Downward gaze = disengaged, low confidence
The barely-there confident near-smile is the only expression that is simultaneously aspirational AND accessible at the ₹500–₹1500 price point.
 
---
 
## STEP 6: FOOTWEAR — THE MOST OVERLOOKED CTR ELEMENT
 
Footwear at thumbnail size can make or break the trouser silhouette. This is the most
common mistake in AI-generated fashion listings.
 
### The Footwear Rules
 
**Rule 1: Never match shoe color to trouser color.**
White trouser + white sneaker = trouser hem disappears at 150px. The ankle line —
which defines the trouser's silhouette — becomes invisible.
 
**Rule 2: Shoe color must create a clean separation from trouser hem.**
 
| Trouser Color | Best Shoe Color |
|---|---|
| White | Nude/tan flat, beige block heel, tan sneaker |
| Black | Nude heel, white sneaker, metallic flat |
| Beige/Camel | Dark brown loafer, tan block heel, olive mule |
| Navy | Tan/camel flat, white sneaker, nude heel |
| Olive | Tan loafer, brown Chelsea boot, nude mule |
| Grey | Blush flat, nude heel, tan sneaker |
 
**Rule 3: Always premium-looking footwear. No sandals. No flat rubber-sole sneakers.**
Footwear must signal premium positioning regardless of the trouser's occasion. Let the AI select the specific shoe style based on the overall outfit, garment silhouette, and top styling — but constrain it to the premium tier only. Acceptable options: block heel mules, pointed-toe kitten heels, clean leather loafers, sleek ankle-strap heels, minimal pointed flats. The shoe must look like it costs more than the trouser.
 
**Prompt instruction for footwear (use this framing):**
```
Premium footwear appropriate to the overall outfit — selected to complement the
trouser silhouette, top styling, and occasion signal. Must be premium-looking:
block heel mule, pointed kitten heel, clean leather loafer, or minimal pointed flat.
No sandals. No rubber-sole sneakers. No flat sport shoes. The shoe style should
feel like a premium brand choice, not a budget catalog shot.
Color: clearly distinct from the trouser hem color (see Rule 2).
```
 
**The fix for white trouser (from this project):**
```
Nude/tan pointed flat shoes or beige low block heel mule — unbranded, minimal,
slight natural wear. Color clearly distinct from white trouser hem. The ankle
line of the trouser must be fully visible and clean.
```
 
---
 
## STEP 7: TOP STYLING — DIRECT THE EYE TO THE PRODUCT
 
The top's job is to frame the trouser, not compete with it. One rule governs all choices:
 
**The eye must travel: face → waistband → trouser. Nothing should interrupt this path.**
 
### The Midriff Problem
A large bare midriff gap (oversized crop top) redirects the eye to the stomach before
it reaches the trouser. At thumbnail size, the skin strip becomes the most visually
dominant element in the image. The customer's first 0.3 seconds go to the wrong place.
 
**Fix:** Use a top that ends at or just above the waistband — maximum 1–2cm of skin
visible. The waistband should be the first trouser element the eye meets.
 
### Top Color Strategy
- **Black top** + white/light trouser = maximum contrast, eye goes straight to the trouser
- **White top** + dark trouser = clean, works if trouser has strong silhouette
- **Tucked neutral** + any trouser = classic, professional, waistband clearly visible
- **Pattern/print top** = NEVER — it steals attention from the trouser
### Top Style by Trouser Occasion
| Trouser Type | Best Top |
|---|---|
| Casual/everyday | Fitted black ribbed sleeveless crop (ending at waistband) |
| Office/formal | Fitted white or cream short-sleeve tucked blouse |
| Party/evening | Fitted satin or silk cami, tucked |
| Athleisure | Fitted sports bra or cropped athletic tank |
 
---
 
## STEP 8: THE COMPLETE CTR AUDIT CHECKLIST
 
Before finalizing any prompt, verify every item against this checklist:
 
### Background
- [ ] Background color is NOT in the same family as the product color
- [ ] Background color is ABSENT or rare in the competitor grid
- [ ] Background is matte, not glossy
- [ ] Background has subtle texture imperfections (not CGI-clean)
- [ ] Floor color clearly distinct from trouser hem color
### Model
- [ ] Model is Eastern/Northern European with naturally white/light skin — no Indian or Asian model
- [ ] Hair color creates contrast against background at thumbnail size
- [ ] Body type is healthy and proportional — not model-thin, not plus-size
### Pose
- [ ] Pose is different from 90%+ of competitors in the grid
- [ ] Pose demonstrates the specific garment type's best feature
- [ ] Pose creates visual energy or has movement signal
### Expression
- [ ] Expression matches price point strategy
- [ ] NOT a full-on smile directly at camera (catalog signal)
- [ ] Eyes are alive, gaze slightly past the camera
### Footwear
- [ ] Shoe color is CLEARLY different from trouser color
- [ ] Trouser ankle line is fully visible and clean (no color bleed)
- [ ] Shoe is premium-looking — block heel, kitten heel, loafer, or pointed flat
- [ ] No sandals. No rubber-sole sneakers. No flat sport shoes.
### Top Styling
- [ ] Top ends at or just above the waistband
- [ ] Midriff exposure is minimal (1–2cm max)
- [ ] Top color frames the trouser, not competes with it
- [ ] No print or pattern on top
### Thumbnail Test (mental simulation)
- [ ] Shrink the image mentally to 150px × 200px. Does the product still read clearly?
- [ ] Is there ONE element that would make the eye pause in a sea of competitors?
- [ ] Does the trouser silhouette have a clean, visible outline from waist to hem?
---
 
## STEP 9: WRITING THE FINAL PROMPT
 
After completing Steps 1–8, write the prompt using the full structure from
`/ai-fashion-photography-prompt`. All photorealism mechanics (skin physics, eye
detail, fabric drape, anatomy anchors, hand states, lighting physics) come from
that skill. This skill provides the strategy; that skill provides the execution.
 
### Critical additions from this project not in the base skill:
 
**For white garments — mandatory lighting note:**
```
CRITICAL: The white trouser must remain pure white — no yellow, cream, or warm
tint from lighting. Slight underexpose the white highlights by 1/3 stop —
fabric texture must remain visible, not blown out. The ponte surface variation
must show under lighting.
```
 
**For structured/ponte fabric:**
```
The fabric has structure and body — it holds its shape. Standing still means
the fabric falls in clean vertical lines. Slight natural compression fold at
the hip crease. Front center crease line faintly visible from waistband to hem.
Fabric texture must remain visible — do not blow out white highlights.
```
 
**The walking pose motion cue (adds energy even at thumbnail size):**
```
The walking motion creates: subtle fabric movement at hem, slight forward sway
in front panel catching directional key light creating diagonal tension fold
across upper thigh. A few flyaway strands from the walking movement catching
the key light.
```
 
---
 
## REFERENCE FILES
 
Read these when you need them:
 
- `references/proven-prompts.md` — Full prompts that have been generated and evaluated in real sessions, with critique notes
- `references/competitor-analysis-flipkart.md` — Specific grid analysis for Flipkart women's trousers category
---
 
## QUICK DECISION GUIDE FOR COMMON INPUTS
 
**User uploads a raw product photo on white floor and says "make it better":**
→ Run Steps 1–8. Choose background by contrast matrix. Default to walking pose unless wide-leg. Write full prompt using base skill.
 
**User uploads a Flipkart/Amazon screenshot and says "help me stand out":**
→ Run Step 1B (competitor grid analysis) first. Identify the gap. Then run Steps 2–8.
 
**User says "my image got generated but it's not getting clicks":**
→ Run the CTR Audit Checklist (Step 8). Identify what's failing. Fix only those sections in the prompt — do not rewrite the whole prompt from scratch.
 
**User asks "should I change my model from Indian to European":**
→ Ask their price point and target demographic. Use the Ethnicity Strategy table in Step 3 to give a clear recommendation with reasoning.
 
**User says "the trouser hem disappears in my image":**
→ Footwear color mismatch. Apply Rule 1 and Rule 2 from Step 6. Add explicit shoe color separation language to the prompt.