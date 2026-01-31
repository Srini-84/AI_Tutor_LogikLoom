"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { StudentSetupWizard } from "@/components/StudentSetupWizard"
import { TutorInterface } from "@/components/TutorInterface"

export default function Home() {
    const [setupComplete, setSetupComplete] = useState(false)
    const [studentProfile, setStudentProfile] = useState<any>(null)

    const handleSetupComplete = (profile: any) => {
        setStudentProfile(profile)
        setSetupComplete(true)
    }

    return (
        <div className="min-h-screen p-5 relative">
            <div className="max-w-[1400px] mx-auto relative z-10">
                <div className="text-center mb-10 animate-fade-in-down">
                    <h1 className="text-5xl font-bold mb-3 text-sage-700 tracking-tight">
                        LogikLoom
                    </h1>
                    <p className="text-sage-600 text-lg font-medium">Your Personal AI Tutor</p>
                    <p className="text-sage-500 text-sm mt-2 font-normal">Adaptive learning across multiple subjects</p>
                </div>

                {!setupComplete ? (
                    <StudentSetupWizard onComplete={handleSetupComplete} />
                ) : (
                    <TutorInterface studentProfile={studentProfile} />
                )}
            </div>
        </div>
    )
}