import type { JobBoardListProps } from "@/types/job-boards";

import { JobBoardRow } from "./job-board-row";

export function JobBoardList({ boards, availableIds }: JobBoardListProps) {
    return (
        <ul>
            {boards.map((board) => (
                <JobBoardRow key={board.id} board={board} available={availableIds.includes(board.id)} />
            ))}
        </ul>
    );
}