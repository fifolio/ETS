export interface JobBoard {
    id: string;
    name: string;
    url: string;
    plan: string;
    plan_name: string;
}

export interface MyJobBoards {
    boards: JobBoard[];
    plan: string;
}

export interface JobBoardRowProps {
    board: JobBoard;
    available: boolean;
}

export interface JobBoardListProps {
    boards: JobBoard[];
    availableIds: string[];
}