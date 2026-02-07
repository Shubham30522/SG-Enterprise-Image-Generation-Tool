---
name: new-product-setup
description: Standard procedure for adding a new product to the Gemini Auto Tool. Handles folder creation and prompt file initialization.
---

# New Product Setup Skill

This skill guides the agent through the process of adding a new product to the Gemini Auto Tool system. Use this skill whenever the user asks to "add a new product" or "create a new product folder".

## Workflow

1.  **Identify Product Name**
    - Confirm the name of the new product (e.g., "T-Shirt for Women").

2.  **Create Directories & Color Setup**
    - Create a new directory at: `Prompts/<Product Name>` (relative to the project root).
    - **Determine Color Folder**:
      - Check if the user specified a color in the request (e.g., "Add Grey Wide Leg Jeans").
      - If **NO** color is specified, you must **STOP AND ASK** the user: _"Please specify the color name for the input folder (e.g., 'Grey', 'Navy', '01-Black')."_
    - Once confirmed, create the nested directory: `input_images/<Product Name>/<Color Name>` (relative to the project root).
    - **Move Raw Image**: Place the provided raw image into `input_images/<Product Name>/<Color Name>/Front.jpg` (or `Front.png` depending on source). Rename it to **Front** regardless of the original filename.

3.  **Smart Angle Selection (Logical Analysis)**
    - **Goal**: You must define exactly 5 prompt files to showcase the product comprehensively.
    - **If Reference Images ARE Provided**:
      - Create 5 prompt files corresponding _exactly_ to the angles/layouts in the provided reference images.
      - Name them intuitively (e.g., `prompt_folded.txt`, `prompt_texture.txt`).
    - **If NO Reference Images are Provided**:
      - **THINK**: What is this product? What are the 5 essential views?
      - **Deduce** the best angles. DO NOT blindly copy "Neck" or "Side" if it doesn't fit.
      - **Common Patterns**:
        - **Tops/Shirts**: `master_prompt.txt` (Front), `neck.txt`, `sleeve.txt`, `side_fold.txt`, `texture.txt`.
        - **Bottoms/Jeans**: `master_prompt.txt` (Front Waist-to-Hem), `waistband.txt` (Buttons/Fly), `back.txt` (Pockets/Yoke), `hem.txt` or `folded_stack.txt`, `texture.txt`.
        - **Dresses**: `master_prompt.txt` (Full Body), `neck.txt`, `hem_drape.txt`, `back.txt`, `texture.txt`.
    - **Constraint**: You MUST create exactly 5 text files in total (including `master_prompt.txt`).

4.  **Populate Content & Fidelity**
    - **Step 4a (Adaptation)**: Populate these files using templates from `configure_prompts.py` as a base, but **REWRITE** the content to match your selected angles.
      - Example: If you chose `waistband.txt`, do NOT paste the "Neck" template blindly. Rewrite it: _"Close-up detail of the waistband, button, and zipper fly."_
    - **Step 4b (Style Consistency)**:
      - Inherit the _Style_ (Lighting, Background) from existing products (e.g., "T-Shirt for Women") if no reference is given.
    - **Step 4c (Critical: Product Preservation)**:
      - **Mandatory**: In every single prompt file, ADD this rule:
        > "STRICT REQUIREMENT: The generated product must match the Input Image (Raw Product) with 100% fidelity. DO NOT alter the color, fabric texture, or stitching details."
    - **Step 4d (Complementary Styling & Consistency)**:
      - **Mandatory**: Always describe a complete, stylish outfit.
        - If Product is **Bottoms**: explicitly describe a matching top (e.g., "Pair with a crisp white t-shirt tucked in") and shoes (e.g., "White minimalist sneakers").
        - If Product is **Top**: explicitly describe matching bottoms (e.g., "Pair with light wash denim jeans").
      - **Consistency Rule**: You MUST copy this exact styling description into ALL 5 prompt files to ensure the model looks the same in every shot.
        - Example: If `master_prompt.txt` says "White sneakers", `side.txt` and `back.txt` MUST also say "White sneakers".

    - **Step 4e (Model Consistency)**:
      - **Mandatory**: You MUST strictly instruct the AI to keep the model's physical characteristics consistent across all images.
        - **Skin Tone & Features**: Must match Image 1 (Generated Front).
        - **Nails**: Explicitly forbid nail polish (`no nail polish` in negative prompt) unless it's a specific feature.
        - **Clothing/Shoes**: If visible in detail shots, they must match the main outfit.

5.  **Verification**
    - Verify that the folder exists.
    - Verify that all 5 files exist and are not empty.
