import { useState } from 'react'; // Need useState for button loading state
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"; // Use Card for structure

interface InputFormProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean; // Passed down from parent
}

export default function InputForm({ value, onChange, onSubmit, isLoading }: InputFormProps) {
  const [buttonLoading, setButtonLoading] = useState(false); // Manage local button loading

  const handleSubmit = async () => {
      if (!value.trim()) return; // Prevent submit on empty input
      setButtonLoading(true);
      await onSubmit(); // Call parent handler
      // Note: Parent handles setting phase and turning off its main isLoading
      // We can turn off local loading here, or let the parent manage it fully.
      // Letting parent manage main phase and loading is cleaner.
      setButtonLoading(false); // Assuming parent state change causes re-render
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">What's your hackathon idea or theme?</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }} className="grid w-full items-center gap-4">
          <div className="flex flex-col space-y-2">
            <Label htmlFor="idea">Describe your initial concept:</Label>
            <Textarea
              id="idea"
              placeholder="e.g., A web app using AI to help teams brainstorm ideas..."
              value={value}
              onChange={(e) => onChange(e.target.value)}
              rows={5}
              className="resize-none"
            />
          </div>
          <Button
            type="submit"
            className="w-full"
            disabled={!value.trim() || buttonLoading}
          >
            {buttonLoading ? 'Generating...' : 'Generate Ideas'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}