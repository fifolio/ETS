import { useEffect, useState } from "react";

import { getIndustries } from "@/services/catalog/get-industries";
import { getIndustryJobs } from "@/services/catalog/get-industry-jobs";
import type { Industry, Job, JobCatalogStart } from "@/types/catalog";

export function useJobCatalog(start: JobCatalogStart) {
    const [industries, setIndustries] = useState<Industry[]>([]);
    const [jobs, setJobs] = useState<Job[]>([]);
    const [industryId, setIndustryId] = useState(start.industryId);
    const [jobId, setJobId] = useState(start.jobId);
    const [error, setError] = useState("");

    useEffect(() => {
        getIndustries()
            .then(setIndustries)
            .catch(() => setError("Could not load the industries."));
    }, []);

    useEffect(() => {
        if (!industryId) {
            return;
        }
        let current = true;
        getIndustryJobs(industryId)
            .then((items) => {
                if (current) {
                    setJobs(items);
                }
            })
            .catch(() => {
                if (current) {
                    setError("Could not load the roles.");
                }
            });
        return () => {
            current = false;
        };
    }, [industryId]);

    function selectIndustry(id: string) {
        setIndustryId(id);
        setJobId("");
        setJobs([]);
    }

    return { industries, jobs, industryId, jobId, error, selectIndustry, selectJob: setJobId };
}