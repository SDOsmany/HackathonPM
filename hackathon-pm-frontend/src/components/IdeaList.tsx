import { Idea } from '@/types';
import IdeaCard from './IdeaCard';

interface IdeaListProps {
  ideas: Idea[];
  onSelectIdea: (idea: Idea) => void;
}

export default function IdeaList({ ideas, onSelectIdea }: IdeaListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {ideas.map((idea) => (
        <IdeaCard key={idea.id} idea={idea} onSelect={onSelectIdea} />
      ))}
    </div>
  );
}