---
name: fashion-product-photography
description: >
  Use this skill when asked to generate AI image prompts for fashion/clothing
  product photography. Given raw front & back product images and an optional
  product description, this skill produces 5–7 angle-specific, photorealistic
  prompts engineered for e-commerce CTR. Every visual decision — background,
  complementary garments, accessories, pose, lighting — is made to maximize
  attention on the hero product. Covers all fashion categories: trousers, tops,
  dresses, kurtas, jackets, skirts, shorts, ethnic wear, and more. Model
  ethnicity is user-configurable with smart defaults.
---

# AI Fashion Product Photography — Multi-Angle Prompt Engine

This skill turns raw product images into a set of 5–7 production-ready,
photorealistic AI image generation prompts. Each prompt is engineered so the
hero product dominates every frame — technically correct AND attention-winning
on crowded e-commerce grids.

---

## THE CORE PRINCIPLE: HERO PRODUCT FOCUS

> "Technically correct doesn't stop a thumb."

An image can be perfectly photorealistic and still fail at CTR. On a mobile grid
at ~150px thumbnail size, all technically correct images look identical. The
customer's thumb stops for different — and it stops for the product, not the
background, not the model's face, not the accessories.

**Every element in the frame exists to serve the hero product.**

### The Attention Hierarchy

| Priority | Element | Role |
|---|---|---|
| 1 | **Hero product** | Highest contrast, most detail, most visual weight |
| 2 | **Model's face** | Draws initial gaze, then guides eye to hero product |
| 3 | **Background** | Contrasts with hero product to make it pop |
| 4 | **Complementary garments** | Visible but subdued — never competing |
| 5 | **Accessories & footwear** | Support the outfit, near-invisible at thumbnail |

If any element below the hero product draws more attention than the hero
product, the image has failed — regardless of how photorealistic it is.

---

## INPUT & OUTPUT FORMAT

### What You Receive
1. **Front product image** (raw photo of the garment — front view)
2. **Back product image** (raw photo of the garment — back view)
3. **Product description** (optional) — may include:
   - Product type and name
   - Key features to highlight
   - Target platform (Flipkart, Amazon, Meesho, Myntra, etc.)
   - Price tier
   - Target customer demographic
   - Model ethnicity preference
   - Specific requirements or constraints

### What You Output
1. **Art Director Analysis** — Brief summary of the hero product: color, fabric,
   silhouette, key features, what makes it worth buying
2. **Visual Strategy** — Background color chosen, complementary garment,
   footwear, accessories — with reasoning for each choice
3. **Shot Plan** — Total image count (5–7) and the list of selected angles
4. **The Prompts** — 5–7 fully written prompts, one per angle, ready for
   image generation (gpt-image-2, Gemini, or similar)

### Consistency Rule
All prompts in a set must maintain absolute consistency: same model identity,
same body type, same skin tone, same hair, same lighting setup, same background,
same styling (all clothing, all accessories). The only things that change between
prompts are pose, camera angle, and framing.

---

## STEP 1: ANALYZE THE HERO PRODUCT

Extract the following from the front and back images before making any decisions:

### From the Front Image
- **Color** — exact hue (pure white, off-white, cream, navy, dusty rose, etc.)
- **Fabric** — identify from texture and drape (cotton, linen, silk, polyester, denim, knit, etc.). If unclear, infer from garment type and note the inference.
- **Silhouette** — fitted, relaxed, oversized, A-line, flared, straight, tapered, etc.
- **Fit** — slim, regular, relaxed, oversized
- **Key design features** — pockets, buttons, zippers, prints, embroidery, pleats, seams, hardware
- **Construction details** — waistband type, neckline, hem style, closure type
- **Occasion signal** — casual, formal, office, party, athleisure, ethnic/festive

### From the Back Image
- **Back design** — plain, seam details, back yoke, vents, back pockets, zipper
- **Overall back silhouette** — how it differs from front
- **Construction** — back closure, darts, pleats from behind

### Synthesize
- **Hero product identity** — one sentence: what IS this product?
- **The one thing worth showcasing** — the single physical feature that sells it
- **Category classification** — bottomwear / topwear / dress / ethnic / outerwear / other

---

## STEP 2: VISUAL STRATEGY

Every decision in this step serves the Hero Product Focus principle.

### 2A: Background Selection

Background is the single highest-impact visual lever. Choose based on contrast
with the hero product color.

#### The Background Contrast Matrix

| Hero Product Color | Worst Background (blends) | Best Background (hero pops) |
|---|---|---|
| **Pure White** | White, grey, cream | Deep forest green, navy, terracotta |
| **Black** | Dark grey, navy, charcoal | Warm beige, dusty rose, warm cream |
| **Beige / Camel** | Beige, cream, white | Dusty sage, warm terracotta, slate blue |
| **Navy / Dark Blue** | White (too clinical), grey | Warm sand, rust, off-white |
| **Olive / Khaki** | Beige, cream | Rust, burnt sienna, deep burgundy |
| **Grey** | Grey walls | Warm ivory, blush, terracotta |
| **Red / Burgundy** | White (garish contrast) | Deep charcoal, dark olive, cream |
| **Pastels** | White (washes out) | Deeper shade of same family, warm neutral |
| **Prints / Patterns** | Busy backgrounds | Deep solid color — let the print breathe |
| **Bright / Vivid** | Competing vivid colors | Muted, desaturated neutral — hero is the only color anchor |

#### Background Rules
1. **Never same color family as hero product.** White garment → never white/grey/cream wall.
2. **Matte over gloss.** Matte reads premium; gloss reads budget studio.
3. **Subtle texture.** Slightly aged paint, fine plaster, natural surface variation — prevents CGI feel.
4. **Premium signal.** Use a richly draped fabric backdrop — floor-to-ceiling natural linen, heavy cotton muslin, or raw silk in a complementary tone, pooling softly at base. This signals premium production and separates the listing from flat budget shots.
5. **Floor color must be clearly distinct from the hero product's hem/bottom edge.** If the garment hem disappears into the floor, the silhouette is lost at thumbnail.

#### Proven Color Combinations
- Deep forest green (`#1A3C2A`) + white garment → maximum contrast
- Burnt terracotta + black/olive garment → warm, rare, premium
- Deep navy + beige/camel garment → sophisticated, premium signal
- Dusty sage + warm-toned garment → editorial, calm
- Warm sand + navy/black garment → approachable, clean

---

### 2B: Complementary Garment Strategy

The complementary garment is whatever covers the body area NOT occupied by the
hero product. Its job is to frame the hero product — never compete with it.

#### The Cardinal Rule
**The eye must travel: Face → Hero Product. The complementary garment must not
interrupt this path.**

#### Rules for ALL Complementary Garments
1. **Solid color only** — never prints, patterns, graphics, logos, or embellishments
2. **Must contrast with BOTH background AND hero product** — so the model's body reads clearly, but the hero product stands out most
3. **Must be SIMPLER than the hero product** — fewer details, less texture, less visual weight
4. **Must be fitted/clean-fitting** — excess fabric creates visual noise
5. **Must create a clean boundary with the hero product** — tucked in, clean hem line, no ambiguous overlap

#### When Hero = Bottomwear (trousers, skirts, shorts)
The complementary garment is a **top**. Choose based on hero product color:

| Hero Bottom Color | Best Complement Top | Why |
|---|---|---|
| White / Light | Fitted black ribbed sleeveless or short-sleeve | Maximum contrast, simple, eye drops to white bottom |
| Black / Dark | Fitted white or cream short-sleeve | Clean contrast, simple |
| Colored / Print | Fitted black or white (whichever contrasts more) | Neutral frame |
| Formal / Office | Fitted cream or white tucked blouse | Professional, clean waistband visibility |

**Critical:** Top must end at or just above the waistband — maximum 1–2cm of skin visible. A large midriff gap redirects the eye to skin before it reaches the hero product.

#### When Hero = Topwear (t-shirt, shirt, blouse, kurta top)
The complementary garment is a **bottom**. Rules:

| Hero Top Color | Best Complement Bottom | Why |
|---|---|---|
| White / Light | Dark wash slim jeans or black trousers | Recedes visually, eye stays on top |
| Black / Dark | Medium blue jeans or khaki chinos | Clean separation, doesn't compete |
| Colored / Graphic | Dark neutral — black, dark grey, dark denim | Lets the top be the color anchor |
| Formal | Tailored neutral trousers | Professional, complementary |

**Critical:** Bottom must be classic fit, no competing details (no rips, no patches, no prints). Simple and receding.

#### When Hero = Full-Body (dress, jumpsuit, saree)
No complementary garment needed. Accessories and footwear become more important for framing.

#### When Hero = Outerwear (jacket, coat, blazer)
Both inner top and bottom are complementary — both must be simple and monochrome:
- Inner: plain white or black tee/blouse
- Bottom: dark slim jeans or tailored trousers

---

### 2C: Footwear Strategy

Footwear at thumbnail size can make or break the garment silhouette.

#### Footwear Rules
1. **Never match shoe color to hero product color.** White trouser + white shoe = hem disappears at 150px.
2. **Shoe color must create clean separation from the nearest garment hem.**
3. **Always premium-looking.** No sandals. No flat rubber-sole sneakers. No sport shoes.
4. **Let the AI select specific style based on outfit context** — but constrain to premium tier.

#### Shoe Color by Hero Product Color

| Hero Product Color | Best Shoe Color |
|---|---|
| White | Nude/tan flat, beige block heel, tan sneaker |
| Black | Nude heel, white minimal sneaker, metallic flat |
| Beige/Camel | Dark brown loafer, tan block heel |
| Navy | Tan/camel flat, white sneaker, nude heel |
| Olive | Tan loafer, brown Chelsea boot |
| Grey | Blush flat, nude heel, tan sneaker |
| Red/Burgundy | Nude or dark neutral — never more red |
| Bright/Prints | Neutral nude or tan — never competing color |

#### Footwear Prompt Template
```
Premium footwear appropriate to the overall outfit — selected to complement the
garment silhouette and occasion signal. Must be premium-looking: block heel mule,
pointed kitten heel, clean leather loafer, minimal pointed flat, or sleek ankle boot.
No sandals. No rubber-sole sneakers. No flat sport shoes.
Color: clearly distinct from the nearest garment hem color.
```

---

### 2D: Accessory Strategy

Accessories ground the image in reality — a real person wears shoes, a watch,
maybe a necklace. Missing accessories read as mannequin display. But accessories
must NEVER draw more attention than the hero product.

#### Rules
1. **Maximum 2–3 accessories** — overstyling reads as catalog
2. **Match metal tone to garment temperature:** cool garment → silver/platinum; warm garment → gold/rose gold; neutral → either
3. **Describe material and wear** — accessories need realism (strap texture, chain weight, natural glint)
4. **Gender-appropriate choices**
5. **No statement pieces** — every accessory should be forgettable at thumbnail

---

## STEP 3: MODEL CONFIGURATION

### Ethnicity
**User-configurable.** If the user specifies a preference, use it. If not specified,
default to:

```
Eastern European or Northern European woman, mid-20s to early 30s.
Naturally white skin with cool pink-neutral undertone — even, porcelain
surface, not tanned, not bronzed. Slight natural rosiness at the cheeks
and nose tip.
```

**Undertone reference by ethnicity (use when user specifies):**

| Ethnicity | Undertone Description |
|---|---|
| South Asian / Indian | Warm golden-olive undertone, natural radiance |
| East Asian | Warm neutral to cool undertone, porcelain or ivory surface |
| Northern European | Light skin with cool pink or neutral undertone |
| Scandinavian | Very light skin with cool neutral undertone, porcelain surface |
| Middle Eastern | Warm olive with golden base undertone |
| Latin / Mediterranean | Warm neutral to olive undertone, slight golden cast |
| West African | Deep warm undertone with bronze-amber depth |

Always describe three layers: **tone + undertone + surface finish.**

### Hair
- Must create contrast against background at thumbnail size
- Dark hair (brown, chestnut) on dark backgrounds → ensure enough contrast or add backlight separation
- Avoid blonde + dark background (silhouette merges)
- Include flyaway detail: `loose wisps and flyaway hairs around the crown and temples, a few stray strands breaking the hair silhouette`

### Expression (Fixed — Use Every Time)
```
A barely-there upward lift at the corners of the mouth — not a full smile,
not performing for camera. The expression that says "I know I look good."
Gaze directed 15–20° past the camera to camera right. Chin level. Alive,
present, not vacant.
```

**Never use:** full smile at camera (catalog signal), completely neutral/editorial (too cold), laughing/exaggerated joy (reads cheap), downward gaze (disengaged).

### Body Type
```
Naturally healthy and proportional — not model-thin, not plus-size.
Soft feminine curves with natural body confidence. Realistic representation.
```
Adjust per user request. Always use specific language, never vague ("beautiful figure").

---

## STEP 4: SHOT PLAN

### How Many Shots
- **5 shots** — simple items (plain t-shirt, basic trouser, simple dress)
- **6 shots** — items with moderate detail (pockets, interesting neckline, texture)
- **7 shots** — feature-rich items (embroidery, hardware, unique construction, multiple design elements)

### Shot 1 Is Always the Hero Shot
Shot 1 is the main listing image — the one that appears on the search grid. It gets
the full CTR optimization treatment: background contrast, pose differentiation, the
0.3-second thumb-stopping element.

**CRITICAL RULE: The hero shot (Shot 1) must NEVER use a walking pose.** The model
must be stationary — composed standing, contrapposto, weight-shift, slight turn, or
any other non-walking body pose. Walking poses are acceptable for Shot 2 onward
(especially effective for back view or motion/lifestyle shots), but the primary
listing image must show the model standing still with poise and confidence. This
ensures the garment silhouette reads cleanly and completely at thumbnail size without
motion blur or mid-stride distortion.

### Pose Selection for the Hero Shot (Shot 1 — No Walking)

#### By Silhouette — Bottomwear

| Silhouette | Best Hero Pose (Standing) | Why |
|---|---|---|
| Straight / Slim / Tapered | Contrapposto, 3/4 angle, weight on one leg | Shows drape at hip, fit across thigh, clean silhouette |
| Wide-leg / Palazzo | Composed standing, weight on one leg, slight hip shift | Lets wide panels fall in full architectural shape |
| Flare / Bootcut | Standing at 3/4 angle, slight weight shift | Shows flare at hem in its natural resting shape |
| Formal / Cigarette | Composed standing, one hand in pocket | Structure of trouser IS the selling point |
| Shorts | Standing with weight shift, one knee slightly bent | Shows thigh fit and hem position cleanly |

#### By Silhouette — Topwear

| Silhouette | Best Hero Pose (Standing) | Why |
|---|---|---|
| Fitted / Slim | Slight torso turn, one arm relaxed | Shows fit and body interaction |
| Oversized / Boxy | Casual stance, slight lean or weight shift | Shows the relaxed silhouette naturally |
| Structured / Blazer | Confident standing, arms at sides or one in pocket | Shows garment structure and shoulders |
| Cropped | Standing with slight hip tilt — ensure crop length visible | Shows where it ends relative to waistband |

#### By Silhouette — Dresses

| Silhouette | Best Hero Pose (Standing) | Why |
|---|---|---|
| Fitted / Bodycon | Contrapposto, slight turn at 3/4 angle | Shows body-conforming silhouette cleanly |
| A-line / Flowy | Standing with subtle weight shift, fabric at rest | Shows natural drape and silhouette shape |
| Maxi / Floor-length | Composed standing, one hand at side | Shows full length and drape |
| Formal / Evening | Composed standing, elegant posture | Shows structure and occasion signal |

#### By Type — Ethnic Wear

| Type | Best Hero Pose (Standing) | Why |
|---|---|---|
| Kurta / Kurti | Standing with slight contrapposto, arms natural | Shows embroidery, length, overall silhouette |
| Saree | Traditional standing pose showing pallu drape | Shows drape artistry |
| Lehenga | Standing with slight turn to show skirt volume | Shows flare and embellishment |

### The Composed Standing Pose Template (USE FOR HERO SHOT — Shot 1)
```
Standing still in composed, tall posture. Body at a very subtle 3/4 angle —
approximately 10–15° turned toward camera left. Weight resting on right leg —
right hip very slightly elevated by 2–3cm. Left knee softly bent and relaxed.
She is NOT walking. Standing with complete composure and stillness. One hand
partially inside the slant pocket — fingers partially inside, thumb on pocket
edge — or resting loosely at hip. The other hand hanging naturally at side.
```

### The Walking Pose Template (for Shot 2+ only — NEVER for hero shot)
```
Walking mid-stride toward camera at a 3/4 angle — weight transitioning
from back foot to front foot, natural forward momentum in torso. Front
knee slightly bent, back foot lifted at heel. Hips in natural forward
rotation. Right arm slightly forward from stride, left arm back —
natural arm swing, relaxed. NOT posing. NOT standing. Mid-stride.
```

### Shot Angle Library by Category

**Bottomwear** (trousers, pants, skirts, shorts):
1. Hero — full front, full body, composed standing pose (never walking)
2. Full back — walking mid-stride or standing with energy, opposite view
3. Side profile — 3/4 angle showing silhouette depth
4. Waistband/hip detail — 3/4 crop from waist to mid-thigh
5. Hem/ankle detail — crop from knee down
6. *(optional)* Motion lifestyle — walking with fabric movement
7. *(optional)* Fabric texture close-up — tight crop on surface

**Topwear** (t-shirts, shirts, blouses, crop tops):
1. Hero — front 3/4 body, composed standing (never walking)
2. Full back — walking or standing, same framing, back view
3. Side profile — showing sleeve and silhouette
4. Neckline/collar detail — tight crop, neck to mid-chest
5. Sleeve/shoulder detail — crop on upper arm area
6. *(optional)* Graphic/print close-up (if applicable)
7. *(optional)* Fabric texture close-up

**Dresses** (all lengths):
1. Hero — full front, full body, composed standing (never walking)
2. Full back — walking or standing, full body
3. Side profile — 3/4 angle
4. Bodice/waist detail — crop from shoulder to hip
5. Hem/skirt movement — crop from knee down (or mid-thigh for short dresses)
6. *(optional)* Neckline detail
7. *(optional)* Fabric texture or embellishment close-up

**Ethnic Wear** (kurtas, kurtis, salwar sets, lehengas):
1. Hero — full front, full body, composed standing (never walking)
2. Full back — walking or standing, full body
3. Side profile — 3/4 angle
4. Neckline/embroidery detail — tight crop
5. Sleeve/cuff detail — crop on arm area
6. *(optional)* Hem detail or border work
7. *(optional)* Full set coordination view

**Outerwear** (jackets, coats, blazers):
1. Hero — full front, open/unbuttoned, composed standing (never walking)
2. Full front, closed/buttoned — same standing pose
3. Full back — full body
4. Side profile — showing structure and lapel
5. Collar/lapel detail — tight crop
6. *(optional)* Cuff/pocket/hardware detail
7. *(optional)* Inside lining (if featured)

---

## STEP 5: PROMPT STRUCTURE

Every prompt must use this 10-section structure. Never collapse into a paragraph.

```
Scene:
[Background surface/material/color. Environmental micro-details for realism —
subtle texture, imperfections. Light source and direction. Fill light. Floor
color and its separation from the garment. Atmosphere.]

Subject:
[Age, ethnicity, undertone. Body type. Expression (the fixed near-smile).
Hair texture, color, flyaway detail. Gaze direction.]

Body & Anatomy:
[Pose with weight distribution. Joint positions. Hand state (Strategy A/B/C/D).
Arm positions. Proportion anchors. Correct anatomy statement.]

Skin:
[Three-layer undertone. Pore detail — non-repeating, organic distribution.
Vellus hair on jawline catching side light. SSS at ear edges and nose tip.
Sebum zones (nose, forehead). Under-eye shadows. Imperfections. Asymmetry.]

Eyes:
[Iris fibers, limbal ring. Catchlight shape matching light source. Waterline
moisture. Individual lash strands with natural variation. Alive and present.]

Garment:
[HERO PRODUCT — Five-Layer description:
1. Precise color
2. Fabric type + weave
3. Weight & drape behavior
4. Fit behavior on this body type
5. Construction details
Then: fabric physics language for this garment type.
Then: COMPLEMENTARY GARMENT — solid, simple, described briefly.
"Preserve the exact fabric color and drape."]

Accessories:
[Footwear — type, color, material, wear detail, separation from hem.
Watch/bracelet or necklace/earrings — metal tone, minimal, complementary.
"Accessories complement but never compete with the hero product."]

Camera & Lighting:
[Camera body, lens, ISO 400, aperture. Camera position and framing.
Key light — type, position, angle, effect on skin and fabric.
Fill light — type, position, ratio. What light does to fabric weave.
Catchlight description. Color temperature.
"Photorealistic."]

Use case:
[E-commerce product photography / editorial fashion lookbook / lifestyle.]

Constraints:
[Full constraints block — see Constraints Library below.]
```

---

## PHOTOREALISM MECHANICS: SKIN

Replace vague "realistic skin" with biological specificity.

### Pore & Surface Detail
- `visible fine pores on cheeks and nose — non-repeating organic pore distribution, denser on nose, finer on cheeks`
- `natural skin micro-texture across forehead and chin`
- `super realistic skin pores — micro-pores visible at full resolution`

### Subsurface Scattering (the anti-plastic fix)
- `subsurface scattering visible at ear edges and nose tip — faint warm translucency`
- `light penetrates the top layer of skin at the nose bridge — soft glow, not hard plastic reflection`

### Vellus Hair (biggest AI giveaway when missing)
- `soft peach fuzz (vellus hair) on jawline and cheekbones catching the side light`
- `fine facial vellus hairs visible on the upper lip and forehead in raking light`
- `micro-hair strands along the hairline catching backlight`

### Undertone Specificity
Always three layers: **tone + undertone + surface finish.**
- `warm medium-deep skin tone with golden undertone, natural radiance`
- `light skin with cool pink undertone, slightly dewy surface`
- `deep skin with warm bronze undertone, subtle satin finish — not glossy`

Never say "brown skin" or "fair skin" alone. Undertone determines how light reads.

### Specular Variation (oily vs dry zones)
- `slight natural sebum sheen on nose bridge and center forehead only`
- `matte texture on cheeks and jawline`
- `gradual highlight roll-off on the cheekbones — not a sharp specular spike`

### Under-Eye Detail
- `natural under-eye shadows — slight darkness, not concealed`
- `faint blue-purple vein visibility beneath under-eye skin`

### Imperfections That Prove Humanity
- `subtle natural pigmentation variation — warmer on cheeks, cooler at temples`
- `faint expression lines at outer eye corners`
- `one or two faint natural freckles on nose bridge`
- `slight natural redness at nostril edges and inner eye corners`
- `very slight asymmetry in facial features`

### Film/Sensor Grain
- `shot on Sony A7R V, 85mm f/1.8, ISO 400 — slight sensor grain in shadow areas`

---

## PHOTOREALISM MECHANICS: EYES

### Iris Detail
- `visible iris texture — fine radial fibers, not flat color disc`
- `slight color variation within the iris — darker limbal ring at the edge`

### Catchlight & Reflection
- `one natural rectangular softbox catchlight in the iris — not ring light`
- `realistic eye reflections showing the environment/light source`

### Moisture & Life
- `slight moisture visible along the lower waterline`
- `the eyes look alive and present, not glassy or vacant`

### Eyelash Detail
- `individual lash strands visible — not a uniform dark line`
- `natural lash length variation — some longer, some shorter`

---

## PHOTOREALISM MECHANICS: BODY & ANATOMY

### Pose Language — Use Contrapposto, Not Generic Stance
Instead of "standing with weight on left leg," use:
`contrapposto stance — weight bearing on left leg, right hip slightly elevated,
shoulders counter-rotated left, natural S-curve in spine visible`

### Proportion Anchors (always include)
- `correct human proportions — head is 1/8 of total body height`
- `natural body structure, realistic anatomy`
- `realistic limb length — arms reaching mid-thigh when relaxed`

### Hands — Choose One Strategy Per Prompt

**A — Describe hand state (safest):**
```
Right hand resting loosely at hip, fingers naturally relaxed and slightly curled —
not stiff, not splayed. Left hand hanging at side, palm facing inward.
Correct finger count, proportional hand size relative to body.
```

**B — Give hands an object (easiest):**
```
Left hand holding a small clutch bag naturally — fingers wrapped around grip, thumb visible.
```

**C — Crop hands out (if not needed):**
```
Framing: 3/4 body shot from mid-thigh up — hands not in frame.
```

**D — Natural position with reinforcement:**
```
Hands in natural resting position — realistic finger proportions,
five fingers on each hand, relaxed curl, no extra joints.
```

### Anatomy Negatives (always include for full-body shots)
```
No extra fingers. No fused fingers. No missing fingers. No broken wrist angle.
No distorted hands. No noodle arms. No broken joints. No warped proportions.
Correct anatomy throughout.
```

---

## PHOTOREALISM MECHANICS: HAIR

- `loose wisps and flyaway hairs around the crown and temples`
- `a few stray strands breaking the hair silhouette — not perfectly styled`
- `natural hair texture with micro-strands catching the light`
- For motion shots: `a few flyaway strands from the walking movement catching the key light`

---

## FABRIC PHYSICS LIBRARY

Use the appropriate block for the hero product's garment type.

### Wide-Leg / Palazzo
```
Wide-leg silhouette. Leg panels fall with natural gravity — vertical parallel fold
lines running down the front panel. Side seams hang straight and true. Slight sway
creates diagonal tension lines across the thigh. Not stiff, not flat — natural
hanging cloth weight visible throughout.
```

### Straight / Slim / Tapered
```
Fitted through hip and upper thigh — slight compression fold at inner thigh from
natural body shape. Taper from knee to ankle. Front crease line running from
waistband to hem. Slight drag crease at the hip crease where leg meets torso.
```

### Flared / Bootcut
```
Fitted at hip and thigh, flaring from knee downward. Flare panels catch light
differently from the fitted upper. Hem drapes with slight break at ankle.
Movement causes the flare to sweep and catch air — organic flowing motion
lines across the lower leg.
```

### Oversized / Boxy Top
```
Oversized boxy silhouette — drop shoulders with sleeve seam falling 3–4 inches
below natural shoulder point. Body drapes loosely over torso with slight
blousing where hem meets hip. Soft vertical fold lines at sides. Fabric falls
with natural gravity — not stiff, not skin-tight, real cloth weight visible.
```

### Fitted Top / Blouse
```
Body-conforming silhouette following the torso's natural contour. Slight tension
at bust, relaxed at waist. Sleeves follow arm shape with natural ease. Fabric
makes contact with skin at pressure points — not painted on, not hovering.
```

### Structured Jacket / Blazer
```
Structured silhouette holding its own shape. Shoulder seams sit at natural
shoulder point. Lapels roll with their own weight. Front panels hang with
slight outward bow when unbuttoned. Sleeve hangs with clean vertical line,
slight compression at elbow bend.
```

### A-Line / Flowy Dress
```
Fitted at bodice, gradually widening from waist. Skirt panels fall with fabric
weight — natural swing radius visible. Movement creates soft arc-shaped fold
lines. Hem circles the body at consistent height, slight hem bounce on walking.
```

### Knit / Jersey
```
Stretch fabric following body contours with soft cling. Visible stretch recovery
tension at contact points. Natural fabric weight pulls hem downward. Surface
shows fine knit texture under directional light.
```

### Denim
```
Rigid weave with structured drape. Visible twill diagonal lines under directional
light. Natural crease memory at knee and hip. Fading patterns at wear points —
whiskers at thigh crease, slight knee fade. Fabric holds its shape between
contact points.
```

### Silk / Satin
```
Liquid drape following gravity and body contour. High specular highlights where
fabric catches key light — elongated bright reflections. Deep shadow contrast
in fold valleys. Fabric pools and flows, does not hold rigid shape.
```

### Chiffon / Sheer
```
Lightweight translucent fabric floating over body contour. Visible through
layering where fabric doubles. Catches air on movement — slight billow.
Requires backlight to show translucency.
```

### Kurta / Ethnic Cotton
```
Semi-structured drape — holds some body away from skin. Vertical fold lines
from shoulder to hem. Embroidery/print adds visual weight to decorated areas.
Side slits show controlled opening on movement. Natural cotton texture visible
under raking light.
```

---

## LIGHTING RULES

### Critical: No Direct Sunlight on Model or Garment
Direct sunlight causes color temperature shifts — navy turns purple, black shifts
brown, white looks yellow. The garment must appear true-to-life on screen.

**Rule:** All lighting on model and garment must be soft, diffused, and
color-neutral (~5500K daylight-balanced). If sunlight is desired for atmosphere,
use it only in the background.

### Fabric-Lighting Relationship

| Fabric Type | Best Light | Why |
|---|---|---|
| Silk, satin, charmeuse | Hard key from 45° | Creates specular highlights revealing sheen |
| Cotton, linen, jersey | Soft octabox / overcast | Reveals weave texture, matte surface |
| Denim, twill, corduroy | Raking sidelight | Catches woven ridges and surface texture |
| Sheer, chiffon | Backlight + soft front fill | Translucency only visible with backlight |
| Velvet | Single directional key | Nap shadow direction visible |
| Knit | Soft directional | Shows knit texture without harsh shadows |
| Embroidered / Sequined | Key light at 30–45° | Catches raised texture and reflective elements |

### Standard Lighting Setup (default for e-commerce)
```
Large softbox key light 45° to camera left at eye level, gentle bounce fill
from white reflector on the right. Soft raking key catching the weave texture
of the fabric. Sculpting shadows on the non-lit side of the face. One natural
rectangular softbox catchlight in the iris. Color temperature 5500K daylight-balanced.
```

### What Light Must Do
- On skin: sculpting shadows, gradual falloff, catchlight in eyes
- On fabric: reveal weave texture, show fold depth, maintain true color
- On background: even, no hotspots, no competing shadows

### Lighting Language That Kills Realism (Never Use)
"beautiful lighting", "perfect lighting", "cinematic lighting" without specifics,
ring lights, "golden hour light on the subject," "warm sunlight falling on her."

---

## CAMERA & LENS

### Combinations by Shot Type

| Shot Type | Camera | Lens | Why |
|---|---|---|---|
| Hero shot (full body) | Sony A7R V | 85mm f/1.8 | Portrait compression, clean bokeh |
| Detail close-up | Sony A7R V | 50mm f/2.0 | Natural perspective, honest |
| Lifestyle/motion | Sony A7R V | 50mm f/2.0 | Slightly wider for movement |
| 3/4 body | Sony A7R V | 85mm f/1.8 | Portrait compression |

### Framing Language
- Full body: `eye-level camera, full body head to toe, no wide-angle distortion`
- 3/4 body: `eye-level camera, mid-thigh to crown, no lens distortion`
- Detail crop: `camera at garment level, tight crop on [area], shallow DOF`

### Always Include
- `ISO 400` (adds natural grain — never ISO 100, too clean)
- `slight authentic sensor grain in shadows`
- `Photorealistic`

---

## CONSTRAINTS LIBRARY

Include the full block in every prompt. Tailor by adding category-specific lines.

### Standard Block (every prompt)
```
No airbrushing. No retouching. No skin smoothing. No beauty filter. No AI glow.
No plastic sheen. No waxy skin. No perfect symmetry. No CGI look. No illustration.
No watermark. No logo. No text overlay.
No direct sunlight on the model or garment — garment must be lit by soft neutral
diffused light only, so fabric color reads true-to-life.
Photorealistic. Feels like a photograph taken by a real photographer, not AI-generated.
```

### Skin Negatives
```
No uniform pore texture. No smooth forehead. No overly symmetrical features.
No skincare-ad aesthetic. No repeating texture pattern on skin. No mannequin look.
No doll-like features. No uncanny valley. No over-saturation.
```

### Eye Negatives
```
No dead eyes. No glassy doll eyes. No ring-light catchlight. No flat iris color.
No oversized catchlight. No perfectly round reflections.
```

### Anatomy Negatives (full-body shots)
```
No extra fingers. No fused fingers. No broken wrists. No distorted hands.
No warped proportions. No noodle arms. No broken joints. Correct human anatomy.
```

### Fabric Negatives
```
No flat fabric. No weightless drape. No fabric painted onto skin.
No uniform wrinkle pattern. No CGI fabric physics.
Fabric behaves with gravity and weight as real cloth would.
```

### Accessory Negatives
```
No oversized or chunky jewelry. No statement accessories that compete with the
hero product. Accessories must complement, not dominate. No floating jewelry.
No accessories defying gravity. No brand logos on accessories unless specified.
```

### Hero Product Protection
```
Do not alter the hero product's color, fabric texture, design, print, or
construction details. The hero product must be the most visually prominent
element in the frame — no other element should draw more attention at thumbnail.
```

---

## ANTI-SLOP WORD SUBSTITUTIONS

| Never Write This | Write This Instead |
|---|---|
| `realistic skin` | `visible fine pores, non-repeating organic microtexture, SSS at nose tip, vellus hair on jawline` |
| `beautiful lighting` | `large softbox key light 45° camera left, white reflector fill right, gradual shadow falloff` |
| `photorealistic` (alone) | `photorealistic — shot on Sony A7R V, 85mm f/1.8, ISO 400, slight sensor grain` |
| `natural expression` | `barely-there upward lift at mouth corners, eyes alive, gaze 15° past camera, relaxed jaw` |
| `real fabric texture` | `[fabric type], [weight], vertical parallel folds, crease at hip and inner thigh` |
| `standing naturally` | `contrapposto — weight on left leg, right hip elevated, shoulders counter-rotated, S-curve` |
| `realistic body` | `correct human proportions, head 1/8 of body height, natural limb length` |
| `brown/fair skin` | `warm medium-deep skin tone with golden undertone, natural radiance, refined pore texture` |
| `realistic eyes` | `visible iris fibers, natural catchlight, slight moisture at waterline, individual lash strands` |
| `8K ultra HD` | `shot on Sony A7R V, authentic sensor grain, natural sharpness — not over-processed` |
| `masterpiece` | `editorial fashion photograph — honest, candid, unretouched, real` |
| `perfect skin` | `natural skin with visible pores, slight sebum sheen, vellus hair, under-eye shadows, asymmetry` |
| `cinematic lighting` | `Rembrandt lighting — directional key from 45°, triangle highlight on cheek, fill at 1:3 ratio` |

**Words that TRIGGER the AI-Face problem (never use anywhere in a prompt):**
`flawless`, `perfect`, `stunning`, `beautiful`, `gorgeous`, `ideal`, `masterpiece`,
`8K`, `ultra HD`, `hyper-detailed`, `award-winning`, `glamour`, `airbrushed`,
`retouched`, `best quality`, `incredible detail`

---

## QUALITY CHECKLIST

Run through this before finalizing each prompt set.

### Hero Product Focus
- [ ] Hero product has the highest visual contrast in the frame
- [ ] Complementary garment is solid, simple, and less attention-grabbing
- [ ] Background contrasts with hero product (not same color family)
- [ ] Accessories don't compete with hero product
- [ ] At 150px thumbnail, hero product is immediately identifiable

### Background
- [ ] Background color is NOT in same family as hero product color
- [ ] Background is matte with subtle texture (not CGI-clean)
- [ ] Floor color clearly distinct from hero product hem
- [ ] Premium signal — draped fabric or textured surface

### Model
- [ ] Ethnicity matches user preference (or default applied)
- [ ] Hair creates contrast against background at thumbnail
- [ ] Expression is the fixed barely-there near-smile
- [ ] Body type is healthy and proportional

### Pose
- [ ] Pose suits the garment silhouette (see pose matrix)
- [ ] Pose creates visual energy or demonstrates garment feature
- [ ] Hands are explicitly addressed (Strategy A/B/C/D)

### Garment
- [ ] Hero product described with Five-Layer Framework
- [ ] Fabric physics language matches garment type
- [ ] Complementary garment is simple, solid, clean boundary
- [ ] "Preserve exact fabric color and drape" included

### Footwear
- [ ] Shoe color clearly different from nearest garment hem
- [ ] Shoe is premium-looking — no sandals, no sport shoes
- [ ] Hem-to-shoe transition is clean at thumbnail

### Skin & Eyes
- [ ] Three-layer undertone specified
- [ ] SSS, vellus hair, pore detail included
- [ ] Iris fibers, catchlight, waterline moisture included
- [ ] No anti-slop words anywhere in prompt

### Lighting & Camera
- [ ] No direct sunlight on model/garment
- [ ] Light type matched to fabric surface
- [ ] ISO 400 specified
- [ ] "Photorealistic" keyword included

### Consistency
- [ ] All prompts describe identical model, background, lighting, styling
- [ ] Only pose, angle, and framing change between prompts

---

## ITERATIVE REFINEMENT

When a generated image is close but not perfect, never rewrite the entire prompt.
Use surgical single-element edits:

```
Change: [one specific thing]
Preserve: face, identity, pose, skin texture, garment color, background, framing
Constraints: [repeat full constraints block]
```

### Escalation Blocks

**Skin still plastic:**
```
SKIN ESCALATION: Non-repeating organic pore pattern, visible capillaries near nose,
slight natural redness at nostril edges, one or two faint freckles, subtle pigmentation
variation. Not a skincare ad. Add: natural under-eye shadows, fine vellus hair catching
sidelight, slight sebum on T-zone.
```

**Eyes look dead:**
```
EYES ESCALATION: Visible iris radial fibers with darker limbal ring. Natural catchlight
matching light source shape. Slight moisture along lower waterline. Individual lash
strands with natural variation. Eyes must look alive and present, not glassy or vacant.
```

**Fabric looks flat or CGI:**
```
FABRIC ESCALATION: The fabric obeys gravity throughout. Hanging sections show parallel
fold lines. Contact points create compression folds. The fabric has weight — it drapes
over the body, not printed onto it. Surface light variation across folds.
```

**Hands look broken:**
```
HANDS ESCALATION: Correct human hand — 5 fingers, natural proportions, relaxed curl,
no extra joints. Skin matching the subject's undertone. Natural finger length, thumb
positioned correctly.
```

**Hero product doesn't stand out enough:**
```
HERO FOCUS ESCALATION: Increase background contrast — deepen or shift the background
color further from the hero product's hue. Simplify the complementary garment — make
it even more plain and visually recessive. Reduce accessory visibility. The hero product
must be the first thing the eye sees after the face.
```

**Image looks AI-generated overall:**
```
REALISM ESCALATION: Remove all beauty words. Add: candid, unposed, honest, no heavy
retouching, 35mm film grain. Add flyaway hairs. Add environmental imperfections. Add
under-eye shadows. Reduce symmetry. Add slight motion in hair or fabric.
```

**Background too clean:**
```
BACKGROUND ESCALATION: Include everyday details — slight surface wear, natural
imperfections. The environment should feel real, not a pristine CGI render. Add subtle
depth cues — draped fabric pooling naturally at base, slight wrinkle in backdrop.
```

**White garment color shifts:**
```
WHITE GARMENT FIX: The white garment must remain pure white — no yellow, cream, or warm
tint from lighting. Slight underexpose white highlights by 1/3 stop — fabric texture must
remain visible, not blown out.
```

---

## RECOMMENDED IMAGE GENERATION API SETTINGS

### For gpt-image-2 (OpenAI)
- **Quality:** `high`
- **Size:** `1024x1536` (2:3 — best for full-body)
- **Size for 3/4 body:** `1024x1536` (crop in prompt language)
- **Size for detail close-ups:** `1024x1024` or `1024x1536`

### For Gemini Image
- Follow the prompt structure exactly as written
- Include "photorealistic" keyword
- Use the same 2:3 aspect ratio for full-body shots

### Resolution Constraints (gpt-image-2)
- Max edge: < 3840px
- Both edges: multiples of 16
- Max aspect ratio: 3:1
- Recommended: `1024x1536` for all fashion photography
