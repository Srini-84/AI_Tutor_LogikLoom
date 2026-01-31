# LogikLoom Frontend

Next.js 14 frontend with Tailwind CSS and shadcn/ui components.

## Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   ```

   The frontend will run on `http://localhost:3000`

3. **Make sure Flask backend is running:**
   ```bash
   # In the root directory
   python app.py
   ```

   The backend should run on `http://localhost:5000`

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main page
│   └── globals.css         # Global styles with Tailwind
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
│   └── utils.ts            # Utility functions (cn helper)
└── package.json
```

## Features

- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **shadcn/ui** components
- **Glassmorphism** design maintained
- **3-column layout** for tutor interface
- **Real-time state updates**

## API Integration

The frontend communicates with the Flask backend via:
- `http://localhost:5000/student-setup` - Student setup
- `http://localhost:5000/tutor` - Tutor interactions

The `next.config.js` includes a rewrite rule to proxy API calls, but for development, direct calls are used with `credentials: "include"` for session cookies.

## Building for Production

```bash
npm run build
npm start
```

## Notes

- The Flask backend handles session management
- CORS may need to be configured if running on different ports
- For production, consider using environment variables for API URLs
