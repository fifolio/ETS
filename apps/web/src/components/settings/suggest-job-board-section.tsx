import { SuggestJobBoardForm } from "./suggest-job-board-form";

export function SuggestJobBoardSection() {
    return (
        <section>
            <h2>Suggest a job board</h2>
            <p>Is your favorite job site missing? Tell us about it and we will review it.</p>
            <SuggestJobBoardForm />
        </section>
    );
}