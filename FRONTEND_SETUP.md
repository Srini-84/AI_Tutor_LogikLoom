# Frontend Upgrade: Next.js + Tailwind + shadcn/ui

## What Changed

The frontend has been upgraded from vanilla HTML/CSS/JS to:
- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui** components

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main page component
│   └── globals.css         # Tailwind + global styles
├── components/
│   ├── ui/                 # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── textarea.tsx
│   │   ├── select.tsx
│   │   └── badge.tsx
│   ├── StudentSetupWizard.tsx
│   └── TutorInterface.tsx
├── lib/
│   └── utils.ts            # Utility functions
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.js
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

### 3. Run Flask Backend (Separate Terminal)

```bash
# In root directory
python app.py
```

Backend runs on `http://localhost:5000`

## Features Maintained

✅ All original functionality preserved:
- Student Setup wizard (5 steps)
- 3-column tutor layout
- Real-time state updates
- Structured response rendering
- Glassmorphism design
- Smooth animations

## New Features

- **TypeScript** for type safety
- **Component-based** architecture
- **Better state management** with React hooks
- **Reusable UI components** from shadcn/ui
- **Responsive design** with Tailwind utilities

## API Integration

The frontend makes direct API calls to Flask backend:
- `http://localhost:5000/student-setup`
- `http://localhost:5000/tutor`

Uses `credentials: "include"` for session cookies.

## Production Build

```bash
cd frontend
npm run build
npm start
```

## Notes

- Flask backend remains unchanged (serves as API)
- Session management handled by Flask
- CORS may need configuration for production
- Consider environment variables for API URLs

## Migration Notes

The old `templates/index.html` is still in the repo but not used. The new frontend is in the `frontend/` directory and runs as a separate Next.js app.
