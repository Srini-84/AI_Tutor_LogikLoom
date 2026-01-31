# ⚠️ IMPORTANT: API Key Setup Required

## How to Get Your API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

## 🔴 CRITICAL: Enable Billing (Free Tier)

**Without billing enabled, you'll get quota errors!**

Even with a $0 budget, enabling billing unlocks much higher free tier limits:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (or create one)
3. Go to **Billing** → **Link a billing account**
4. Create a billing account (you can set a $0 budget limit)
5. This unlocks the free tier quotas:
   - **15 RPM** (requests per minute)
   - **1,500 RPD** (requests per day)
   - **1M tokens per minute**

**Note:** You won't be charged if you stay within free tier limits!

## Set Up Your API Key

1. Create `.env` file in project root:
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

2. Replace `your-api-key-here` with your actual API key

## Free Tier Limits (After Billing Setup)
- ✅ 15 requests per minute
- ✅ 1,500 requests per day  
- ✅ 1M tokens per minute
- ✅ Perfect for hackathons!

## After Updating
Restart your Flask server for changes to take effect.
