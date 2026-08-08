import type { Component } from "vue";

export type AnalyzeResponse = {
  match_score: number;
  summary: string;
  strengths: string[];
  matched_requirements: string[];
  gaps: string[];
  recommendations: string[];
  interview_focus: string[];
  history_id: number | null;
  history_status: "saved" | "disabled" | "failed";
};

export type AnalysisSection = {
  title: string;
  icon: Component;
  items: string[];
};
