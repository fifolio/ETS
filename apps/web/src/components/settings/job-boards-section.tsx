"use client";

import { useMyJobBoards } from "@/hooks/use-my-job-boards";

import { JobBoardList } from "./job-board-list";

export function JobBoardsSection() {
    const { all, mine, error } = useMyJobBoards();
    const availableIds = mine?.boards.map((board) => board.id) ?? [];
    const hasLocked = all !== null && mine !== null && all.length > availableIds.length;

    return (
        <section>
            <h2>Job boards</h2>
            <p>
                The extension only reads job pages from the boards included in your plan. Boards marked
                with a plan name come with that plan.
            </p>
            {error && <p role="alert">{error}</p>}
            {!all && !mine && !error && <p>Loading...</p>}
            {all && all.length === 0 && <p>No job boards are available yet.</p>}
            {all && mine && all.length > 0 && <JobBoardList boards={all} availableIds={availableIds} />}
            {hasLocked && <p>Upgrade your plan to unlock more job boards.</p>}
        </section>
    );
}