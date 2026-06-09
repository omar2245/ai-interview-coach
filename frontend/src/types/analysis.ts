import type { Component } from "vue";

export type AnalyzeResponse = {
  match_score: number;
  summary: string;
  strengths: string[];
  matched_requirements: string[];
  gaps: string[];
  recommendations: string[];
  interview_focus: string[];
};

export type AnalysisSection = {
  title: string;
  icon: Component;
  items: string[];
};
