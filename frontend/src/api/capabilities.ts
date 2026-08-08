export type Capabilities = {
  history_enabled: boolean;
};

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ??
  "http://127.0.0.1:8000";

export async function getCapabilities(): Promise<Capabilities> {
  const response = await fetch(`${apiBaseUrl}/api/capabilities`);

  if (!response.ok) {
    throw new Error("Unable to load application capabilities.");
  }

  return response.json();
}
