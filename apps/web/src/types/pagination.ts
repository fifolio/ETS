export interface PageInfo {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
}

export interface PagerProps {
    page: number;
    totalPages: number;
    onPage: (page: number) => void;
}