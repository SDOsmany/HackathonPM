import { ExecutionPlan } from '@/types';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription} from "@/components/ui/card"; 
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area"; // Use ScrollArea for content
import { CopyIcon } from 'lucide-react'; // Need to install lucide-react: npm install lucide-react

interface PlanDisplayProps {
  ideaTitle: string;
  plan: ExecutionPlan;
  onRefine: () => void;
  onStartOver: () => void;
}

export default function PlanDisplay({ ideaTitle, plan, onRefine, onStartOver }: PlanDisplayProps) {

  // Helper function to render structured plan data
  const renderPlanSection = (title: string, content: string[] | string | { milestone: string; tasks: string[] }[]) => {
      if (!content || (Array.isArray(content) && content.length === 0) || (typeof content === 'string' && !content.trim())) {
          return null; // Don't render empty sections
      }

      return (
          <div className="mb-6">
              <h3 className="text-xl font-semibold mb-3">{title}</h3>
              {Array.isArray(content) ? (
                  // Handle arrays (like features, roles)
                  <ul>
                      {content.map((item, index) => (
                          <li key={index} className="ml-4 list-disc text-muted-foreground">{typeof item === 'string' ? item : item.milestone}</li>
                      ))}
                  </ul>
              ) : typeof content === 'string' ? (
                  // Handle raw text
                   <p className="text-muted-foreground whitespace-pre-wrap">{content}</p> // Use whitespace-pre-wrap for basic formatting
              ) : (
                 // Handle structured objects like timeline
                 <ul>
                     {(content as { milestone: string; tasks: string[] }[]).map((phase, index) => (
                        <li key={index} className="mb-2">
                            <h4 className="font-medium">{phase.milestone}</h4>
                            <ul className="ml-4">
                                {phase.tasks.map((task, taskIndex) => (
                                     <li key={taskIndex} className="list-disc text-muted-foreground">{task}</li>
                                ))}
                            </ul>
                        </li>
                     ))}
                 </ul>
              )}
          </div>
      );
  };

   const copyPlanToClipboard = () => {
        const planText = `Idea: ${ideaTitle}\n\n${plan.rawText || JSON.stringify(plan, null, 2)}`; // Copy raw text or JSON

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
        <ScrollArea className="h-[60vh] px-4 pb-4 -mr-4"> {/* Limit height and enable scrolling */}
          {/* Render the structured plan sections */}
          {renderPlanSection("Problem Statement / User Story", plan.problemStatement)}
          {plan.problemStatement && <Separator className="my-4" />} {/* Add separators between sections */}

          {renderPlanSection("Core Features (MVP Scope)", plan.coreFeatures)}
           {plan.coreFeatures && plan.coreFeatures.length > 0 && <Separator className="my-4" />}

          {renderPlanSection("Potential Tech Stack", plan.techStack)}
           {plan.techStack && plan.techStack.length > 0 && <Separator className="my-4" />}

          {renderPlanSection("Timeline / Milestones", plan.timeline)}
           {plan.timeline && plan.timeline.length > 0 && <Separator className="my-4" />}


          {renderPlanSection("Team Roles & Task Suggestions", plan.teamRoles)}
           {plan.teamRoles && plan.teamRoles.length > 0 && <Separator className="my-4" />}

          {/* Add more sections as defined in your ExecutionPlan type */}

           {/* Fallback/Raw Text */}
            {plan.rawText && !plan.problemStatement && ( // Only show raw if structured failed or isn't available
                <div className="mt-6">
                     <h3 className="text-xl font-semibold mb-3">Raw Plan Output</h3>
                     <p className="text-muted-foreground whitespace-pre-wrap font-mono text-sm bg-gray-100 dark:bg-gray-800 p-4 rounded-md">{plan.rawText}</p>
                </div>
            )}


        </ScrollArea>

        <div className="flex flex-col md:flex-row gap-4 mt-6">
          <Button onClick={onRefine} variant="outline" className="flex-grow">
             Refine Plan {/* Or "Add Details", "Modify" */}
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