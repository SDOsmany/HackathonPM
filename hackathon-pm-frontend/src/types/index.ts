
export interface Idea {
    id: string; // Or some unique identifier
    title: string;
    summary: string;
    sources: string[]; // Array of URLs
    // Potentially add more details that the backend provides
  }
  
  export interface ExecutionPlan {
    rawText: string; // Maybe store the raw LLM output too
  }