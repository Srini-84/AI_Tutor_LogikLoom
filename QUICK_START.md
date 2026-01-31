# 🚀 Quick Start Guide - LogikLoom

## Prerequisites

- **Python 3.13+** installed
- **Node.js 18+** and **npm** installed
- **Google account** (for Gemini API key)

---

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key

---

## Step 2: Set Up Backend (Flask)

### 2.1 Navigate to Project Root
```bash
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom
```

### 2.2 Create Virtual Environment (if not already created)
```bash
python3 -m venv venv
```

### 2.3 Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 2.4 Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2.5 Create `.env` File
```bash
touch .env
```

### 2.6 Add Your API Key to `.env`
Open `.env` file and add:
```
GEMINI_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with the API key you copied in Step 1.

---

## Step 3: Set Up Frontend (Next.js)

### 3.1 Navigate to Frontend Directory
```bash
cd frontend
```

### 3.2 Install Node Dependencies
```bash
npm install
```

This may take a few minutes the first time.

---

## Step 4: Start the Application

You need **TWO terminal windows** - one for backend, one for frontend.

### Terminal 1: Start Flask Backend

```bash
# Make sure you're in the project root
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom

# Activate virtual environment
source venv/bin/activate

# Start Flask server
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

✅ **Backend is running on port 5000**

### Terminal 2: Start Next.js Frontend

```bash
# Navigate to frontend directory
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom/frontend

# Start Next.js dev server
npm run dev
```

You should see:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
```

✅ **Frontend is running on port 3000**

---

## Step 5: Open the App

1. Open your browser
2. Go to: **http://localhost:3000**
3. You should see the LogikLoom logo and setup wizard!

---

## Quick Commands Reference

### Backend (Terminal 1):
```bash
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom
source venv/bin/activate
python app.py
```

### Frontend (Terminal 2):
```bash
cd /Users/ifedayoagboola/Desktop/myProjects/AI_Tutor_LogikLoom/frontend
npm run dev
```

---

## Troubleshooting

### ❌ "GEMINI_API_KEY not found"
- Make sure you created `.env` file in the project root
- Check that `.env` contains: `GEMINI_API_KEY=your-key`
- Restart Flask server after creating `.env`

### ❌ "Module not found" errors
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### ❌ "Port 5000 already in use"
- Another process is using port 5000
- Kill it: `lsof -ti:5000 | xargs kill`
- Or change port in `app.py`

### ❌ "Port 3000 already in use"
- Another process is using port 3000
- Kill it: `lsof -ti:3000 | xargs kill`
- Or Next.js will automatically use 3001

### ❌ Frontend can't connect to backend
- Make sure Flask is running on port 5000
- Check browser console for CORS errors
- Verify both servers are running

### ❌ "npm: command not found"
- Install Node.js from [nodejs.org](https://nodejs.org/)

### ❌ Logo not showing
- Check that `logo.jpeg` exists in `frontend/public/assets/`
- Restart Next.js server
- Clear browser cache

---

## Verification Checklist

Before starting, verify:
- [ ] Python 3.13+ installed: `python3 --version`
- [ ] Node.js installed: `node --version`
- [ ] Virtual environment created and activated
- [ ] All Python packages installed: `pip list | grep flask`
- [ ] All Node packages installed: `cd frontend && npm list`
- [ ] `.env` file created with `GEMINI_API_KEY`
- [ ] Logo file exists: `frontend/public/assets/logo.jpeg`

---

## Stopping the App

- **Backend**: Press `Ctrl+C` in Terminal 1
- **Frontend**: Press `Ctrl+C` in Terminal 2

---

## What You'll See

1. **Student Setup Wizard** - Complete the 6-step setup:
   - Step 1: Name & Grade
   - Step 2: Subject Selection (Mathematics available)
   - Step 3: Algebra Topic
   - Step 4: Confidence Level
   - Step 5: Goal
   - Step 6: Learning Style

2. **Tutor Interface** - 3-column layout with:
   - Left: Your profile
   - Center: Chat with tutor
   - Right: Adaptation panel + buttons

---

## Next Steps After Starting

1. Complete the **Student Setup** wizard
2. Select **Mathematics** as subject
3. Choose an **Algebra topic**
4. Start learning with the tutor!

Happy learning! 🎓
