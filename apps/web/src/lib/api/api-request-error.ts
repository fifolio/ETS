export class ApiRequestError extends Error {
    readonly status: number;
    readonly problems: string[];

    constructor(status: number, message: string, problems: string[] = []) {
        super(message);
        this.name = "ApiRequestError";
        this.status = status;
        this.problems = problems;
    }
}