'use client'; // Use Client Component

import { useState } from 'react';
import { Idea, ExecutionPlan } from '@/types'; // Adjust path if needed
import { Button } from '@/components/ui/button';
import { API_ENDPOINTS } from '@/config/api';

// Import your components
import InputForm from '@/components/InputForm';
import IdeaList from '@/components/IdeaList';
// import PlanDisplay from '@/components/PlanDisplay';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
// Define the phases
type AppPhase = 'input' | 'generating_ideas' | 'show_ideas' | 'generating_plan' | 'show_plan' | 'error';

export default function HomePage() {
  const [phase, setPhase] = useState<AppPhase>('input');
  const [inputValue, setInputValue] = useState('');
  const [generatedIdeas, setGeneratedIdeas] = useState<Idea[]>([]);
  const [selectedIdea, setSelectedIdea] = useState<Idea | null>(null);
  const [executionPlan, setExecutionPlan] = useState<ExecutionPlan | null>(null);
  const [error, setError] = useState<string | null>(null);

  // --- API Call Functions ---

  const generateIdeas = async (ideaInput: string) => {
    setPhase('generating_ideas');
    setError(null); // Clear previous errors
    try {
      // Replace with your actual backend API endpoint
      const res = await fetch(API_ENDPOINTS.RAG, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: ideaInput }),
      });
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || 'Failed to generate ideas.');
      }

      const data = await res.json();
      console.log("data:", data)
      // Assuming backend returns { ideas: Idea[] }
      console.log("data:", data)
      if (data.ideas && data.ideas.length > 0) {
        setGeneratedIdeas(data.ideas);
        setPhase('show_ideas');
      } else {
         throw new Error('Backend did not return any ideas.');
      }

    } catch (err: unknown) {
      console.error("Error generating ideas:", err);
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      setPhase('error'); // Or back to input with error
    }
  };

  const generatePlan = async (idea: Idea) => {
    setPhase('generating_plan');
    setSelectedIdea(idea); // Set selected idea immediately
    setError(null); // Clear previous errors
    try {
      const res = await fetch(API_ENDPOINTS.GENERATE_PLAN, { // Assuming a Next.js API route proxy or direct backend call
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea: idea }), // Send the selected idea object
      });
      console.log("req: ", JSON.stringify({ idea: idea }))
      if (!res.ok) {
         const errorData = await res.json();
         throw new Error(errorData.message || 'Failed to generate plan.');
      }

      const data = await res.json();
      // Assuming backend returns ExecutionPlan object
      console.log("plan data:", data)
      setExecutionPlan(data); // Assuming the plan is in data.plan
      setPhase('show_plan');

    } catch (err: unknown) {
      console.error("Error generating plan:", err);
      const errorMessage = err instanceof Error ? err.message : 'Error generating plan';
      setError(errorMessage);
      setPhase('error'); // Or back to idea selection with error
    }
  };

    // --- Handlers ---

  const handleInputChange = (value: string) => {
    setInputValue(value);
  };

  const handleInputSubmit = () => {
    if (inputValue.trim()) {
      generateIdeas(inputValue);
    }
    // Optionally show an error if input is empty
  };

  const handleIdeaSelect = (idea: Idea) => {
    generatePlan(idea);
  };

  const handleRefinePlan = () => {
      // TODO: Implement refinement logic.
      // This would likely involve another API call, maybe sending
      // the current plan text + user instructions for refinement.
      console.log("Refine plan clicked for idea:", selectedIdea?.title);
      alert("Refine functionality not yet implemented!");
      // setPhase('refining_plan'); // Example phase
      // refinePlanAPI(selectedPlan, refineInstructions);
  };

  const handleStartOver = () => {
      setPhase('input');
      setInputValue('');
      setGeneratedIdeas([]);
      setSelectedIdea(null);
      setExecutionPlan(null);
      setError(null);
  };


  // --- Render Logic ---

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <h1 className="text-4xl font-bold text-center mb-8">HackathonPM</h1>
      <p className="text-center text-lg text-muted-foreground mb-8">
        Turn your hackathon theme into a plan.
      </p>

      {/* Render based on phase */}

      {phase === 'input' && (
        <InputForm
          value={inputValue}
          onChange={handleInputChange}
          onSubmit={handleInputSubmit}
          isLoading={false} // No loading here, button handles its own
        />
      )}

      {(phase === 'generating_ideas' || phase === 'generating_plan') && (
        <div className="text-center p-8">
            {/* Use shadcn/ui skeleton or simple text */}
            <div className="h-8 w-8 mx-auto mb-4 rounded-full bg-primary animate-pulse"></div>
            <p className="text-lg">{phase === 'generating_ideas' ? 'Generating ideas...' : 'Crafting the plan...'}</p>
            {/* Optional: Show the input/selected idea */}
             {inputValue && phase === 'generating_ideas' && <p className="text-sm text-muted-foreground mt-2">Based on: &apos;{inputValue}&apos;</p>}
             {selectedIdea && phase === 'generating_plan' && <p className="text-sm text-muted-foreground mt-2">For idea: &apos;{selectedIdea.title}&apos;</p>}

        </div>
      )}

      {phase === 'show_ideas' && (
        <div>
            <h2 className="text-2xl font-semibold mb-4 text-center">Choose an Idea</h2>
            <IdeaList ideas={generatedIdeas} onSelectIdea={handleIdeaSelect} />
            <div className="text-center mt-8">
                 <Button variant="outline" onClick={handleStartOver}>Start Over</Button>
            </div>
        </div>
      )}

      {phase === 'show_plan' && executionPlan && selectedIdea && (
        // <PlanDisplay
        //   ideaTitle={selectedIdea.title}
        //   plan={executionPlan}
        //   onRefine={handleRefinePlan}
        //   onStartOver={handleStartOver}
        // />
        <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-center text-2xl">{selectedIdea.title}</CardTitle>
          <CardDescription className="text-center">Your Hackathon Execution Plan</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mt-6 max-h-[60vh] overflow-y-auto">
            <pre className="whitespace-pre-wrap font-mono text-sm bg-gray-100 dark:bg-gray-800 p-4 rounded-md">
              {executionPlan.rawText}
            </pre>
          </div>
          <div className="flex flex-col md:flex-row gap-4 mt-6">
            <Button onClick={handleStartOver} variant="ghost" className="flex-grow">
              Start Over
            </Button>
          </div>
        </CardContent>
      </Card>
      )}

      {phase === 'error' && (
        <div className="text-center text-red-500 p-8 border border-red-500 rounded-md">
            <h2 className="text-2xl font-semibold mb-4">An Error Occurred</h2>
            <p>{error || 'Something went wrong. Please try again.'}</p>
            <Button onClick={handleStartOver} className="mt-4">Start Over</Button>
        </div>
      )}

        {/* Optional: Keep the footer visible */}
         <footer className="text-center text-sm text-muted-foreground mt-12">
             Built for Microsoft Hackathon 2025!
         </footer>

    </div>
  );
}