import { Idea } from '@/types';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface IdeaCardProps {
  idea: Idea;
  onSelect: (idea: Idea) => void;
}

export default function IdeaCard({ idea, onSelect }: IdeaCardProps) {
  return (
    <Card className="flex flex-col h-full"> {/* Use flex and h-full for consistent height */}
      <CardHeader>
        <CardTitle>{idea.title}</CardTitle>
      </CardHeader>
      <CardContent className="flex-grow"> {/* Allows content to grow */}
        <CardDescription>{idea.summary}</CardDescription>
        {idea.sources && idea.sources.length > 0 && (
          <div className="mt-4">
            <p className="text-sm font-semibold mb-1">Sources/Inspiration:</p>
            <ul className="list-disc list-inside text-sm text-muted-foreground max-h-20 overflow-y-auto"> {/* Add max height and scroll */}
              {idea.sources.map((source, index) => (
                <li key={index} className="truncate"> {/* Truncate long links */}
                  <a href={source} target="_blank" rel="noopener noreferrer" className="hover:underline">
                    {source}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
      <CardFooter className="mt-auto"> {/* Pushes footer to bottom */}
        <Button onClick={() => onSelect(idea)} className="w-full">Select This Idea & Get Plan</Button>
      </CardFooter>
    </Card>
  );
}