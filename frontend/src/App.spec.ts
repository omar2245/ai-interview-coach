// @vitest-environment happy-dom

import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "@/App.vue";
import AnalysisResultCard from "@/components/AnalysisResultCard.vue";
import type { AnalyzeResponse } from "@/types/analysis";


function mockCapabilities(historyEnabled: boolean) {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ history_enabled: historyEnabled }),
    }),
  );
}


describe("runtime history capability", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("hides history navigation when history is disabled", async () => {
    mockCapabilities(false);
    const wrapper = mount(App);

    await flushPromises();

    expect(
      wrapper.find('nav[aria-label="Application views"]').exists(),
    ).toBe(false);
  });

  it("shows analysis and history navigation when history is enabled", async () => {
    mockCapabilities(true);
    const wrapper = mount(App);

    await flushPromises();

    const navigation = wrapper.get('nav[aria-label="Application views"]');
    expect(navigation.text()).toContain("Analysis");
    expect(navigation.text()).toContain("History");
  });

  it("keeps history navigation hidden when capabilities cannot load", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("offline")));
    const wrapper = mount(App);

    await flushPromises();

    expect(
      wrapper.find('nav[aria-label="Application views"]').exists(),
    ).toBe(false);
  });

  it("submits display metadata and shows that the analysis was saved", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ history_enabled: true }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          match_score: 78,
          summary: "Good fit",
          strengths: [],
          matched_requirements: [],
          gaps: [],
          recommendations: [],
          interview_focus: [],
          history_id: 42,
          history_status: "saved",
        }),
      });
    vi.stubGlobal("fetch", fetchMock);
    const wrapper = mount(App);
    await flushPromises();

    await wrapper.get("#job-title").setValue("Frontend Engineer");
    await wrapper.get("#company-name").setValue("Example Corp");
    await wrapper.get("#job-description").setValue("Build Vue apps");
    const fileInput = wrapper.get<HTMLInputElement>("#resume-file");
    const file = new File(["Vue engineer"], "resume.txt", {
      type: "text/plain",
    });
    Object.defineProperty(fileInput.element, "files", { value: [file] });
    await fileInput.trigger("change");
    await wrapper.get('[aria-label="Analyze job fit"]').trigger("click");
    await flushPromises();

    const submittedData = fetchMock.mock.calls[1][1].body as FormData;
    expect(submittedData.get("job_title")).toBe("Frontend Engineer");
    expect(submittedData.get("company_name")).toBe("Example Corp");
    expect(wrapper.text()).toContain("已儲存至本機分析紀錄");
  });
});

describe("analysis history outcome", () => {
  const baseAnalysis: AnalyzeResponse = {
    match_score: 78,
    summary: "Good fit",
    strengths: [],
    matched_requirements: [],
    gaps: [],
    recommendations: [],
    interview_focus: [],
    history_id: null,
    history_status: "disabled",
  };

  it.each([
    ["disabled", "本機分析紀錄功能未啟用"],
    ["failed", "無法儲存至本機紀錄"],
  ] as const)("shows the %s saving outcome", (historyStatus, copy) => {
    const wrapper = mount(AnalysisResultCard, {
      props: {
        analysis: { ...baseAnalysis, history_status: historyStatus },
        sections: [],
        hasResult: true,
      },
    });

    expect(wrapper.text()).toContain(copy);
  });
});
