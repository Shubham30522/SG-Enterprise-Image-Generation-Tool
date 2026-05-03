---
name: ai-fashion-photography-prompt
description: >
  Use this skill whenever the user asks you to write a prompt for AI image generation,
  specifically for fashion/clothing brand photography using gpt-image-2 (ChatGPT Images 2.0)
  or similar photorealistic image models. Triggers include: "write a prompt for my product",
  "generate a prompt for a model wearing X", "create an image prompt", "write me a prompt
  for ChatGPT image", or any request to produce a clothing brand visual with a human model.
  This skill acts as an Automated Art Director: automatically analyzing garments, determining
  optimal visual coverage (5-7 shots), and generating a cohesive set of production-ready prompts.
  It encodes hard-won best practices for achieving photorealistic skin texture,
  authentic body anatomy, garment fabric physics, and hand accuracy — making results
  indistinguishable from a real photograph.
---
 
# AI Fashion Photography Prompt Skill (v1.3 — Research-Enhanced + Community-Proven)
 
This skill produces structured, highly specific image generation prompts for clothing brand
photography. The goal is output that looks like a real photographer took it — not AI-generated.
Every prompt produced with this skill must follow the structure, skin physics language, anatomy
anchors, fabric physics language, and constraint system defined below.
 
## THE AUTOMATED ART DIRECTOR WORKFLOW
 
When a user provides a garment (via image upload + optional description), you must act as an Automated Art Director and execute the following 4-step process before outputting prompts:
 
### Step 1: Analyze the Product
Identify and internalize:
- **Garment Type:** (e.g., trousers, t-shirt, dress, jacket)
- **Key Design Elements:**
  - *Fit:* (slim, relaxed, oversized)
  - *Length:* (cropped, full-length, ankle-grazing)
  - *Structure:* (waistband, sleeves, collars, hems)
  - *Unique Features:* (pleats, pockets, prints, textures, stitching, asymmetrical cuts)
 
### Step 2: Determine Required Shot Count
Dynamically decide the number of images to generate:
- **Minimum:** 5 shots
- **Maximum:** 7 shots
- **Logic:** Simple items (e.g., basic tee) get 5 shots. Detailed/feature-rich items (e.g., cargo pants with hardware, detailed jackets) get up to 7 shots to capture all features.
 
### Step 3: Select Angles Intelligently
Classify and select angles based on the garment type to ensure complete product storytelling without redundancy.
 
**Must-Have Angles (Essential Coverage):**
- *Trousers / Bottomwear:* Waistband → hem (full vertical focus), Front full-body, Back full-body, etc.
- *Tops / T-Shirts:* Shoulder → waistband (clear torso focus), Front upper-body, Back upper-body, etc.
- *General Rule:* Always ensure clear visibility of the primary garment area, at least one front shot, one back shot, and one detail-focused shot.
 
**Should-Have Angles (Enhancement Shots):**
- Side profile, etc.
- 3/4 angle, etc.
- Close-up detail (fabric texture, stitching, waistband, collar, hardware), etc.
- Motion / lifestyle pose (if relevant to the garment's fit/drape), etc.
 
### Step 4: Generate Cohesive Prompts
Output the final set of 5–7 high-quality prompts. Each prompt must:
- Follow the **MANDATORY PROMPT STRUCTURE** and rules defined in this skill.
- **Maintain Absolute Consistency** across all images: Same model (identity, body type, hair, skin undertone), same lighting setup, same background, and same styling (accessories, secondary garments).
- Clearly define the pose and framing based on the selected angle.
- Clearly define garment visibility priority, camera position, and crop.
 
### Expected Output Format
When responding to the user, strictly structure your output as follows:
1. **Art Director Analysis:** A brief summary of the garment analysis (Step 1).
2. **Shot Plan:** Total image count (5-7) and the list of selected angles.
3. **The Prompts:** The 5-7 fully written prompts, one per angle, ready for generation.
 
---
 
## THE CORE PROBLEM THIS SKILL SOLVES
 
AI image models default to:
- Waxy, over-smooth "plastic" skin with no pores, no micro-texture, no imperfection
- Flat, unrealistic lighting that ignores physics
- Stylized, idealized faces that look like digital art, not photographs
- Anatomically broken bodies — especially hands, proportions, and unnatural poses
- Fabric that looks flat, weightless, or fake — no drape, no physics, no wrinkle logic
- Generic "beautiful" models that read as AI immediately
- Dead, doll-like eyes with no realistic reflections or iris detail
- Overly clean, staged backgrounds with no environmental imperfections
The fix is not vague realism language ("realistic skin", "photorealistic"). The fix is
**biological specificity** + **photography-first framing** + **fabric physics language**
+ **anatomical pose language** + **aggressive negative constraints** + **the word
"photorealistic" itself** (OpenAI confirms this keyword strongly engages the model's
photorealistic mode).
---
 
## MANDATORY PROMPT STRUCTURE
 
Always use the Scene / Subject / Body & Anatomy / Skin / Eyes / Garment / Accessories / Camera & Lighting / Use Case / Constraints template.
Never collapse these into a single paragraph.
 
```
Scene:
[where — location, background, time of day, light source and direction,
environmental micro-details for realism]
 
Subject:
[who — age, ethnicity, body type, pose with contrapposto language, expression,
hair texture and flyaway details]
 
Body & Anatomy:
[weight distribution, joint positions, hand state, anatomical anchors]
 
Skin:
[skin physics vocabulary — pores, SSS, vellus hair, sebum zones, undertone,
grain, under-eye detail, imperfections]
 
Eyes:
[iris detail, catchlight shape, moisture, gaze direction, eyelash detail]
 
Garment:
[fabric type, weave, weight, drape behavior, fit on body, wear signs, construction]
 
Accessories:
[gender-appropriate accessories that complement the outfit — shoes, watch,
jewelry, bag — with material, color, and wear detail]
 
Camera & Lighting:
[sensor/film stock, lens, ISO, aperture, light source, direction, fill,
what light does to fabric, color temperature]
 
Use case:
[editorial fashion photograph / lookbook / e-commerce / campaign visual]
 
Constraints:
[explicit negatives — anatomy, skin, fabric, face, eyes, accessories —
everything the model must NOT do]
```
 
Ten sections solve ten separate problems:
1. WHERE the image exists (including environmental realism)
2. WHO the subject is (including hair micro-detail)
3. HOW the body is physically positioned (prevents broken anatomy)
4. WHAT skin micro-details must be visible
5. HOW the eyes read as alive and real
6. HOW the fabric behaves physically on the body
7. WHAT accessories complete the outfit and how they interact with the body
8. WHAT camera, film stock, and light physics apply
9. WHAT kind of finished image is expected
10. WHAT must not drift or default
---
 
## SKIN TEXTURE: THE BIOLOGICAL VOCABULARY
 
Replace vague phrases like "realistic skin" with specific biological terms.
 
### Pore & Surface Detail
- `visible fine pores on cheeks and nose`
- `non-repeating organic pore distribution — denser on nose, finer on cheeks`
- `natural skin micro-texture across forehead and chin`
- `microtexture mapping across the skin surface — not uniform, not repeating`
- `super realistic skin pores — micro-pores visible at full resolution`
### Subsurface Scattering (the anti-plastic fix)
- `subsurface scattering visible at ear edges and nose tip — faint warm translucency`
- `light penetrates the top layer of skin at the nose bridge, soft glow not hard plastic reflection`
- `translucent quality at the inner corners of the eyes and nostril edges`
### Vellus Hair (single biggest AI giveaway when missing)
- `soft peach fuzz (vellus hair) on jawline and cheekbones catching the side light`
- `fine facial vellus hairs visible on the upper lip and forehead in raking light`
- `micro-hair strands along the hairline catching backlight`
### Flyaway Hair Detail (adds instant realism)
- `loose wisps and flyaway hairs around the crown and temples`
- `a few stray strands breaking the hair silhouette — not perfectly styled`
- `natural hair texture with micro-strands catching the light`
### Undertone Specificity (prevents "grey zombie" skin)
Always describe three layers: **tone + undertone + surface finish**:
- `warm medium-deep skin tone with golden undertone, natural radiance`
- `light skin with cool pink undertone, slightly dewy surface`
- `olive skin with warm neutral undertone, refined pore texture`
- `deep skin with warm bronze undertone, subtle satin finish — not glossy`
> Do NOT say "brown skin" or "fair skin" alone. Undertone determines how light reads.
> Pick lighting congruent with the undertone: warm golden light for warm undertones;
> cool window light for cool/neutral undertones.
 
**Undertone by ethnicity:**
- South Asian / Indian: `warm golden-olive undertone`
- East Asian: `warm neutral to cool undertone, porcelain or ivory surface`
- West African: `deep warm undertone with bronze-amber depth`
- Middle Eastern: `warm olive with golden base undertone`
- Latin/Mediterranean: `warm neutral to olive undertone, slight golden cast`
- Northern European: `light skin with cool pink or neutral undertone`
- Scandinavian: `very light skin with cool neutral undertone, porcelain surface`
### Specular Variation (oily vs dry zones)
- `slight natural sebum sheen on nose bridge and center forehead only`
- `matte texture on cheeks and jawline`
- `gradual highlight roll-off on the cheekbones — not a sharp specular spike`
- `dewy but not glossy — natural skin moisture`
### Under-Eye Detail (commonly overlooked realism cue)
- `natural under-eye shadows — slight darkness, not concealed`
- `faint blue-purple vein visibility beneath the under-eye skin`
- `thin, delicate skin texture below the lower lash line`
### Imperfections That Prove Humanity
- `subtle natural pigmentation variation — warmer on cheeks, cooler at temples`
- `faint expression lines at the outer eye corners`
- `one or two faint natural freckles on the nose bridge`
- `slight natural redness at nostril edges and inner eye corners`
- `very slight asymmetry in facial features — not perfect symmetry`
- `natural blemishes — a faint mole, a tiny imperfection — real skin is not uniform`
### Film/Sensor Grain
- `shot on Sony A7R V, 85mm f/1.8, ISO 400 — slight sensor grain in shadow areas`
- `subtle authentic film grain, Kodak Portra 400 feel`
- `analog 35mm grain structure — organic noise, not digital sharpening artifacts`
---
 
## EYE REALISM: THE ANTI-DOLL VOCABULARY
 
AI-generated eyes are a major giveaway. Always include eye-specific language:
 
### Iris Detail
- `visible iris texture — fine radial fibers, not flat color disc`
- `slight color variation within the iris — darker limbal ring at the edge`
- `natural iris pattern — unique, organic, not perfectly circular`
### Catchlight & Reflection
- `one natural rectangular softbox catchlight in the iris — not ring light`
- `realistic eye reflections showing the environment/light source`
- `soft, natural catchlight — not oversized, not perfectly round`
### Moisture & Life
- `slight moisture visible along the lower waterline`
- `natural eye moisture — not dry, not over-glossy`
- `the eyes look alive and present, not glassy or vacant`
### Eyelash Detail
- `individual lash strands visible — not a uniform dark line`
- `natural lash length variation — some longer, some shorter`
- `a few lashes slightly crossing or out of alignment`
---
 
## BODY ANATOMY: THE ANTI-BROKEN-BODY VOCABULARY
 
### Pose — Use Contrapposto Language, Not Generic Stance
Instead of: `standing with weight on left leg`
Use: `contrapposto stance — weight bearing on left leg, right hip slightly elevated,
shoulders counter-rotated left, natural S-curve in spine visible`
 
More contrapposto cues:
- `weight shifted to right hip, left knee slightly bent, torso angled 3/4 to camera`
- `relaxed hip drop — one hip 2–3cm lower than the other, natural weight distribution`
- `standing mid-stride — weight transitioning between feet, natural momentum in posture`
- `seated with slight forward lean, weight on sitting bones, spine naturally lengthened`
> Why this works: "Standing" gives the AI no physics. Contrapposto with weight distribution
> and shoulder counter-rotation gives the model a skeletal geometry to solve.
> This is the difference between a wooden mannequin and a living person.
 
### Body Proportion Anchors
Always include:
- `correct human proportions — head is 1/8 of total body height`
- `natural body structure, realistic anatomy`
- `realistic limb length — arms reaching mid-thigh when relaxed`
For fuller body types:
- `full-figured, soft and rounded figure with natural proportions` (NOT "fat" or "overweight")
- `realistic proportions, natural representation — not caricature, not exaggerated`
For curvy body types:
- `hourglass figure — visibly defined natural waist, fuller hips and bust, curvaceous but proportionate silhouette, realistic representation, not exaggerated`
- `naturally curvy and healthy — not too slim, not plus-size, soft feminine curves with natural body confidence`
### Hands — The Most Common AI Failure
Always handle hands explicitly. Choose one strategy:
 
**Strategy A — Describe hand state (safest):**
```
Right hand resting loosely at hip, fingers naturally relaxed and slightly curled —
not stiff, not splayed. Left hand hanging at side, palm facing inward.
Correct finger count, proportional hand size relative to body.
```
 
**Strategy B — Give hands an object (easiest):**
```
Left hand holding a small clutch bag naturally — fingers wrapped around grip, thumb visible.
```
 
**Strategy C — Crop hands (if not needed):**
```
Framing: 3/4 body shot from mid-thigh up — hands not in frame.
```
 
**Strategy D — Natural hand positioning with reinforcement:**
```
Hands in natural resting position — realistic finger proportions,
five fingers on each hand, relaxed curl, no extra joints.
```
 
### Anatomy Negatives (always include for full-body shots):
```
No extra fingers. No fused fingers. No missing fingers. No broken wrist angle.
No distorted hands. No noodle arms. No broken joints. No warped proportions.
Correct anatomy throughout.
```
 
---
 
## LIGHTING: THE PHYSICS RULE
 
### CRITICAL: No Direct Sunlight on Model or Garment
 
> **NEVER use direct sunlight, golden hour light, or any hard natural light falling
> directly on the model or the garment.** Direct sunlight causes color temperature
> shifts on fabric — the garment will appear a different color in the AI image than
> it does in real life. This creates a mismatch between what the customer sees on
> their phone and what they receive. Warm sunlight turns navy into purple, shifts
> black into brown, makes white look yellow, and distorts every color in between.
>
> **Rule:** All lighting on the model and garment must be **soft, diffused, and
> color-neutral** (daylight-balanced ~5500K). If sunlight is desired for atmosphere,
> use it **only in the background** — e.g., sunlit wall behind the subject, warm
> light spilling on the ground behind them, golden glow on distant architecture.
> The subject herself must remain in open shade, diffused overcast light, or
> controlled soft studio light so that the garment color reads true-to-life.
>
> **How to prompt outdoor warmth without color-shifting the garment:**
> - `subject standing in open shade, background wall catching warm late-afternoon sunlight`
> - `model in diffused overcast light, distant buildings glowing with golden hour warmth`
> - `garment lit by soft neutral daylight — warm sunlight visible only on the background surfaces`
 
### The Fabric-Lighting Relationship (critical for garment realism)
| Fabric type | Best light | Why |
|---|---|---|
| Silk, satin, charmeuse | Hard key from 45° | Creates specular highlights revealing sheen |
| Cotton, linen, jersey | Soft octabox / overcast | Reveals weave texture, matte surface |
| Denim, twill, corduroy | Raking sidelight | Catches woven ridges and surface texture |
| Sheer, chiffon | Backlight + soft front fill | Translucency only visible with backlight |
| Velvet | Single directional key | Nap shadow direction visible |
 
### Lighting Setups for Maximum Realism
 
| Lighting Type | Best For | How to Prompt |
|---|---|---|
| **Softbox Key** | Studio fashion, lookbook | `large softbox key light 45° to camera left at eye level, gentle bounce fill from white reflector on the right` |
| **Golden Hour** | Warm outdoor, lifestyle | `golden hour sunlight casting warm rim light, long soft shadows, natural color temperature around 3500K` |
| **Window Light** | Indoor, intimate portraits | `soft diffused daylight through a window, gentle catchlight in eyes, natural shadow transitions` |
| **Rembrandt** | Dramatic, editorial | `classic Rembrandt lighting — directional light from 45° creating a small triangle of light on the opposite cheek` |
| **Overcast/Flat** | Ultra-natural, unstyled | `flat overcast daylight, even soft illumination, no harsh shadows, natural white balance` |
| **Fluorescent/Urban** | Night street, documentary | `harsh fluorescent lighting with slight green color cast, mixed with neon reflections` |
| **35mm Film Look** | Nostalgic, authentic | `35mm film photograph, subtle film grain, slight color shift, natural highlight roll-off` |
 
### Always Specify:
- `sculpting shadows on the non-lit side of the face`
- `soft raking key catching the weave texture of the [fabric]`
- `one natural rectangular softbox catchlight in the iris — not ring light`
- Color temperature when relevant: `natural color temperature around 3500K` (golden) or `5500K` (daylight)
### Lighting Language That Kills Realism (NEVER USE)
- "beautiful lighting", "perfect lighting", "cinematic lighting" without specifics, ring lights.
- **Direct sunlight on model or garment** — causes fabric color shift between screen and real life.
- "golden hour light on the subject" — use only on background, never on the model/garment.
- "warm sunlight falling on her" — the garment must stay in neutral diffused light.
---
 
## CAMERA & LENS SPECS
 
**Key insight from OpenAI official prompting guide**: Prompt the model as if a real photo
is being captured in the moment. Use photography language and explicitly ask for real texture.
Avoid words that imply studio polish or staging. Include the word **"photorealistic"**
directly — OpenAI confirms this strongly engages the model's photorealistic mode.
 
### Camera + Lens Combinations by Style
 
| Look | Camera | Lens | Effect | Best for |
|------|--------|------|--------|----------|
| Professional portrait | Sony A7R V / Canon EOS R5 | 85mm f/1.8 | Portrait compression, creamy bokeh | Hero shots, face detail |
| Editorial fashion | Hasselblad X2D 100C | 50mm f/1.4 | Medium format depth, studio-quality | High-end editorial, campaigns |
| Natural / documentary | Sony A7R V | 50mm f/2.0 | Natural perspective, honest feel | Lookbook, lifestyle |
| Candid street | Leica M10 | 35mm f/2.0 | Candid, slightly wide | Street style, casual |
| iPhone snapshot | iPhone 15 Pro | built-in | Slightly off-center, casual | Social media, candid lifestyle |
| Film photography | Analog 35mm body | 50mm f/2.0 | Grain, color shift, soft roll-off | Nostalgic, authentic |
| Runway / product focus | Sony A7R V | 70–200mm | Telephoto compression | Product-focused, garment detail |
 
### Film Stock Language (when film aesthetic desired)
| Film Stock | Characteristics | Best For |
|---|---|---|
| Kodak Portra 400 | Warm skin tones, fine grain, natural colors | Portraits, fashion |
| Kodak Portra 800 | Slightly more grain, warm tones, works in low light | Evening, indoor |
| Fuji Pro 400H | Cool greens, pastel rendering, soft contrast | Lifestyle, editorial |
| Kodak Ektar 100 | Vivid, saturated, fine grain | Bright daylight, outdoor |
| Ilford HP5 Plus | Black and white, punchy contrast, visible grain | Dramatic editorial, art |
| CineStill 800T | Tungsten balanced, halation glow, cinematic | Night/urban, neon-lit |
 
Always: `ISO 400` (adds grain). Never: `ISO 100` (too clean — reads as digital render).
 
**Framing language that prevents distortion:**
- Full body: `eye-level camera, full body head to toe, no wide-angle distortion`
- 3/4: `eye-level camera, mid-thigh to crown, 3/4 framing, no lens distortion`
---
 
## GARMENT DESCRIPTION LANGUAGE
 
### The Five-Layer Framework:
1. **Color** (precise: "dusty terracotta" not "orange", "slate teal" not "blue")
2. **Fabric type + weave** ("cotton-twill", "linen plain weave", "jersey stretch knit", "silk charmeuse")
3. **Weight & behavior** ("medium-weight with structured body", "lightweight with fluid drape")
4. **Fit behavior** ("sits naturally on fuller hips", "slight drag crease at the thigh")
5. **Construction details** ("flat waistband with internal elastic", "gently flared leg from knee")
**Always add:** `preserve the exact fabric color and drape`
 
### Fabric Physics Language by Type:
 
**Wide-leg / Palazzo:**
```
Wide-leg silhouette in [fabric]. Leg panels fall with natural gravity — vertical parallel
fold lines running down the front panel. Side seams hang straight and true.
Slight sway creates diagonal tension lines across the thigh. Not stiff, not flat —
natural hanging cloth weight visible throughout.
```
 
**Mom-fit / Tapered:**
```
High-rise waistband lying smooth and flat. Fitted through hip and upper thigh —
slight compression fold at inner thigh from the natural body shape.
Taper from knee to ankle. Front crease line running from waistband to hem.
Slight drag crease at the hip crease where leg meets torso.
```
 
**Flared / Bell-bottom:**
```
Fitted at hip and thigh, flaring dramatically from knee downward. Flare panels
catch light differently from the fitted upper. Hem drapes to the floor with slight
break at the ankle. Movement causes the flare to sweep and catch air — organic
flowing motion lines across the lower leg.
```
 
**Oversized / Boxy T-shirt:**
```
Oversized boxy silhouette — drop shoulders with sleeve seam falling 3–4 inches
below the natural shoulder point. The body drapes loosely over the torso with
slight blousing where the hem meets the hip. Soft vertical fold lines at the sides
where excess fabric gathers. Short sleeves ending above the elbow with a relaxed
straight-cut opening. Fabric falls with natural gravity — not stiff, not skin-tight,
real cloth weight visible throughout.
```
 
---
 
## ACCESSORIES: COMPLETING THE OUTFIT
 
Every prompt must include **gender-appropriate accessories** that complement the garment
without competing with it. Accessories ground the image in reality — a real person wears
shoes, a watch, maybe a necklace. Missing accessories make the image look like a
mannequin display.
 
### The Accessory Rules:
 
1. **Always include shoes** — barefoot reads as AI-generated or stock photo.
2. **Always complement, never compete** — accessories support the garment, they don't steal focus.
3. **Match metal tones to garment temperature** — cool-toned garments (blue, purple, grey) pair
   with silver/platinum metals. Warm-toned garments (caramel, red, earth) pair with gold/rose-gold.
4. **Keep it minimal for streetwear** — 2–3 accessories maximum. Overstyling reads as catalogue.
5. **Describe material and wear** — accessories need the same realism treatment as garments.
   A watch has a strap, a necklace has weight, shoes have creases.
6. **Gender-specific choices** — use accessories appropriate to the subject's gender presentation.
### Accessory Selection by Garment Style:
 
| Garment Style | Recommended Accessories | Why |
|---|---|---|
| Oversized streetwear tee | Clean minimal sneakers, slim watch, delicate chain necklace | Balances the relaxed silhouette with subtle detail |
| Fitted formal top | Heeled boots or pointed flats, structured bag, elegant earrings | Matches the refined silhouette |
| Casual / lifestyle | Canvas sneakers or loafers, simple bracelet, crossbody bag | Keeps the easy, everyday feel |
| Edgy / urban | Chunky boots, layered chain, ring stack | Reinforces the attitude |
| Feminine / soft | Minimal sandals or ballet flats, pendant necklace, stud earrings | Supports the delicate aesthetic |
 
### Accessory Selection by Garment Color (metal tone matching):
 
| Garment Color | Metal Tone | Why |
|---|---|---|
| Cool tones (navy, purple, grey, blue) | Silver, platinum, white gold | Cool metal harmonizes with cool fabric |
| Warm tones (caramel, red, orange, earth) | Gold, rose gold, brass | Warm metal harmonizes with warm fabric |
| Neutral (black, white, cream) | Either — silver or gold both work | Neutrals are flexible |
| Mixed warm-cool | Silver is the safer default | Less risk of clashing |
 
### Accessory Physics Language (realism details):
 
**Shoes:**
```
Clean white minimal leather sneakers — low-profile silhouette, white rubber sole.
Lightly worn — faint natural crease at the toe bend, subtle scuff near the sole edge.
Laces tied naturally, not perfectly symmetrical.
```
 
**Watch:**
```
Slim minimalist silver-toned wristwatch on the left wrist — clean round face,
thin case, simple strap. The watch sits naturally on the wrist — not floating,
not too tight. Faint soft highlight on the watch crystal from the ambient light.
```
 
**Necklace:**
```
Delicate thin silver chain necklace with a tiny minimalist pendant resting
naturally just below the collarbone — sitting on top of or just inside the
neckline. The chain drapes with natural gravity, not perfectly centered.
Faint glint of diffused light on the chain links.
```
 
**Earrings:**
```
Small simple silver stud earrings — subtle, not statement. Visible only
when hair is pulled back or tucked behind the ear.
```
 
### Accessory Negatives (add to Constraints):
```
No oversized or chunky jewelry. No statement accessories that compete with the
garment graphic. Accessories must complement, not dominate. No floating jewelry.
No accessories that defy gravity. No brand logos on accessories unless specified.
```
 
---
 
## SUBJECT DESCRIPTION LANGUAGE
 
### Body Type
Use: `hourglass figure — visibly defined natural waist, fuller hips and bust,
curvaceous but proportionate silhouette — realistic representation, not exaggerated`
 
Add body-garment interaction:
`the trousers sit naturally on her fuller hips, waistband lying flat and smooth`
 
### Expression (never "beautiful" or "confident")
- `natural resting expression — lips slightly parted, not smiling, not posed`
- `honest, unposed expression — like a photographer caught her between shots`
- `direct gaze, slight natural squint from the light`
- `candid caught-mid-thought expression`
- `relaxed, genuine expression — not posing for camera`
### Words That TRIGGER the AI-Face Problem (NEVER USE)
`flawless`, `perfect`, `stunning`, `beautiful`, `gorgeous`, `ideal`, `masterpiece`,
`8K`, `ultra HD`, `hyper-detailed`, `award-winning`, `incredible detail`,
`glamour`, `airbrushed`, `retouched`, `best quality`
 
> **Why these fail:** "8K" and "ultra HD" trigger over-sharpening artifacts.
> "masterpiece" and "best quality" push toward generic stock-image aesthetics.
> "glamour" and "airbrushed" directly activate skin-smoothing behavior.
 
---
 
## SCENE & BACKGROUND REALISM
 
### Outdoor / On-Location Backgrounds
When shooting outside a studio, add environmental micro-details that prove
the scene is real:
 
- `include everyday environmental details — slight dust, natural wear on surfaces`
- `imperfect background — real-world textures, not a pristine render`
- `natural environmental imperfections — chipped paint, weathered stone, scuff marks on ground`
- `ambient environmental elements — distant figures blurred, stray objects at frame edges`
### Background Selection by Garment Color (complementary contrast)
| Garment Color | Complementary Background | Why |
|---|---|---|
| Deep navy / indigo | Warm sandstone, terracotta, honey-toned architecture | Warm-cool contrast makes blue pop |
| White / cream | Dark moody tones, charcoal concrete, deep wood | Value contrast highlights the garment |
| Black | Light neutral walls, pale concrete, soft grey stone | Clean separation without competing |
| Red / burgundy | Cool grey stone, blue-grey urban, muted concrete | Cools the palette, lets red dominate |
| Earth tones / khaki | Cool-toned urban, slate, steel, blue-hour sky | Temperature contrast adds dimension |
| Pastel / soft pink | Warm neutral, cream stone, soft golden surfaces | Harmonious warmth without washing out |
| Bright / vivid colors | Desaturated, muted backgrounds — grey, concrete, fog | Lets the garment be the only color anchor |
 
### Background Types to Avoid Unless Specifically Requested
- Generic garden / greenery (reads as stock photo)
- Pure white void (reads as e-commerce cutout, not editorial)
- Heavily blurred "bokeh balls" background (reads as AI-generated)
- Overly dramatic landscapes competing with the garment
---
 
## THE CONSTRAINTS SECTION: CRITICAL
 
### Standard Block (every prompt):
```
No airbrushing. No retouching. No skin smoothing. No beauty filter. No AI glow.
No plastic sheen. No waxy skin. No perfect symmetry. No CGI look. No illustration.
No watermark. No logo. No text overlay. Slight authentic sensor grain in shadows.
No direct sunlight on the model or garment — garment must be lit by soft neutral
diffused light only, so fabric color reads true-to-life.
Photorealistic. Feels like a photograph taken by a real photographer, not AI-generated.
```
 
### Skin Negatives:
```
No uniform pore texture. No smooth forehead. No overly symmetrical features.
No skincare-ad aesthetic. No studio beauty lighting. No repeating texture pattern on skin.
No mannequin look. No doll-like features. No uncanny valley.
No over-saturation. No dramatic color grading.
```
 
### Eye Negatives:
```
No dead eyes. No glassy doll eyes. No ring-light catchlight. No flat iris color.
No oversized catchlight. No perfectly round reflections.
```
 
### Anatomy Negatives (full-body shots):
```
No extra fingers. No fused fingers. No broken wrists. No distorted hands.
No warped proportions. No noodle arms. No broken joints. Correct human anatomy throughout.
```
 
### Fabric Negatives:
```
No flat fabric. No weightless drape. No fabric painted onto skin.
No uniform wrinkle pattern. No CGI fabric physics.
Fabric behaves with gravity and weight as real cloth would.
```
 
---
 
## THE ANTI-SLOP WORD SUBSTITUTION LIST (v1.3 — Expanded)
 
| Instead of this... | Use this... |
|---|---|
| `realistic skin` | `visible fine pores, non-repeating organic microtexture, SSS at nose tip, vellus hair on jawline` |
| `beautiful lighting` | `large softbox key light 45° camera left, white reflector fill right, gradual shadow falloff` |
| `photorealistic` (alone) | `photorealistic — shot on Sony A7R V, 85mm f/1.8, ISO 400, slight sensor grain — honest and unposed` |
| `natural expression` | `lips slightly parted, not smiling, eyes direct, relaxed jaw, honest unposed expression` |
| `hourglass figure` | `visibly defined natural waist, fuller hips and bust, curvaceous proportionate silhouette, realistic` |
| `real fabric texture` | `cotton-twill, medium weight, vertical parallel folds in hanging panels, crease at hip and inner thigh` |
| `professional photography` | `editorial fashion photograph, 85mm lens, octabox key light at 45°, grey seamless backdrop` |
| `no AI look` | `no plastic sheen, no smooth skin, no AI glow, no beauty filter, no perfect symmetry, no extra fingers` |
| `standing naturally` | `contrapposto stance — weight on left leg, right hip elevated, shoulders counter-rotated, natural S-curve` |
| `realistic body` | `correct human proportions, head 1/8 of body height, natural limb length, anatomically accurate` |
| `brown/fair skin` | `warm medium-deep skin tone with golden undertone, natural radiance, refined pore texture` |
| `good lighting` | `soft diffused daylight at 45°, gentle catchlight in eyes, natural shadow transitions, color temp 5500K` |
| `realistic eyes` | `visible iris fibers, natural catchlight, slight moisture at waterline, individual lash strands` |
| `8K ultra HD` | `shot on Sony A7R V, high resolution, authentic sensor grain, natural sharpness — not over-processed` |
| `masterpiece` | `editorial fashion photograph — honest, candid, unretouched, real` |
| `cinematic lighting` | `Rembrandt lighting — directional key from 45° creating triangle highlight on cheek, fill at 1:3 ratio` |
| `perfect skin` | `natural skin with visible pores, slight sebum sheen on nose, vellus hair, under-eye shadows, asymmetry` |
 
---
 
## COMPLETE PROVEN PROMPT TEMPLATE (v1.3)
 
```
Scene:
[LOCATION]. [Environmental micro-details — surface wear, texture, imperfections].
[Light source type] positioned [direction and angle], [what shadows do].
[Fill light source]. [Time of day and color temperature].
No [unwanted background elements]. [Atmosphere — dry/humid/warm/cool].
 
Subject:
A [GENDER] in [their AGE RANGE], [ETHNICITY], [UNDERTONE description].
[BODY TYPE — with specific language per the Body Type section].
[Expression — using anti-slop vocabulary]. [Hair description including
flyaway details and micro-strands]. [Gaze direction].
 
Body & Anatomy:
[Contrapposto or specific pose with weight distribution language].
[Hand state — using Strategy A, B, C, or D].
[Arm positions with specific joint angles].
Correct human proportions — head is 1/8 of total body height.
Natural limb length. Correct anatomy throughout.
 
Skin:
[Three-layer undertone: tone + undertone + surface finish].
Visible fine pores on cheeks and nose — non-repeating organic pore distribution,
denser on nose, finer on cheeks. Soft peach fuzz (vellus hair) on jawline and
cheekbones catching the side light. Subsurface scattering visible at ear edges and
nose tip — faint warm translucency. Natural pigmentation variation — [specific zones].
[Sebum zones]. Gradual highlight roll-off on cheekbones — not a sharp specular spike.
[Age-appropriate imperfections]. Very slight asymmetry in facial features.
Natural under-eye shadows — slight darkness, not concealed.
 
Eyes:
Visible iris texture — fine radial fibers, slight color variation, darker limbal ring.
[Catchlight shape matching the light source]. Slight moisture along the lower waterline.
Individual lash strands — natural length variation. Eyes look alive and present.
 
Garment:
[EXACT GARMENT using the Five-Layer Framework:
1. Precise color name
2. Fabric type + weave
3. Weight & behavior
4. Fit behavior on this body type
5. Construction details].
Paired with [SECONDARY GARMENT].
[Fabric physics language appropriate to this garment type].
Preserve the exact fabric color, graphic design, and natural drape.
 
Accessories:
[SHOES — type, color, material, wear details, how they sit on the ground].
[WATCH or BRACELET — metal tone matching garment temperature, strap, fit on wrist].
[NECKLACE or EARRINGS — if appropriate, delicate, complementary, not competing].
All accessories gender-appropriate and complementary to the outfit.
Accessories have natural wear and physics — not floating, not pristine.
 
Camera & Lighting:
[Camera body], [lens], ISO 400, [aperture].
[Camera position and framing — eye-level, angle, crop].
[Key light — type, position, angle, what it does to skin and fabric].
[Fill light — type, position, ratio to key].
[What light does to the fabric weave texture].
[Catchlight description].
[Color temperature if relevant].
Photorealistic.
 
Use case:
[Editorial fashion lookbook / e-commerce / campaign visual / lifestyle].
 
Constraints:
[Full Standard Block].
[Skin Negatives].
[Eye Negatives].
[Anatomy Negatives — for full-body shots].
[Fabric Negatives].
[Accessory Negatives].
[Scene-specific negatives — e.g., "No garden. No greenery."].
Do not alter the garment graphic design, color, or placement.
Slight authentic sensor grain in shadows.
Photorealistic. Feels like a photograph taken by a real photographer, not AI-generated.
```
 
---
 
## ALTERNATIVE PROMPT STYLES
 
### Style A — Film Photography Aesthetic
When the user wants a nostalgic, analog feel:
```
Analog 35mm film photography, [FILM STOCK e.g., Kodak Portra 400 / Fuji Pro 400H],
soft [AESTHETIC] aesthetic,
gentle diffused [LIGHT SOURCE],
slight overexposure, pastel tones, low contrast,
soft highlights, [SETTING DESCRIPTION],
[PERSON DESCRIPTION with full skin detail vocabulary],
[outfit description using Five-Layer Framework],
[contrapposto pose description],
focus on light, air, and quiet everyday mood,
soft film grain, dreamy and understated atmosphere.
Photorealistic. No AI glow. No plastic skin. No watermark.
```
 
### Style B — Candid/Documentary (Most "Real" Looking)
When the user wants maximum authenticity:
```
A candid photograph — like someone quickly pulled out their camera and captured
a real moment. [PERSON DESCRIPTION] [IN SITUATION].
Slightly off-center framing, imperfect composition.
Natural, unposed moment. [PERSON] is [ACTION/POSE].
[Full skin vocabulary — pores, sebum, vellus hair, under-eye shadows, flyaway hairs].
[ENVIRONMENT with everyday details — dust, slight mess, natural imperfections].
[SPECIFIC LIGHTING — not "good lighting"].
Shot on [Leica M10 / 35mm film camera], [35mm f/2], natural light,
slight motion blur acceptable, authentic snapshot quality.
Photorealistic. Not overly polished — should look like a real candid photo.
No glamorization, no beauty filters, no staged posing.
```
 
### Style C — Korean Photobook / Soft Editorial
When the user wants an intimate, soft-focus editorial look:
```
9:16 vertical — portrait photography,
soft black mist filter effect, lowered contrast,
gentle highlight bloom, subtle glow, soft diffusion.
[SETTING: minimal indoor near window, white curtains, clean background].
[PERSON: age, ethnicity, full skin texture vocabulary, natural makeup].
[outfit using Five-Layer Framework].
[hair style with flyaway detail].
[contrapposto or intimate pose].
[unposed expression].
Camera: [framing] with intimate distance, slight handheld feel.
Lighting: diffused natural daylight, soft shadows.
Mood: [intimate, everyday, romantic, quiet].
Quality: photorealistic, fine film grain, subtle analog softness,
natural imperfections, dreamy understated tone.
No plastic skin. No AI glow. No watermark.
```
 
### Style D — Urban Night / Neon Editorial
When the user wants a moody, night-time urban look:
```
35mm film photography with harsh [fluorescent / convenience store / neon] lighting
mixed with colorful neon signs from outside,
authentic film grain, high contrast, slight color cast,
cinematic street editorial style, intimate medium shot,
[PERSON DESCRIPTION with full skin vocabulary],
[outfit using Five-Layer Framework],
[pose/action at location],
[environment details — glass reflections, store interior, wet streets, etc.],
[FILM STOCK] color grading — [CineStill 800T for tungsten halation /
Kodak Portra 800 for warm grain].
Photorealistic. No plastic skin. No watermark. No text.
```
 
---
 
## ADVANCED TECHNIQUES
 
### Technique 1: "Describe-Then-Generate" Method
Instead of writing the prompt yourself, ask the AI to describe the image first,
then generate from its own description:
 
**Step 1:**
> "Describe in extremely vivid details what a photorealistic photo of [YOUR IDEA]
> would look like. Be very elaborate about lighting, skin texture, fabric physics,
> and environment details. No word limit."
 
**Step 2:**
> "Now generate the photo using your description. Make it photorealistic with
> visible pores and natural skin texture."
 
**Why it works:** The text model is autoregressive and responds better to richly
written context. Long descriptions give it the "reasoning" it needs to place
elements logically and aesthetically. The image model then follows this detailed
spec more faithfully than a shorter user-written prompt.
 
### Technique 2: Style Reference Transfer
Upload a reference photo whose style/lighting you want to replicate, then:
```
"Use the style, lighting, and color grading from the first image.
Apply it to the person in the second image.
Keep the person's exact facial features, skin tone, and identity.
Generate a new photorealistic portrait with realistic skin texture,
visible pores, and natural imperfections."
```
 
### Technique 3: Multi-Image Compositing
Upload multiple reference images and specify each one's role:
```
"Image 1: the person (preserve identity exactly).
Image 2: the outfit (dress the person in these clothes — preserve exact color and design).
Image 3: the background/scene (place the person in this environment).
 
Do not change face, facial features, skin tone, body shape, or identity.
Match lighting, shadows, and color temperature so the composite looks
photorealistic — nothing should look pasted on.
Preserve exact garment color, fabric texture, and graphic design from Image 2."
```
 
### Technique 4: Face Identity Locking
When using a reference face photo:
1. Upload a **tight crop** of the face (ears touching edges, hair at top, neck at bottom)
2. Prompt:
```
"Use the uploaded image as the primary reference.
Keep facial features IDENTICAL — exact same eyes, nose, mouth,
face shape, and proportions.
The face must be immediately recognizable as the person in the reference photo.
[SCENE DESCRIPTION].
Photorealistic, realistic skin texture with visible pores."
```
 
> **Pro Tip:** Don't upload full-body photos for face reference. Too much extra
> visual information dilutes the face accuracy. Crop tightly to just the face.
 
---
 
## ITERATIVE REFINEMENT STRATEGY
 
When the first result is close but not perfect, **never rewrite the entire prompt**.
Use surgical single-element edits:
 
```
Change: [one specific thing]
Preserve: face, identity, pose, skin texture, garment color, background, framing
Constraints: [repeat full constraints block]
```
 
### Escalation Blocks:
 
**Skin still plastic:**
```
SKIN ESCALATION: Non-repeating organic pore pattern, visible capillaries near the nose,
slight natural redness at nostril edges, one or two faint freckles, subtle pigmentation
variation — the skin should look like a surface, not a mask. Not a skincare-ad.
Add: natural under-eye shadows, fine vellus hair catching sidelight, slight sebum on T-zone.
```
 
**Eyes look dead or doll-like:**
```
EYES ESCALATION: Visible iris radial fibers with darker limbal ring. Natural catchlight
matching the light source shape — not ring light. Slight moisture along lower waterline.
Individual lash strands with natural variation. The eyes must look alive and present,
not glassy or vacant.
```
 
**Fabric looks flat or CGI:**
```
FABRIC ESCALATION: The [fabric type] obeys gravity throughout. Hanging sections show
parallel fold lines. Points of contact with the body create compression folds.
The fabric has weight — it is not printed onto the body, it drapes over it.
Variation in surface light across garment where folds catch the key light.
```
 
**Hands look broken:**
```
HANDS ESCALATION (use inpainting): Correct human hand — 5 fingers, natural proportions,
relaxed curl, no extra joints. Skin matching the subject's undertone.
Natural finger length, thumb positioned correctly.
```
 
**Body proportions wrong:**
```
ANATOMY ESCALATION: Correct human proportions — head 1/8 of total body height.
Torso length natural, legs proportional to torso. Eye-level camera, 85mm lens, no distortion.
```
 
**Image looks AI-generated overall:**
```
REALISM ESCALATION: Remove all beauty words. Add: candid, unposed, honest,
no heavy retouching, 35mm film grain. Add flyaway hairs. Add environmental
imperfections. Add under-eye shadows. Reduce symmetry. Add slight motion in hair
or fabric. The image should feel like a documentary photographer's outtake, not a
rendered advertisement.
```
 
**Background looks too clean/staged:**
```
BACKGROUND ESCALATION: Include everyday environmental details — dust particles,
slight surface wear, natural imperfections in surfaces. The environment should feel
lived-in and real, not a pristine CGI render. Add subtle depth cues — distant blurred
elements, natural perspective.
```
 
**Colors overly saturated:**
```
COLOR ESCALATION: Natural color balance. Realistic white balance. No color grading.
No over-saturation. Colors should look like they were captured by a real camera sensor,
not post-processed for social media. Muted, honest color palette.
```
 
---
 
## MODEL SETTINGS & QUALITY GUIDE
 
### Quality Settings
- **Quality**: `high` (never low or medium for hero shots)
- **Thinking mode**: enabled (Plus/Pro) — significantly more realistic skin vs instant mode
- **Resolution**: 2K via API, or maximum available in ChatGPT interface
### API Resolution Reference
 
| Use Case | Quality | Size | Notes |
|---|---|---|---|
| Close-up portrait with skin detail | `high` | `1024x1536` | Maximum fidelity for pores/texture |
| Standard portrait | `medium` | `1024x1536` | Good balance of quality and speed |
| Full-body fashion shot | `high` | `1024x1536` (2:3) | Best for head-to-toe framing |
| 3/4 body shot | `high` | `1024x1536` (3:4 crop) | Mid-thigh to crown |
| Wide cinematic scene | `high` | `2560x1440` | Upper recommended boundary |
| Quick exploration / preview | `low` | `1024x1024` | Surprisingly good for iteration |
 
### Resolution Constraints for gpt-image-2:
- **Max edge:** < 3840px
- **Both edges:** multiples of 16
- **Max aspect ratio:** 3:1
- **Max total pixels:** 8,294,400
- **Min total pixels:** 655,360
- **Recommended aspect ratio**: `2:3` for full-body, `3:4` for 3/4 body shots
---
 
## TROUBLESHOOTING COMMON ISSUES
 
| Problem | Solution |
|---|---|
| **Skin looks plastic/smooth** | Add full skin vocabulary: visible pores, SSS, vellus hair, sebum zones, under-eye shadows. Remove any beauty words. Use SKIN ESCALATION block. |
| **Face doesn't match reference** | Upload tighter face crop. Add: "Use uploaded image as primary reference. Keep facial features IDENTICAL." |
| **Image looks AI-generated** | Remove all beauty/quality words. Add: "candid, unposed, honest, 35mm film grain, flyaway hairs, environmental imperfections." Use REALISM ESCALATION. |
| **Too symmetrical/perfect** | Add: "slightly asymmetrical features, natural facial asymmetry, very slight asymmetry" |
| **Overly saturated colors** | Add: "natural color balance, realistic white balance, no color grading, no over-saturation" |
| **Lighting looks fake** | Replace vague lighting words with physics: specific angle, source type, fill ratio, shadow behavior, color temperature |
| **Eyes look dead/doll-like** | Add full eye vocabulary: iris fibers, natural catchlight, waterline moisture, individual lash strands. Use EYES ESCALATION. |
| **Hands look wrong** | Use Strategy A (describe state), B (give object), C (crop out), or D (reinforce). Use HANDS ESCALATION for inpainting fixes. |
| **Background too clean/staged** | Add environmental imperfections: dust, surface wear, natural textures, distant blurred elements |
| **Expression looks forced** | Replace with: "relaxed, genuine expression — not posing for camera, honest, unposed, caught-mid-thought" |
| **Fabric looks flat or painted on** | Add fabric physics: gravity, fold lines, compression points, weight. Use FABRIC ESCALATION. |
| **Over-sharpened / crunchy detail** | Remove "8K", "ultra HD", "hyper-detailed". Use: "natural sharpness, authentic sensor grain, not over-processed" |
| **Body proportions distorted** | Add proportion anchors: head 1/8 body height, natural limb length, eye-level camera. Use ANATOMY ESCALATION. |
 
---
 
## QUICK REFERENCE: THE COMPLETE REALISM CHECKLIST
 
### Skin
- [ ] Undertone specified (tone + undertone + surface finish)
- [ ] Subsurface scattering at specific zones (nose tip, ear edges)
- [ ] Vellus hair / peach fuzz mentioned
- [ ] Non-repeating organic pore distribution
- [ ] Sebum zones (oily nose, matte cheeks)
- [ ] Gradual highlight roll-off (not sharp specular spike)
- [ ] Under-eye shadows / detail
- [ ] ISO 400 / film grain reference
- [ ] No "beautiful/stunning/flawless/8K/masterpiece" language
- [ ] Natural imperfections (freckles, redness, pigmentation variation)
### Eyes
- [ ] Iris texture — radial fibers, limbal ring
- [ ] Catchlight shape matching light source
- [ ] Waterline moisture
- [ ] Individual lash strands with natural variation
- [ ] Eyes described as alive and present
### Body & Anatomy
- [ ] Contrapposto or specific weight-distribution pose language
- [ ] Hand state explicitly described (or cropped, or holding object)
- [ ] Proportional anchors (head 1/8 of body height)
- [ ] Anatomy negatives in constraints
- [ ] Eye-level camera specified
### Hair
- [ ] Texture and style described
- [ ] Flyaway hairs / loose wisps mentioned
- [ ] Micro-strands catching light
### Garment
- [ ] Fabric type + weave specified
- [ ] Drape behavior described (gravity + fold logic)
- [ ] Fit behavior on this specific body type
- [ ] Natural crease / compression locations named
- [ ] Lighting type matched to fabric surface
- [ ] Fabric physics negatives in constraints
- [ ] "Preserve exact fabric color and drape" included
### Accessories
- [ ] Shoes included (type, color, material, wear detail)
- [ ] At least one complementary accessory (watch, necklace, earrings, bracelet)
- [ ] Metal tone matches garment temperature (cool garment → silver, warm → gold)
- [ ] Accessories are gender-appropriate
- [ ] Material and wear details described (creases, glint, natural drape)
- [ ] Accessories complement but don't compete with garment graphic
- [ ] Accessory negatives in constraints
### Lighting
- [ ] Directional lighting with shadow side specified
- [ ] What light does to skin described
- [ ] What light does to fabric described
- [ ] Color temperature specified (when relevant)
- [ ] No ring light
- [ ] Catchlight shape specified for eyes
- [ ] No direct sunlight on model or garment (sunlight in background only)
### Scene / Background
- [ ] Environmental micro-details included (for outdoor/location shots)
- [ ] Background color/tone complements garment color
- [ ] No unwanted background elements specified in constraints
### Overall
- [ ] Full negative constraints block (standard + skin + eyes + anatomy + fabric)
- [ ] Ethnicity and age specified
- [ ] "Honest and unposed" language present
- [ ] "Photorealistic" keyword included
- [ ] Photography framing language (not "render" or "create")
- [ ] Word "photorealistic" appears in prompt
- [ ] No anti-slop words anywhere in the prompt