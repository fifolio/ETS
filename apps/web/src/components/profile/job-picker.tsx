import type { JobPickerProps } from "@/types/catalog";

export function JobPicker({
    industries,
    jobs,
    industryId,
    jobId,
    onIndustryChange,
    onJobChange,
}: JobPickerProps) {
    return (
        <>
            <label>
                Industry{" "}
                <select
                    value={industryId}
                    onChange={(event) => onIndustryChange(event.target.value)}
                    required
                >
                    <option value="">Choose...</option>
                    {industries.map((industry) => (
                        <option key={industry.id} value={industry.id}>
                            {industry.name}
                        </option>
                    ))}
                </select>
            </label>
            <br />
            <label>
                Role{" "}
                <select
                    value={jobId}
                    onChange={(event) => onJobChange(event.target.value)}
                    required
                    disabled={!industryId}
                >
                    <option value="">{industryId ? "Choose..." : "Choose an industry first"}</option>
                    {jobs.map((job) => (
                        <option key={job.id} value={job.id}>
                            {job.name}
                        </option>
                    ))}
                </select>
            </label>
        </>
    );
}