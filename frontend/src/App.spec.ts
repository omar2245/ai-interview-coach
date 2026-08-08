// @vitest-environment happy-dom

import { flushPromises, mount } from "@vue/test-utils";
import { afterEach, describe, expect, it, vi } from "vitest";

import App from "@/App.vue";


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
});
