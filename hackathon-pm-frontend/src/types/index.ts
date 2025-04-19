
export interface Idea {
    id: string; // Or some unique identifier
    title: string;
    summary: string;
    sources: string[]; // Array of URLs
    // Potentially add more details that the backend provides
  }
  
  export interface ExecutionPlan {
    // Structure this based on your desired plan output
    problemStatement: string;
    coreFeatures: string[]; // Or a more complex structure
    techStack: string[];
    timeline: { milestone: string; tasks: string[] }[];
    teamRoles: string[];
    // Add other relevant sections...
    rawText?: string; // Maybe store the raw LLM output too
  }