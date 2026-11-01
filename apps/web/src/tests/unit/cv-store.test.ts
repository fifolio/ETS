import { beforeEach, describe, expect, it, vi } from "vitest";

const services = vi.hoisted(() => ({
    getCvInfo: vi.fn(),
    uploadCv: vi.fn(),
    deleteCv: vi.fn(),
}));

vi.mock("@/services/cv/get-cv-info", () => ({ getCvInfo: services.getCvInfo }));
vi.mock("@/services/cv/upload-cv", () => ({ uploadCv: services.uploadCv }));
vi.mock("@/services/cv/delete-cv", () => ({ deleteCv: services.deleteCv }));

import { useCvStore } from "@/stores/cv/cv-store";

const info = { file_name: "cv.pdf", characters: 1200 };

beforeEach(() => {
    vi.resetAllMocks();
    useCvStore.setState({ info: null, loaded: false });
});

describe("cv store", () => {
    it("stores the CV info and marks it loaded", async () => {
        services.getCvInfo.mockResolvedValue(info);

        await useCvStore.getState().load();

        expect(useCvStore.getState()).toMatchObject({ info, loaded: true });
    });

    it("replaces the info after an upload", async () => {
        services.uploadCv.mockResolvedValue(info);

        await useCvStore.getState().upload(new File(["x"], "cv.pdf"));

        expect(useCvStore.getState().info).toEqual(info);
    });

    it("clears the info after the CV is deleted", async () => {
        useCvStore.setState({ info, loaded: true });
        services.deleteCv.mockResolvedValue(undefined);

        await useCvStore.getState().remove();

        expect(useCvStore.getState().info).toBeNull();
    });

    it("forgets everything on clear", () => {
        useCvStore.setState({ info, loaded: true });

        useCvStore.getState().clear();

        expect(useCvStore.getState()).toMatchObject({ info: null, loaded: false });
    });
});