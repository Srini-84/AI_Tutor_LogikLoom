"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface StudentSetupWizardProps {
  onComplete: (profile: any) => void
}

const SUBJECTS = [
  { id: "mathematics", label: "Mathematics", available: true, description: "Algebra, Geometry, Calculus" },
  { id: "science", label: "Science", available: false, description: "Physics, Chemistry, Biology" },
  { id: "english", label: "English", available: false, description: "Literature, Writing, Grammar" },
  { id: "history", label: "History", available: false, description: "World History, Social Studies" },
  { id: "computer_science", label: "Computer Science", available: false, description: "Programming, Algorithms" },
]

const ALGEBRA_TOPICS = [
  { id: "linear_equations", label: "Linear Equations" },
  { id: "expanding_brackets", label: "Expanding Brackets" },
  { id: "factorisation", label: "Factorisation" },
  { id: "solving_inequalities", label: "Solving Inequalities" },
  { id: "simultaneous_equations", label: "Simultaneous Equations" },
]

const GOALS = [
  { id: "exam_prep", label: "Exam Prep" },
  { id: "homework", label: "Homework Help" },
  { id: "catch_up", label: "Catch Up" },
  { id: "learn_ahead", label: "Learn Ahead" },
]

const LEARNING_STYLES = [
  { id: "examples_first", label: "Examples First" },
  { id: "practice_first", label: "Practice First" },
  { id: "explain_slow", label: "Explain Slowly" },
  { id: "go_fast", label: "Go Fast" },
]

export function StudentSetupWizard({ onComplete }: StudentSetupWizardProps) {
  const [currentStep, setCurrentStep] = useState(1)
  const [formData, setFormData] = useState({
    preferred_name: "",
    grade_year: "",
    subject: "",
    topic: "",
    confidence: "",
    goal: "",
    learning_style: "",
  })

  const totalSteps = 6

  const updateFormData = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const nextStep = () => {
    if (validateStep(currentStep)) {
      if (currentStep < totalSteps) {
        setCurrentStep(currentStep + 1)
      }
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
    }
  }

  const validateStep = (step: number): boolean => {
    switch (step) {
      case 1:
        if (!formData.grade_year) {
          alert("Please select your year")
          return false
        }
        return true
      case 2:
        if (!formData.subject) {
          alert("Please select a subject")
          return false
        }
        return true
      case 3:
        if (!formData.topic) {
          alert("Please select a topic")
          return false
        }
        return true
      case 4:
        if (!formData.confidence) {
          alert("Please select your confidence level")
          return false
        }
        return true
      case 5:
        if (!formData.goal) {
          alert("Please select your goal")
          return false
        }
        return true
      case 6:
        if (!formData.learning_style) {
          alert("Please select your learning style")
          return false
        }
        return true
      default:
        return true
    }
  }

  const handleComplete = async () => {
    if (!validateStep(6)) return

    try {
      const response = await fetch("http://localhost:5001/student-setup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          preferred_name: formData.preferred_name,
          grade_year: formData.grade_year,
          subject: formData.subject,
          topic: formData.topic,
          confidence: parseInt(formData.confidence),
          goal: formData.goal,
          learning_style: formData.learning_style,
        }),
        credentials: "include",
      })

      const data = await response.json()

      if (data.success) {
        onComplete(data.student_profile)
      } else {
        alert("Error: " + (data.error || "Something went wrong"))
      }
    } catch (error: any) {
      alert("Error: " + error.message)
    }
  }

  return (
    <Card className="max-w-2xl mx-auto bg-white/95 backdrop-blur-xl border border-sage-200 shadow-xl animate-slide-up">
      <CardContent className="p-10">
        {/* Progress Bar */}
        <div className="flex gap-2 mb-10">
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={i}
              className={cn(
                "flex-1 h-1.5 rounded-full transition-all duration-300",
                i + 1 < currentStep
                  ? "bg-sage-500"
                  : i + 1 === currentStep
                  ? "bg-sage-600"
                  : "bg-sage-100"
              )}
            />
          ))}
        </div>

        {/* Step 1: Name & Grade */}
        {currentStep === 1 && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <div className="w-10 h-10 rounded-full bg-sage-600 text-white flex items-center justify-center text-base font-semibold mb-4 shadow-sm">
                1
              </div>
              <h2 className="text-2xl font-semibold text-sage-800 mb-2 tracking-tight">
                Let's get started
              </h2>
              <p className="text-sage-600 text-base leading-relaxed">Tell us a bit about yourself so we can personalize your learning experience</p>
            </div>
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">
                  Preferred Name (Optional)
                </label>
                <Input
                  placeholder="What should we call you?"
                  value={formData.preferred_name}
                  onChange={(e) => updateFormData("preferred_name", e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">
                  Grade/Year *
                </label>
                <select
                  value={formData.grade_year}
                  onChange={(e) => updateFormData("grade_year", e.target.value)}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Select your year...</option>
                  {[7, 8, 9, 10, 11, 12, 13].map((year) => (
                    <option key={year} value={`Year ${year}`}>
                      Year {year}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Subject */}
        {currentStep === 2 && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <div className="w-10 h-10 rounded-full bg-sage-600 text-white flex items-center justify-center text-base font-semibold mb-4 shadow-sm">
                2
              </div>
              <h2 className="text-2xl font-semibold text-sage-800 mb-2 tracking-tight">
                Which subject?
              </h2>
              <p className="text-sage-600 text-base leading-relaxed">
                Select the subject you'd like to learn
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {SUBJECTS.map((subject) => (
                <div
                  key={subject.id}
                  onClick={() => {
                    if (subject.available) {
                      updateFormData("subject", subject.id)
                    }
                  }}
                  className={cn(
                    "p-4 rounded-lg border-2 transition-all cursor-pointer",
                    formData.subject === subject.id
                      ? "border-sage-600 bg-sage-50 shadow-sm"
                      : subject.available
                      ? "border-sage-200 hover:border-sage-400 hover:bg-sage-50 bg-white"
                      : "border-sage-100 bg-sage-50/50 opacity-60 cursor-not-allowed"
                  )}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-sage-800">{subject.label}</h3>
                    {subject.available ? (
                      <Badge variant="default" className="bg-sage-600 text-white text-xs">
                        Available
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="border-sage-300 text-sage-500 text-xs">
                        Coming Soon
                      </Badge>
                    )}
                  </div>
                  <p className="text-sm text-sage-600">{subject.description}</p>
                </div>
              ))}
            </div>
            {formData.subject === "mathematics" && (
              <div className="mt-4 p-3 bg-sage-50 border border-sage-200 rounded-lg">
                <p className="text-sm text-sage-700">
                  <strong>Note:</strong> Currently, only Algebra topics are fully functional. Other subjects coming soon!
                </p>
              </div>
            )}
          </div>
        )}

        {/* Step 3: Topic (only for Mathematics/Algebra) */}
        {currentStep === 3 && formData.subject === "mathematics" && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <div className="w-10 h-10 rounded-full bg-sage-600 text-white flex items-center justify-center text-base font-semibold mb-4 shadow-sm">
                3
              </div>
              <h2 className="text-2xl font-semibold text-sage-800 mb-2 tracking-tight">
                Which Algebra topic?
              </h2>
              <p className="text-sage-600 text-base leading-relaxed">
                Choose the topic you'd like to focus on
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              {ALGEBRA_TOPICS.map((topic) => (
                <Badge
                  key={topic.id}
                  variant={formData.topic === topic.id ? "default" : "outline"}
                  className={cn(
                    "cursor-pointer px-5 py-2.5 text-sm font-medium transition-all rounded-lg",
                    formData.topic === topic.id
                      ? "bg-sage-600 text-white shadow-sm"
                      : "bg-white border border-sage-200 hover:border-sage-400 hover:bg-sage-50 text-sage-700"
                  )}
                  onClick={() => updateFormData("topic", topic.id)}
                >
                  {topic.label}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Step 4: Confidence */}
        {currentStep === 4 && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <div className="w-10 h-10 rounded-full bg-sage-600 text-white flex items-center justify-center text-base font-semibold mb-4 shadow-sm">
                4
              </div>
              <h2 className="text-2xl font-semibold text-sage-800 mb-2 tracking-tight">
                How confident are you?
              </h2>
              <p className="text-sage-600 text-base leading-relaxed">
                Rate your confidence level (1 = not confident, 5 = very confident)
              </p>
            </div>
            <div className="flex gap-3">
              {[1, 2, 3, 4, 5].map((num) => (
                <button
                  key={num}
                  onClick={() => updateFormData("confidence", num.toString())}
                  className={cn(
                    "flex-1 py-4 rounded-lg border transition-all font-medium",
                    formData.confidence === num.toString()
                      ? "bg-sage-600 text-white border-sage-600 shadow-sm"
                      : "bg-white border-sage-200 hover:border-sage-400 hover:bg-sage-50 text-sage-700"
                  )}
                >
                  {num}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Step 5: Goal */}
        {currentStep === 5 && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <div className="w-10 h-10 rounded-full bg-sage-600 text-white flex items-center justify-center text-base font-semibold mb-4 shadow-sm">
                5
              </div>
              <h2 className="text-2xl font-semibold text-sage-800 mb-2 tracking-tight">
                What's your goal?
              </h2>
              <p className="text-sage-600 text-base leading-relaxed">What are you hoping to achieve?</p>
            </div>
            <div className="flex flex-wrap gap-3">
              {GOALS.map((goal) => (
                <Badge
                  key={goal.id}
                  variant={formData.goal === goal.id ? "default" : "outline"}
                  className={cn(
                    "cursor-pointer px-5 py-2.5 text-sm font-medium transition-all rounded-lg",
                    formData.goal === goal.id
                      ? "bg-sage-600 text-white shadow-sm"
                      : "bg-white border border-sage-200 hover:border-sage-400 hover:bg-sage-50 text-sage-700"
                  )}
                  onClick={() => updateFormData("goal", goal.id)}
                >
                  {goal.label}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Step 6: Learning Style */}
        {currentStep === 6 && (
          <div className="animate-fade-in">
            <div className="mb-8">
              <div className="w-10 h-10 rounded-full bg-sage-600 text-white flex items-center justify-center text-base font-semibold mb-4 shadow-sm">
                6
              </div>
              <h2 className="text-2xl font-semibold text-sage-800 mb-2 tracking-tight">
                How do you like to learn?
              </h2>
              <p className="text-sage-600 text-base leading-relaxed">
                This helps us adapt our teaching style to you
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              {LEARNING_STYLES.map((style) => (
                <Badge
                  key={style.id}
                  variant={
                    formData.learning_style === style.id ? "default" : "outline"
                  }
                  className={cn(
                    "cursor-pointer px-5 py-2.5 text-sm font-medium transition-all rounded-lg",
                    formData.learning_style === style.id
                      ? "bg-sage-600 text-white shadow-sm"
                      : "bg-white border border-sage-200 hover:border-sage-400 hover:bg-sage-50 text-sage-700"
                  )}
                  onClick={() => updateFormData("learning_style", style.id)}
                >
                  {style.label}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex gap-3 mt-8">
          {currentStep > 1 && (
            <Button variant="secondary" onClick={prevStep} className="flex-1">
              ← Back
            </Button>
          )}
          {currentStep < totalSteps ? (
            <Button onClick={nextStep} className="flex-1 py-3 font-medium">
              Continue →
            </Button>
          ) : (
            <Button onClick={handleComplete} className="flex-1 py-3 font-medium">
              Start Learning
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}