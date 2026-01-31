# 🚀 Quick Start Guide

## Step-by-Step Instructions

### 1. Set Up Gemini API Key

**Get your API key:**
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in and create a new API key
3. Copy the key

**Set it in your terminal:**
```bash
export GEMINI_API_KEY='your-api-key-here'
```

### 2. Start Flask Backend (Terminal 1)

```bash
# Navigate to project root
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom

# Activate virtual environment (if you created one)
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

✅ Backend running on `http://localhost:5000`

### 3. Start Next.js Frontend (Terminal 2)

```bash
# Navigate to frontend directory
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom/frontend

# Install dependencies (first time only)
npm install

# Start Next.js dev server
npm run dev
```

✅ Frontend running on `http://localhost:3000`

### 4. Open in Browser

Open: **http://localhost:3000**

## What You'll See

1. **Student Setup Wizard** - Complete the 5-step setup
2. **Tutor Interface** - 3-column layout with:
   - Left: Your profile
   - Center: Chat with tutor
   - Right: Adaptation panel + buttons

## Troubleshooting

### Backend won't start?
- Check if port 5000 is already in use
- Verify `GEMINI_API_KEY` is set: `echo $GEMINI_API_KEY`
- Make sure virtual environment is activated

### Frontend won't start?
- Make sure you're in the `frontend/` directory
- Run `npm install` if you haven't already
- Check if port 3000 is available

### API errors?
- Make sure both servers are running
- Check browser console for CORS errors
- Verify Flask is on port 5000 and Next.js on 3000

## Quick Commands Reference

```bash
# Backend
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom
source venv/bin/activate  # If using venv
python app.py

# Frontend (new terminal)
cd frontend
npm run dev
```

That's it! 🎉