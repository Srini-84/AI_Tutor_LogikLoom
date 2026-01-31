import type { Config } from "tailwindcss"

const config = {
    darkMode: ["class"],
    content: [
        './pages/**/*.{ts,tsx}',
        './components/**/*.{ts,tsx}',
        './app/**/*.{ts,tsx}',
        './src/**/*.{ts,tsx}',
    ],
    prefix: "",
    theme: {
        container: {
            center: true,
            padding: "2rem",
            screens: {
                "2xl": "1400px",
            },
        },
        extend: {
            colors: {
                border: "hsl(var(--border))",
                input: "hsl(var(--input))",
                ring: "hsl(var(--ring))",
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                primary: {
                    DEFAULT: "#6b9f6b",
                    dark: "#5a8f5a",
                    light: "#8bb88b",
                    lighter: "#a8cfa8",
                    foreground: "#ffffff",
                },
                secondary: {
                    DEFAULT: "#7eb77e",
                    foreground: "#ffffff",
                },
                sage: {
                    50: "#f6f8f5",
                    100: "#e8ede6",
                    200: "#d1dccd",
                    300: "#b0c4a8",
                    400: "#8ba87c",
                    500: "#6b8d5b",
                    600: "#547145",
                    700: "#455a3a",
                    800: "#3a4a32",
                    900: "#323f2b",
                },
                destructive: {
                    DEFAULT: "hsl(var(--destructive))",
                    foreground: "hsl(var(--destructive-foreground))",
                },
                muted: {
                    DEFAULT: "hsl(var(--muted))",
                    foreground: "hsl(var(--muted-foreground))",
                },
                accent: {
                    DEFAULT: "#ec4899",
                    foreground: "hsl(var(--accent-foreground))",
                },
                popover: {
                    DEFAULT: "hsl(var(--popover))",
                    foreground: "hsl(var(--popover-foreground))",
                },
                card: {
                    DEFAULT: "hsl(var(--card))",
                    foreground: "hsl(var(--card-foreground))",
                },
            },
            borderRadius: {
                lg: "var(--radius)",
                md: "calc(var(--radius) - 2px)",
                sm: "calc(var(--radius) - 4px)",
            },
            keyframes: {
                "accordion-down": {
                    from: { height: "0" },
                    to: { height: "var(--radix-accordion-content-height)" },
                },
                "accordion-up": {
                    from: { height: "var(--radix-accordion-content-height)" },
                    to: { height: "0" },
                },
                "fade-in-down": {
                    from: { opacity: "0", transform: "translateY(-20px)" },
                    to: { opacity: "1", transform: "translateY(0)" },
                },
                "slide-up": {
                    from: { opacity: "0", transform: "translateY(30px)" },
                    to: { opacity: "1", transform: "translateY(0)" },
                },
                "slide-in-message": {
                    from: { opacity: "0", transform: "translateY(10px)" },
                    to: { opacity: "1", transform: "translateY(0)" },
                },
            },
            animation: {
                "accordion-down": "accordion-down 0.2s ease-out",
                "accordion-up": "accordion-up 0.2s ease-out",
                "fade-in-down": "fade-in-down 0.6s ease-out",
                "slide-up": "slide-up 0.6s ease-out",
                "slide-in-message": "slide-in-message 0.3s ease-out",
            },
            backgroundImage: {
                'gradient-primary': 'linear-gradient(135deg, #c1e1c1 0%, #bedfc2 100%)',
                'gradient-soft': 'linear-gradient(135deg, #e8f0e8 0%, #ddeedd 50%, #d4e8d4 100%)',
                'gradient-subtle': 'linear-gradient(135deg, #f0f5f0 0%, #e8efe8 100%)',
            },
        },
    },
    plugins: [require("tailwindcss-animate")],
} satisfies Config

export default config