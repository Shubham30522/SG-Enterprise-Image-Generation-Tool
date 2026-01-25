import os
import shutil

base_input = r"d:\E-Commerce\Gemini_Auto_Tool\Gemini_Auto_Tool - SG Enterprise\input_images"
base_prompt = r"d:\E-Commerce\Gemini_Auto_Tool\Gemini_Auto_Tool - SG Enterprise\Prompts"

# Source
src_input = os.path.join(base_input, "dress")
src_prompt = os.path.join(base_prompt, "dress")

# Dest
dst_input = os.path.join(base_input, "Dress - Flat lay")
dst_prompt = os.path.join(base_prompt, "Dress - Flat lay")

def copy_and_setup():
    # 1. Input Images
    if os.path.exists(dst_input):
        shutil.rmtree(dst_input)
    shutil.copytree(src_input, dst_input)
    print(f"Copied input images to {dst_input}")

    # 2. Prompts
    if os.path.exists(dst_prompt):
        shutil.rmtree(dst_prompt)
    shutil.copytree(src_prompt, dst_prompt)
    print(f"Copied prompts to {dst_prompt}")

    # 3. Rename Reference
    ref_src = os.path.join(dst_input, "Dress_Ref_Image.jpeg")
    ref_dst = os.path.join(dst_input, "REFERENCE IMAGE.png")
    
    if os.path.exists(ref_src):
        os.rename(ref_src, ref_dst)
        print(f"Renamed {ref_src} to {ref_dst}")
    else:
        print(f"Warning: {ref_src} not found. Check if file exists.")

if __name__ == "__main__":
    copy_and_setup()
