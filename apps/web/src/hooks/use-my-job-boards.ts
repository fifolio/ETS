import { useEffect, useState } from "react";

import { getJobBoards } from "@/services/job-boards/get-job-boards";
import { getMyJobBoards } from "@/services/job-boards/get-my-job-boards";
import type { JobBoard, MyJobBoards } from "@/types/job-boards";

export function useMyJobBoards() {
    const [all, setAll] = useState<JobBoard[] | null>(null);
    const [mine, setMine] = useState<MyJobBoards | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        getJobBoards()
            .then(setAll)
            .catch(() => setError("Could not load the job boards."));
        getMyJobBoards()
            .then(setMine)
            .catch(() => setError("Could not load your job boards."));
    }, []);

    return { all, mine, error };
}