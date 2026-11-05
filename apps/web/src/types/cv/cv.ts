export interface CvInfo {
    file_name: string | null;
    characters: number;
}

export interface ProblemListProps {
    problems: string[];
}

export interface CvUploadFormProps {
    hasCv: boolean;
}