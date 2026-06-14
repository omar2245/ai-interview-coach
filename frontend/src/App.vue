<script setup lang="ts">
import {
  AlertCircle,
  CheckCircle2,
  ClipboardList,
  Lightbulb,
  Sparkles,
  Target,
} from "@lucide/vue";
import { computed, ref } from "vue";

import { analyzeJobFit } from "@/api/analysis";
import AnalyzeActionBar from "@/components/AnalyzeActionBar.vue";
import AnalysisResultCard from "@/components/AnalysisResultCard.vue";
import JobDescriptionCard from "@/components/JobDescriptionCard.vue";
import ResumeInputCard from "@/components/ResumeInputCard.vue";
import { Badge } from "@/components/ui/badge";
import type { AnalysisSection, AnalyzeResponse } from "@/types/analysis";

const appVersion = "v0.1.0";
const resumeInputMode = ref<"file" | "text">("file");
const jobDescription = ref("");
const resumeText = ref("");
const selectedFileName = ref("");
const selectedResumeFile = ref<File | null>(null);
const isAnalyzing = ref(false);
const analysisResult = ref<AnalyzeResponse | null>(null);
const errorMessage = ref("");

const displaySections = computed<AnalysisSection[]>(() => [
  {
    title: "履歷強項",
    icon: CheckCircle2,
    items: analysisResult.value?.strengths ?? [],
  },
  {
    title: "命中需求",
    icon: Target,
    items: analysisResult.value?.matched_requirements ?? [],
  },
  {
    title: "可能缺口",
    icon: AlertCircle,
    items: analysisResult.value?.gaps ?? [],
  },
  {
    title: "建議補強",
    icon: Lightbulb,
    items: analysisResult.value?.recommendations ?? [],
  },
  {
    title: "面試準備重點",
    icon: ClipboardList,
    items: analysisResult.value?.interview_focus ?? [],
  },
]);

function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0] ?? null;

  selectedResumeFile.value = file;
  selectedFileName.value = file?.name ?? "";
}

function handleResumeInputModeChange(value: "file" | "text") {
  resumeInputMode.value = value;
  errorMessage.value = "";

  if (value === "file") {
    resumeText.value = "";
    return;
  }

  selectedResumeFile.value = null;
  selectedFileName.value = "";
}

function validateAnalysisInput() {
  if (!jobDescription.value.trim()) {
    errorMessage.value = "請先貼上職缺描述。";
    return false;
  }

  if (resumeInputMode.value === "file" && !selectedResumeFile.value) {
    errorMessage.value = "請先選擇履歷檔案，或切換成貼上履歷文字。";
    return false;
  }

  if (resumeInputMode.value === "text" && !resumeText.value.trim()) {
    errorMessage.value = "請先貼上履歷文字，或切換成上傳履歷檔案。";
    return false;
  }

  return true;
}

async function handleAnalyzeJobFit() {
  errorMessage.value = "";

  if (!validateAnalysisInput()) {
    return;
  }

  isAnalyzing.value = true;
  analysisResult.value = null;

  try {
    analysisResult.value = await analyzeJobFit({
      jobDescription: jobDescription.value,
      resumeText: resumeInputMode.value === "text" ? resumeText.value : "",
      resumeFile:
        resumeInputMode.value === "file" ? selectedResumeFile.value : null,
    });
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : "無法連線到後端服務，請確認 FastAPI 是否已啟動。";
  } finally {
    isAnalyzing.value = false;
  }
}
</script>

<template>
  <main class="relative min-h-screen bg-app-canvas text-app-text">
    <div
      class="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8"
    >
      <header
        class="mb-6 flex flex-col gap-4 border-b border-app-border pb-5 lg:flex-row lg:items-end lg:justify-between"
      >
        <div class="max-w-3xl">
          <h1
            class="text-3xl font-semibold tracking-normal text-app-text sm:text-4xl"
          >
            JobFit Analyzer
          </h1>
          <p class="mt-2 max-w-2xl text-base leading-7 text-app-muted">
            面試職缺匹配分析器
          </p>
        </div>
        <div class="flex items-center gap-2 text-sm text-app-muted">
          <Sparkles class="size-4 text-brand" aria-hidden="true" />
          <span>履歷 × 職缺分析</span>
        </div>
      </header>

      <section class="space-y-5">
        <div class="grid gap-5 lg:grid-cols-2">
          <ResumeInputCard
            :resume-input-mode="resumeInputMode"
            :resume-text="resumeText"
            :selected-file-name="selectedFileName"
            @update:resume-input-mode="handleResumeInputModeChange"
            @update:resume-text="resumeText = $event"
            @file-change="handleFileChange"
          />

          <JobDescriptionCard
            :job-description="jobDescription"
            @update:job-description="jobDescription = $event"
          />
        </div>

        <AnalyzeActionBar
          :is-analyzing="isAnalyzing"
          :error-message="errorMessage"
          @analyze="handleAnalyzeJobFit"
        />

        <AnalysisResultCard
          :analysis="analysisResult"
          :sections="displaySections"
          :has-result="Boolean(analysisResult)"
        />
      </section>

      <footer
        class="mt-5 flex flex-wrap justify-end gap-2 border-t border-app-border pt-4 text-xs font-medium text-app-subtle"
      >
        <Badge
          class="border border-app-border bg-app-panel-soft text-app-muted"
        >
          MVP 階段 1
        </Badge>
        <Badge
          variant="outline"
          class="border-app-border bg-app-panel text-app-muted"
        >
          Vue 3 + FastAPI
        </Badge>
        <span
          class="rounded-md border border-app-border bg-app-panel px-2.5 py-0.5 leading-5"
        >
          {{ appVersion }}
        </span>
      </footer>
    </div>
  </main>
</template>
