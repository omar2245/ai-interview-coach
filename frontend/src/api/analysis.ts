import type { AnalyzeResponse } from "@/types/analysis";

type AnalyzeJobFitParams = {
  jobDescription: string;
  resumeText: string;
  language?: string;
};

export async function analyzeJobFit({
  jobDescription,
  resumeText,
  language = "zh-TW",
}: AnalyzeJobFitParams): Promise<AnalyzeResponse> {
  const response = await fetch("http://127.0.0.1:8000/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      job_description: jobDescription,
      resume_text: resumeText,
      language,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "分析失敗，請稍後再試。");
  }

  return data;
}
