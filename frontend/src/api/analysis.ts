import type { AnalyzeResponse } from "@/types/analysis";

type AnalyzeJobFitParams = {
  jobDescription: string;
  jobTitle?: string;
  companyName?: string;
  resumeText?: string;
  resumeFile?: File | null;
  language?: string;
};

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ??
  "http://127.0.0.1:8000";

export async function analyzeJobFit({
  jobDescription,
  jobTitle,
  companyName,
  resumeText,
  resumeFile,
  language = "zh-TW",
}: AnalyzeJobFitParams): Promise<AnalyzeResponse> {
  const formData = new FormData();

  formData.append("job_description", jobDescription);
  formData.append("language", language);

  if (jobTitle) {
    formData.append("job_title", jobTitle);
  }

  if (companyName) {
    formData.append("company_name", companyName);
  }

  if (resumeText) {
    formData.append("resume_text", resumeText);
  }

  if (resumeFile) {
    formData.append("resume_file", resumeFile);
  }

  const response = await fetch(`${apiBaseUrl}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "分析失敗，請稍後再試。");
  }

  return data;
}
