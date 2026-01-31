# 💳 Billing Setup Guide (Required for Free Tier)

## Why Billing is Needed

Even though Gemini API has a free tier, **you must enable billing** to access it. Without billing:
- ❌ Quota limits are **0 requests**
- ❌ You'll get "quota exceeded" errors
- ❌ The API won't work

**Good news:** You can set a **$0 budget** and won't be charged if you stay within free limits!

---

## Step-by-Step Setup

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Sign in with your Google account

### Step 2: Create or Select a Project
1. Click the project dropdown at the top
2. Click **"New Project"**
3. Name it (e.g., "LogikLoom")
4. Click **"Create"**

### Step 3: Enable Billing
1. In the left menu, go to **"Billing"**
2. Click **"Link a billing account"**
3. Click **"Create billing account"**
4. Fill in:
   - **Account name**: Your name or project name
   - **Country**: Your country
   - **Currency**: Your currency
5. Click **"Submit and enable billing"**

### Step 4: Set Budget Alert (Optional but Recommended)
1. Go to **"Budgets & alerts"**
2. Click **"Create budget"**
3. Set budget amount to **$0** (or small amount like $5)
4. Set alert at 100% (you'll get notified if you exceed)
5. This prevents unexpected charges

### Step 5: Enable Gemini API
1. Go to **"APIs & Services"** → **"Library"**
2. Search for **"Generative Language API"**
3. Click on it and click **"Enable"**

---

## Free Tier Limits (After Billing Setup)

Once billing is enabled, you get:
- ✅ **15 requests per minute**
- ✅ **1,500 requests per day**
- ✅ **1M tokens per minute**
- ✅ **No cost** if you stay within limits

---

## Verify It's Working

After setup, try your app again. The quota errors should be gone!

---

## Troubleshooting

### Still getting quota errors?
- Wait 2-3 minutes after enabling billing
- Make sure Generative Language API is enabled
- Check your API key is from the correct project

### Don't want to use billing?
Unfortunately, Google requires billing to be enabled even for free tier. However:
- You can set a $0 budget
- You won't be charged for free tier usage
- You can disable billing anytime

---

## Need Help?

- [Google Cloud Billing Docs](https://cloud.google.com/billing/docs)
- [Gemini API Quotas](https://ai.google.dev/gemini-api/docs/rate-limits)
