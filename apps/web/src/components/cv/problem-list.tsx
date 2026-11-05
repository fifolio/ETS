import type { ProblemListProps } from "@/types/cv/cv";

export function ProblemList({ problems }: ProblemListProps) {
    if (problems.length === 0) {
        return null;
    }
    return (
        <ul role="alert">
            {problems.map((problem) => (
                <li key={problem}>{problem}</li>
            ))}
        </ul>
    );
}