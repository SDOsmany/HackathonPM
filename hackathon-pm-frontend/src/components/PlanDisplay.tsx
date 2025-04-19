import { ExecutionPlan } from '@/types';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription} from "@/components/ui/card"; 
import { ScrollArea } from "@/components/ui/scroll-area";
import { CopyIcon } from 'lucide-react';

interface PlanDisplayProps {
  ideaTitle: string;
  plan: ExecutionPlan;
  onRefine: () => void;
  onStartOver: () => void;
}

export default function PlanDisplay({ ideaTitle, plan, onRefine, onStartOver }: PlanDisplayProps) {
  const copyPlanToClipboard = () => {
    const planText = `Idea: ${ideaTitle}\n\n${plan.rawText}`;
    
    navigator.clipboard.writeText(planText)
      .then(() => {
        alert('Plan copied to clipboard!');
      })
      .catch(err => {
        console.error('Failed to copy plan: ', err);
        alert('Failed to copy plan.');
      });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center text-2xl">{ideaTitle}</CardTitle>
        <CardDescription className="text-center">Your Hackathon Execution Plan</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[60vh] px-4 pb-4 -mr-4">
          <div className="mt-6">
            <p className="text-muted-foreground whitespace-pre-wrap font-mono text-sm bg-gray-100 dark:bg-gray-800 p-4 rounded-md">
              {plan.rawText}
            </p>
          </div>
        </ScrollArea>

        <div className="flex flex-col md:flex-row gap-4 mt-6">
          <Button onClick={onRefine} variant="outline" className="flex-grow">
            Refine Plan
          </Button>
          <Button onClick={copyPlanToClipboard} variant="secondary" className="flex-grow">
            <CopyIcon className="mr-2 h-4 w-4" /> Copy Plan
          </Button>
          <Button onClick={onStartOver} variant="ghost" className="flex-grow">
            Start Over
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}