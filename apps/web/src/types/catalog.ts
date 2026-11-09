export interface Industry {
    id: string;
    name: string;
}

export interface Job {
    id: string;
    name: string;
    hourly_rate_usd: number;
}

export interface JobCatalogStart {
    industryId: string;
    jobId: string;
}

export interface JobPickerProps {
    industries: Industry[];
    jobs: Job[];
    industryId: string;
    jobId: string;
    onIndustryChange: (industryId: string) => void;
    onJobChange: (jobId: string) => void;
}