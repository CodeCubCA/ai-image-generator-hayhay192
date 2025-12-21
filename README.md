---
title: AI Image Generator
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.32.0
app_file: app.py
pinned: false
---

[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/zrsH8x_3)

# AI Image Generator

A beautiful web application that generates AI images from text descriptions using Streamlit and HuggingFace's FLUX.1-schnell model.

## Features

- **Clean and intuitive user interface** with custom styling
- **Fast image generation** using FLUX.1-schnell model
- **Random Prompt Generator** - Get instant creative inspiration with 1-25 random words from 300+ word dictionary
- **Image History Gallery** - View all generated images in a 3-column grid (up to 10 images)
- **Download Button** - Save generated images with timestamped filenames
- **Negative Prompt Support** - Tell the AI what to avoid in your images
- **Regenerate from History** - Reuse prompts from previously generated images
- **Real-time loading indicators** with progress feedback
- **Comprehensive error handling** with helpful troubleshooting messages
- **Example prompts** for inspiration in sidebar
- **Advanced options panel** with tips and model information
- **Tips for better results** and prompt guidance

## Prerequisites

- Python 3.8 or higher
- HuggingFace account (free)
- HuggingFace API token with Write permissions

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/CodeCubCA/ai-image-generator-hayhay192.git
cd ai-image-generator
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get HuggingFace API Token

1. Go to [HuggingFace Settings - Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name (e.g., "AI Image Generator")
4. Select **"Write"** permissions (or at minimum "Make calls to the serverless Inference API")
   - **IMPORTANT:** Read-only tokens will NOT work!
5. Click "Generate token"
6. Copy the token (you won't be able to see it again)

### 5. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   # Windows
   copy .env.example .env

   # macOS/Linux
   cp .env.example .env
   ```

2. Open `.env` file and replace `your_token_here` with your actual HuggingFace token:
   ```
   HUGGINGFACE_TOKEN=hf_YourActualTokenHere
   ```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

### Basic Usage

1. **Enter a description** of the image you want to generate in the main text area
2. **(Optional)** Add a negative prompt to specify what you DON'T want
3. Click **"🚀 Generate Image"** button
4. Wait 10-30 seconds for the AI to create your image
5. **Download** your image using the download button (timestamped filename)
6. Or right-click on the image to save it manually

### Using the Random Prompt Generator

1. Click **"🎲 Random Prompt"** button to get instant creative inspiration
2. A random prompt (1-25 words) will be generated from 300+ word dictionary
3. Click again for a completely different prompt
4. Edit the prompt if you want to customize it
5. Click **"🚀 Generate Image"** to create the image

### Using Negative Prompts

Negative prompts help you avoid unwanted elements in your images:

1. Enter your main prompt describing what you want
2. In the **"🚫 Negative Prompt"** field, list what you DON'T want
3. Examples:
   - "blurry, low quality, distorted"
   - "dark, gloomy, scary"
   - "text, watermark, signature"
   - "oversaturated, ugly, deformed"

### Using Image History Gallery

The app automatically saves your last 10 generated images:

1. **View History** - Scroll down to see all your generated images in a 3-column grid
2. **View Prompts** - Click "📝 View Prompt" to see the prompts used for each image
3. **Download** - Each image has its own "⬇️ Download" button
4. **Regenerate** - Click "🔄 Regenerate" to reuse a prompt from your history
5. **Clear History** - Click "🗑️ Clear History" to remove all saved images

Features:
- Stores up to 10 images per session
- Shows timestamp for each image
- Displays both positive and negative prompts
- Most recent images appear first

### Example Prompts

- "A futuristic city at night with neon lights, cyberpunk style"
- "A cute corgi wearing a space suit, floating in space, digital art"
- "A peaceful Japanese garden with cherry blossoms, watercolor painting"
- "A majestic dragon flying over mountains at sunset, fantasy art"

### Tips for Better Results

- Be specific and descriptive
- Include style keywords (e.g., "digital art", "photorealistic", "oil painting")
- Mention lighting, colors, and mood
- Describe the composition

## Technology Stack

- **Frontend:** Streamlit
- **AI Model:** FLUX.1-schnell by Black Forest Labs
- **API:** HuggingFace Inference API
- **Libraries:**
  - `streamlit` - Web interface
  - `huggingface_hub` - API client
  - `python-dotenv` - Environment variables
  - `Pillow` - Image processing

## Troubleshooting

### "HuggingFace API token not found"
- Make sure you created the `.env` file
- Check that your token is correctly added to the `.env` file
- Restart the application after adding the token

### "Authentication Error"
- Verify your token is correct
- Ensure your token has **Write** permissions (not read-only)
- Generate a new token if needed

### "Rate Limit Exceeded"
- Free tier has usage limits
- Wait a few minutes before trying again
- Consider upgrading your HuggingFace account

### "Model Loading"
- The model is starting up on the server
- Wait 20-30 seconds and try again
- This is normal for the first request

## Project Structure

```
ai-image-generator/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env               # Your API token (not in git)
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## API Rate Limits

The free tier of HuggingFace Inference API has the following limits:
- Limited number of requests per hour
- May have slower response times during peak usage
- Models may need to "cold start" if not recently used

## License

This project is for educational purposes as part of CodeCub's curriculum.

## Acknowledgments

- Powered by [HuggingFace Inference API](https://huggingface.co/inference-api)
- Uses [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) model
- Built with [Streamlit](https://streamlit.io/)

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all setup steps were completed
3. Check your internet connection
4. Ensure your HuggingFace token is valid

---

Made with ❤️ for CodeCub students
