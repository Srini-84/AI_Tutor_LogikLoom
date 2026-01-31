# ⚠️ IMPORTANT: API Key Setup Required

## Current Status
Your current Gemini API key has been reported as **leaked** and is not working.

## How to Get a New API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the new API key
5. Replace the key in `app.py` line 11:

```python
GEMINI_API_KEY = 'YOUR_NEW_API_KEY_HERE'
```

## Free Tier Limits
- Google Gemini API has a **free tier** with generous limits
- No credit card required for basic usage
- Perfect for hackathons!

## After Updating
Restart your Flask server for changes to take effect.
