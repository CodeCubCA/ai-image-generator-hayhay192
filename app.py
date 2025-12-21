import streamlit as st
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO
from datetime import datetime
import random

# Load environment variables
load_dotenv()

# Configuration
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"

# Word dictionary for random prompt generation
NOUNS = [
    "cat", "dog", "dragon", "robot", "wizard", "knight", "princess", "astronaut", "pirate", "ninja",
    "unicorn", "phoenix", "griffin", "mermaid", "vampire", "werewolf", "fairy", "giant", "dwarf", "elf",
    "city", "forest", "mountain", "ocean", "desert", "castle", "temple", "tower", "bridge", "cave",
    "garden", "library", "museum", "market", "tavern", "spaceship", "island", "waterfall", "volcano", "lake",
    "sunset", "sunrise", "storm", "rainbow", "aurora", "galaxy", "nebula", "planet", "star", "moon",
    "flower", "tree", "mushroom", "crystal", "gem", "sword", "shield", "crown", "book", "potion",
    "car", "train", "airplane", "boat", "bicycle", "motorcycle", "airship", "submarine", "rocket", "helicopter",
    "tiger", "lion", "eagle", "wolf", "bear", "fox", "owl", "deer", "horse", "elephant"
]

ADJECTIVES = [
    "magical", "ancient", "futuristic", "mystical", "enchanted", "cursed", "blessed", "haunted", "sacred", "forbidden",
    "glowing", "shimmering", "sparkling", "blazing", "frozen", "ethereal", "celestial", "cosmic", "divine", "infernal",
    "massive", "tiny", "giant", "colossal", "miniature", "enormous", "microscopic", "towering", "grand", "majestic",
    "dark", "bright", "colorful", "vibrant", "radiant", "luminous", "shadowy", "gleaming", "dazzling", "brilliant",
    "peaceful", "chaotic", "serene", "wild", "calm", "stormy", "turbulent", "tranquil", "violent", "gentle",
    "cyberpunk", "steampunk", "gothic", "baroque", "minimalist", "surreal", "abstract", "realistic", "whimsical", "dramatic",
    "mechanical", "organic", "crystalline", "metallic", "wooden", "stone", "glass", "golden", "silver", "bronze",
    "floating", "flying", "swimming", "dancing", "sleeping", "running", "standing", "sitting", "jumping", "soaring"
]

ACTIONS = [
    "riding", "flying", "swimming", "dancing", "fighting", "meditating", "reading", "writing", "painting", "crafting",
    "exploring", "discovering", "guarding", "protecting", "attacking", "defending", "casting", "summoning", "brewing", "forging",
    "climbing", "jumping", "running", "walking", "floating", "gliding", "diving", "surfing", "skating", "racing",
    "singing", "playing", "performing", "celebrating", "mourning", "praying", "chanting", "whispering", "shouting", "laughing",
    "building", "destroying", "creating", "transforming", "evolving", "growing", "shrinking", "appearing", "vanishing", "emerging"
]

SETTINGS = [
    "in a cyberpunk city", "in a magical forest", "on a distant planet", "under the ocean", "in the clouds",
    "in a medieval castle", "in a futuristic laboratory", "in an ancient temple", "on a mountain peak", "in a desert oasis",
    "in a haunted mansion", "in a crystalline cave", "in a neon-lit street", "in a starship", "in a treehouse",
    "in a library", "in a garden", "in a marketplace", "in a battlefield", "in a throne room",
    "during sunset", "during sunrise", "at midnight", "at dawn", "at dusk",
    "during a storm", "under a rainbow", "beneath the stars", "under the aurora", "in moonlight"
]

STYLES = [
    "digital art", "oil painting", "watercolor", "pencil sketch", "ink drawing", "pixel art", "3D render",
    "photorealistic", "anime style", "cartoon style", "comic book style", "fantasy art", "concept art",
    "impressionist", "surrealist", "abstract", "minimalist", "baroque", "gothic", "art nouveau",
    "cinematic", "dramatic lighting", "soft lighting", "neon lighting", "golden hour", "studio lighting",
    "highly detailed", "atmospheric", "ethereal", "dreamlike", "vibrant colors", "muted colors", "monochrome"
]

def generate_random_prompt():
    """Generate a random prompt with 1-25 words"""
    # Random length between 1 and 25 words
    length = random.randint(1, 25)

    # Pool of all words
    all_words = NOUNS + ADJECTIVES + ACTIONS + SETTINGS + STYLES

    # Generate random words
    words = random.sample(all_words, min(length, len(all_words)))

    # Join words into a prompt
    return " ".join(words)

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .sub-header {
        text-align: center;
        color: #4ECDC4;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .stButton>button {
        width: 100%;
        background-color: #4ECDC4;
        color: white;
        font-size: 1.2em;
        padding: 0.5em;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45B7AA;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-header">🎨 AI Image Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform your imagination into stunning images using AI</p>', unsafe_allow_html=True)

# Check if API token is configured
if not HUGGINGFACE_TOKEN:
    st.error("⚠️ HuggingFace API token not found!")
    st.info("""
    **Setup Instructions:**
    1. Go to https://huggingface.co/settings/tokens
    2. Create a new token with 'Write' permissions
    3. Create a `.env` file in the project directory
    4. Add your token: `HUGGINGFACE_TOKEN=your_token_here`
    5. Restart the application
    """)
    st.stop()

# Initialize the InferenceClient
@st.cache_resource
def get_client():
    return InferenceClient(token=HUGGINGFACE_TOKEN)

client = get_client()

# Main interface
st.markdown("---")

# Initialize session state for prompt if not exists
if 'prompt_text' not in st.session_state:
    st.session_state.prompt_text = ""

# Initialize session state for image history
if 'image_history' not in st.session_state:
    st.session_state.image_history = []

# Prompt input
prompt = st.text_area(
    "✍️ Enter your image description:",
    value=st.session_state.prompt_text,
    placeholder="Example: A serene landscape with mountains at sunset, digital art style",
    height=100,
    help="Describe the image you want to generate. Be specific for better results!",
    key="prompt_input"
)

# Negative prompt input
negative_prompt = st.text_input(
    "🚫 Negative Prompt (Optional):",
    placeholder="What you DON'T want in the image...",
    help="Examples: 'blurry, low quality, distorted' or 'dark, gloomy, scary' or 'text, watermark, signature'"
)

# Advanced options (collapsible)
with st.expander("⚙️ Advanced Options"):
    st.info(f"**Current Model:** {MODEL_NAME}")
    st.caption("This model is optimized for fast, high-quality image generation.")

    st.markdown("**💡 Negative Prompt Tips:**")
    st.caption("Tell the AI what to avoid in your image. Common examples:")
    st.code("• blurry, low quality, distorted\n• dark, gloomy, scary\n• text, watermark, signature\n• oversaturated, ugly, deformed", language=None)

# Buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    random_button = st.button("🎲 Random Prompt")
with col2:
    generate_button = st.button("🚀 Generate Image")

# Handle random prompt button
if random_button:
    st.session_state.prompt_text = generate_random_prompt()
    st.rerun()

st.markdown("---")

# Image generation
if generate_button:
    if not prompt.strip():
        st.warning("⚠️ Please enter a description for your image!")
    else:
        try:
            # Show loading state
            with st.spinner("🎨 Creating your masterpiece... This may take 10-30 seconds..."):
                # Generate image using InferenceClient
                # Include negative prompt if provided
                if negative_prompt and negative_prompt.strip():
                    try:
                        image = client.text_to_image(
                            prompt=prompt,
                            negative_prompt=negative_prompt,
                            model=MODEL_NAME
                        )
                    except TypeError:
                        # If negative_prompt parameter is not supported, fallback to basic generation
                        st.info("ℹ️ Note: Negative prompt feature may not be fully supported by this model.")
                        image = client.text_to_image(
                            prompt=prompt,
                            model=MODEL_NAME
                        )
                else:
                    image = client.text_to_image(
                        prompt=prompt,
                        model=MODEL_NAME
                    )

                # Display the generated image
                st.success("✅ Image generated successfully!")
                st.image(image, caption=f"Generated: {prompt}", use_container_width=True)

                # Save to image history
                current_time = datetime.now()
                image_data = {
                    'image': image,
                    'prompt': prompt,
                    'negative_prompt': negative_prompt if negative_prompt else None,
                    'timestamp': current_time
                }
                st.session_state.image_history.insert(0, image_data)

                # Limit to 10 images to prevent memory issues
                if len(st.session_state.image_history) > 10:
                    st.session_state.image_history = st.session_state.image_history[:10]

                # Download button
                st.markdown("---")

                # Convert PIL Image to bytes for download
                buf = BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()

                # Create timestamp for filename
                timestamp = current_time.strftime("%Y%m%d_%H%M%S")
                filename = f"ai_generated_{timestamp}.png"

                # Download button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="⬇️ Download Image",
                        data=byte_im,
                        file_name=filename,
                        mime="image/png"
                    )

                st.info("💡 **Tip:** You can also right-click on the image to save it!")

        except Exception as e:
            error_message = str(e)
            st.error("❌ Failed to generate image")

            # Provide helpful error messages
            if "401" in error_message or "unauthorized" in error_message.lower():
                st.error("""
                **Authentication Error:** Your API token is invalid or expired.

                Please check:
                1. Your token is correct in the `.env` file
                2. Your token has 'Write' permissions (read-only tokens won't work)
                3. Generate a new token at https://huggingface.co/settings/tokens
                """)
            elif "429" in error_message or "rate limit" in error_message.lower():
                st.error("""
                **Rate Limit Exceeded:** You've made too many requests.

                Solutions:
                - Wait a few minutes before trying again
                - Free tier has usage limits
                - Consider upgrading your HuggingFace account
                """)
            elif "503" in error_message or "loading" in error_message.lower():
                st.warning("""
                **Model Loading:** The model is currently loading on the server.

                Please wait 20-30 seconds and try again.
                """)
            else:
                st.error(f"**Error Details:** {error_message}")
                st.info("Try refreshing the page or checking your internet connection.")

# Image History Gallery
st.markdown("---")
st.markdown("## 🖼️ Image History")

if len(st.session_state.image_history) > 0:
    # Header with count and clear button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"**{len(st.session_state.image_history)} image(s) in history** (max 10)")
    with col2:
        if st.button("🗑️ Clear History"):
            st.session_state.image_history = []
            st.rerun()

    st.markdown("---")

    # Display images in grid (3 columns)
    for idx in range(0, len(st.session_state.image_history), 3):
        cols = st.columns(3)

        for col_idx, col in enumerate(cols):
            img_idx = idx + col_idx
            if img_idx < len(st.session_state.image_history):
                img_data = st.session_state.image_history[img_idx]

                with col:
                    # Display image
                    st.image(img_data['image'], use_container_width=True)

                    # Show timestamp
                    time_str = img_data['timestamp'].strftime("%m/%d %I:%M %p")
                    st.caption(f"🕒 {time_str}")

                    # Show prompt in expander
                    with st.expander("📝 View Prompt"):
                        st.write(f"**Prompt:** {img_data['prompt']}")
                        if img_data.get('negative_prompt'):
                            st.write(f"**Negative:** {img_data['negative_prompt']}")

                    # Download button for this image
                    buf = BytesIO()
                    img_data['image'].save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    timestamp_str = img_data['timestamp'].strftime("%Y%m%d_%H%M%S")

                    st.download_button(
                        label="⬇️ Download",
                        data=byte_im,
                        file_name=f"ai_generated_{timestamp_str}.png",
                        mime="image/png",
                        key=f"download_{img_idx}"
                    )

                    # Regenerate button
                    if st.button("🔄 Regenerate", key=f"regen_{img_idx}"):
                        st.session_state.prompt_text = img_data['prompt']
                        st.rerun()

                    st.markdown("---")
else:
    st.info("📭 No images generated yet. Create your first image above!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1em;'>
        <p>Powered by <strong>HuggingFace FLUX.1-schnell</strong> model</p>
        <p>Made with ❤️ using Streamlit</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This application uses the FLUX.1-schnell model from Black Forest Labs
    to generate high-quality images from text descriptions.
    """)

    st.header("💡 Tips for Better Results")
    st.write("""
    - Be specific and descriptive
    - Include style keywords (e.g., "digital art", "photorealistic", "oil painting")
    - Mention lighting, colors, and mood
    - Describe the composition
    """)

    st.header("📝 Example Prompts")
    examples = [
        "A futuristic city at night with neon lights, cyberpunk style",
        "A cute corgi wearing a space suit, floating in space, digital art",
        "A peaceful Japanese garden with cherry blossoms, watercolor painting",
        "A majestic dragon flying over mountains at sunset, fantasy art",
        "An astronaut riding a horse on Mars, photorealistic"
    ]

    for example in examples:
        if st.button(example, key=example):
            st.session_state.example_prompt = example
            st.rerun()

    # Handle example prompt selection
    if 'example_prompt' in st.session_state:
        prompt = st.session_state.example_prompt
        del st.session_state.example_prompt
