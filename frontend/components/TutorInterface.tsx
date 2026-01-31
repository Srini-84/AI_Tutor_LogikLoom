"use client"

import { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface TutorInterfaceProps {
    studentProfile: any
}

const TOPIC_NAMES: Record<string, string> = {
    linear_equations: "Linear Equations",
    expanding_brackets: "Expanding Brackets",
    factorisation: "Factorisation",
    solving_inequalities: "Solving Inequalities",
    simultaneous_equations: "Simultaneous Equations",
}

export function TutorInterface({ studentProfile }: TutorInterfaceProps) {
    const [messages, setMessages] = useState<any[]>([
        {
            role: "tutor",
            content: `Welcome${studentProfile?.preferred_name ? `, ${studentProfile.preferred_name}` : ''}! I'm your AI tutor${studentProfile?.subject ? ` for ${studentProfile.subject.replace('_', ' ')}` : ''}. Let's start with a question to assess your current understanding.`,
        },
    ])
    const [input, setInput] = useState("")
    const [currentMode, setCurrentMode] = useState("lesson")
    const [learningState, setLearningState] = useState<any>({
        currentTopic: studentProfile?.topic || "linear_equations",
        difficulty: "core",
        weakAreas: [],
        mastered: [],
        nextFocus: "Starting learning",
    })
    const messagesEndRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages])

    const sendMessage = async (message?: string, mode?: string) => {
        const studentMessage = message || input.trim()
        const activeMode = mode || currentMode

        if (!studentMessage && activeMode !== "reset") return

        if (studentMessage) {
            setMessages((prev) => [...prev, { role: "student", content: studentMessage }])
            setInput("")
        }

        // Add thinking indicator
        const thinkingId = Date.now()
        setMessages((prev) => [
            ...prev,
            { role: "tutor", content: "Thinking...", id: thinkingId, thinking: true },
        ])

        try {
            const response = await fetch("http://localhost:5000/tutor", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    studentMessage: studentMessage,
                    mode: activeMode,
                }),
                credentials: "include",
            })

            const data = await response.json()

            // Remove thinking indicator
            setMessages((prev) => prev.filter((m) => m.id !== thinkingId))

            if (data.error) {
                setMessages((prev) => [
                    ...prev,
                    { role: "tutor", content: `Error: ${data.error}` },
                ])
            } else {
                setMessages((prev) => [
                    ...prev,
                    {
                        role: "tutor",
                        content: data.assistantMessage,
                        practice: data.practice || [],
                        quiz: data.quiz || [],
                        plan7Days: data.plan7Days || [],
                    },
                ])

                if (data.stateUpdate) {
                    setLearningState(data.stateUpdate)
                }
            }
        } catch (error: any) {
            setMessages((prev) => prev.filter((m) => m.id !== thinkingId))
            setMessages((prev) => [
                ...prev,
                { role: "tutor", content: `Error: ${error.message}` },
            ])
        }
    }

    const setMode = (mode: string) => {
        setCurrentMode(mode)
        if (mode === "reset") {
            sendMessage("", "reset")
        } else {
            sendMessage("", mode)
        }
    }

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr_320px] gap-5 animate-fade-in">
            {/* Left: Student Summary */}
            <Card className="bg-white/95 backdrop-blur-xl border border-sage-200 shadow-lg sticky top-5 h-fit">
                <CardHeader className="bg-sage-50/50 rounded-t-lg border-b border-sage-100 pb-4">
                    <CardTitle className="text-base font-semibold text-sage-800">Your Profile</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Name</div>
                        <div className="font-semibold text-gray-900">
                            {studentProfile?.preferred_name || "Student"}
                        </div>
                    </div>
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Grade/Year</div>
                        <div className="font-semibold text-gray-900">
                            {studentProfile?.grade_year || "-"}
                        </div>
                    </div>
                    {studentProfile?.subject && (
                        <div>
                            <div className="text-xs text-gray-500 mb-1">Subject</div>
                            <div className="font-medium text-sage-700 capitalize">
                                {studentProfile.subject.replace('_', ' ')}
                            </div>
                        </div>
                    )}
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Topic</div>
                        <div className="font-medium text-sage-700">
                            {TOPIC_NAMES[studentProfile?.topic] || studentProfile?.topic}
                        </div>
                        <Badge variant="default" className="mt-2 bg-sage-600 text-white border-0 text-xs">
                            {TOPIC_NAMES[studentProfile?.topic] || studentProfile?.topic}
                        </Badge>
                    </div>
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Confidence</div>
                        <div className="font-semibold text-gray-900">
                            {studentProfile?.confidence || "-"}/5
                        </div>
                    </div>
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Goal</div>
                        <div className="font-semibold text-gray-900">
                            {studentProfile?.goal?.replace("_", " ") || "-"}
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Center: Tutor Interaction */}
            <Card className="bg-white/95 backdrop-blur-xl border border-sage-200 shadow-lg flex flex-col min-h-[600px]">
                <CardContent className="flex-1 flex flex-col p-6">
                    <div className="flex-1 overflow-y-auto mb-5 pr-2 max-h-[500px] space-y-4">
                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={cn(
                                    "p-4 rounded-lg animate-slide-in-message",
                                    msg.role === "student"
                                        ? "bg-sage-600 text-white ml-auto max-w-[80%] shadow-sm"
                                        : "bg-sage-50/50 border-l-2 border-sage-400"
                                )}
                            >
                                <p className="whitespace-pre-wrap">{msg.content}</p>

                                {msg.practice && msg.practice.length > 0 && (
                                    <div className="mt-4 pt-4 border-t border-sage-200">
                                        <div className="font-semibold text-sage-700 mb-3 text-sm uppercase tracking-wide">
                                            Practice Questions
                                        </div>
                                        {msg.practice.map((p: any, i: number) => (
                                            <div
                                                key={i}
                                                className="bg-sage-50 p-3 rounded-md mb-2 border-l-2 border-sage-400"
                                            >
                                                <span className="text-sage-800 text-sm">{p.question}</span>
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {msg.quiz && msg.quiz.length > 0 && (
                                    <div className="mt-4 pt-4 border-t border-sage-200">
                                        <div className="font-semibold text-sage-700 mb-3 text-sm uppercase tracking-wide">
                                            Quiz
                                        </div>
                                        {msg.quiz.map((q: any, i: number) => (
                                            <div
                                                key={i}
                                                className="bg-sage-50 p-3 rounded-md mb-2 border-l-2 border-sage-400"
                                            >
                                                <span className="text-sage-800 text-sm">{q.question}</span>
                                                {q.choices && (
                                                    <div className="mt-2 text-xs text-sage-600 bg-white p-2 rounded border border-sage-200">
                                                        {q.choices.join(", ")}
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}

                                {msg.plan7Days && msg.plan7Days.length > 0 && (
                                    <div className="mt-4 pt-4 border-t border-sage-200">
                                        <div className="font-semibold text-sage-700 mb-3 text-sm uppercase tracking-wide">
                                            7-Day Study Plan
                                        </div>
                                        {msg.plan7Days.map((day: any, i: number) => (
                                            <div
                                                key={i}
                                                className="bg-sage-50 p-3 rounded-md mb-2 border-l-2 border-sage-400"
                                            >
                                                <div className="text-sage-800 text-sm font-medium mb-1">Day {day.day}: {day.task} ({day.minutes} min)</div>
                                                <div className="text-xs text-sage-600 mt-1">
                                                    Practice: {day.practice} | Review: {day.review}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>

                    <div className="flex gap-3">
                        <Textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyPress}
                            placeholder="Type your answer or question here..."
                            rows={2}
                            className="flex-1 border border-sage-200 focus:border-sage-400 focus:ring-sage-300"
                        />
                        <Button onClick={() => sendMessage()} className="px-6 font-medium">
                            Send
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {/* Right: Adaptation Panel */}
            <Card className="bg-white/95 backdrop-blur-xl border border-sage-200 shadow-lg sticky top-5 h-fit">
                <CardHeader className="bg-sage-50/50 rounded-t-lg border-b border-sage-100 pb-4">
                    <CardTitle className="text-base font-semibold text-sage-800">
                        Learning Progress
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Current Topic</div>
                        <div className="font-semibold text-gray-900">
                            {TOPIC_NAMES[learningState.currentTopic] || learningState.currentTopic}
                        </div>
                    </div>
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Difficulty Level</div>
                        <Badge
                            variant={
                                learningState.difficulty === "foundation"
                                    ? "foundation"
                                    : learningState.difficulty === "core"
                                        ? "core"
                                        : "higher"
                            }
                            className="text-sm font-semibold"
                        >
                            {learningState.difficulty?.charAt(0).toUpperCase() +
                                learningState.difficulty?.slice(1) || "-"}
                        </Badge>
                    </div>
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Areas to Work On</div>
                        <div className="flex flex-wrap gap-1">
                            {learningState.weakAreas && learningState.weakAreas.length > 0 ? (
                                learningState.weakAreas.map((area: string, i: number) => (
                                    <Badge key={i} variant="weak" className="text-xs">
                                        {area}
                                    </Badge>
                                ))
                            ) : (
                                <span className="text-gray-400 text-sm">None yet</span>
                            )}
                        </div>
                    </div>
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Mastered</div>
                        <div className="flex flex-wrap gap-1">
                            {learningState.mastered && learningState.mastered.length > 0 ? (
                                learningState.mastered.map((m: string, i: number) => (
                                    <Badge key={i} variant="mastered" className="text-xs">
                                        {m}
                                    </Badge>
                                ))
                            ) : (
                                <span className="text-gray-400 text-sm">None yet</span>
                            )}
                        </div>
                    </div>
                    <div>
                        <div className="text-xs text-gray-500 mb-1">Next Focus</div>
                        <div className="font-semibold text-gray-900">
                            {learningState.nextFocus || "-"}
                        </div>
                    </div>

                    <div className="pt-4 space-y-2 border-t">
                        <Button
                            variant="outline"
                            className="w-full justify-start border border-sage-200 hover:bg-sage-50 hover:border-sage-300 text-sage-700 font-medium text-sm"
                            onClick={() => setMode("lesson")}
                        >
                            Start Lesson
                        </Button>
                        <Button
                            variant="outline"
                            className="w-full justify-start border border-sage-200 hover:bg-sage-50 hover:border-sage-300 text-sage-700 font-medium text-sm"
                            onClick={() => setMode("quiz")}
                        >
                            Quiz Me
                        </Button>
                        <Button
                            variant="outline"
                            className="w-full justify-start border border-sage-200 hover:bg-sage-50 hover:border-sage-300 text-sage-700 font-medium text-sm"
                            onClick={() => setMode("plan")}
                        >
                            Generate 7-Day Plan
                        </Button>
                        <Button
                            variant="outline"
                            className="w-full justify-start border border-sage-200 hover:bg-sage-50 hover:border-sage-300 text-sage-700 font-medium text-sm"
                            onClick={() => setMode("reset")}
                        >
                            Reset
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}