import type { JobBoard } from "@/types/job-boards";

/** "Available" when the user's plan includes the board, otherwise the plan that does. */
export function describeBoardAccess(board: JobBoard, available: boolean): string {
    return available ? "Available" : board.plan_name;
}