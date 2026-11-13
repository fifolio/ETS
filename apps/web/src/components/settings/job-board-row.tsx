import { describeBoardAccess } from "@/lib/job-boards/describe-board-access";
import type { JobBoardRowProps } from "@/types/job-boards";

export function JobBoardRow({ board, available }: JobBoardRowProps) {
    return (
        <li>
            {board.name} <small>({board.url})</small>: {describeBoardAccess(board, available)}
        </li>
    );
}