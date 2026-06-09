<script setup lang="ts">
import { FileText, Upload } from "@lucide/vue";
import { ref } from "vue";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";

defineProps<{
  resumeInputMode: "file" | "text";
  resumeText: string;
  selectedFileName: string;
}>();

const emit = defineEmits<{
  "update:resumeInputMode": [value: "file" | "text"];
  "update:resumeText": [value: string];
  "file-change": [event: Event];
}>();

const resumeFileInput = ref<HTMLInputElement | null>(null);

function openFilePicker() {
  resumeFileInput.value?.click();
}
</script>

<template>
  <Card class="rounded-lg border-app-border bg-app-panel text-app-text shadow-app">
    <CardHeader class="space-y-2">
      <div class="flex items-center gap-2 text-sm font-medium text-brand">
        <FileText class="size-4" aria-hidden="true" />
        <span>履歷</span>
      </div>
      <CardTitle class="text-xl font-semibold tracking-normal text-app-text">
        履歷輸入
      </CardTitle>
      <CardDescription class="text-app-muted">
        預設使用檔案上傳，也可以切換成直接貼上履歷文字。
      </CardDescription>
    </CardHeader>

    <CardContent class="space-y-4">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <Label class="text-sm font-medium text-app-text"> 輸入方式 </Label>
        <div class="grid grid-cols-2 rounded-lg border border-app-border bg-app-field p-1">
          <button
            type="button"
            class="rounded-md px-3 py-1.5 text-sm font-medium transition"
            :class="
              resumeInputMode === 'file'
                ? 'bg-brand-strong text-white'
                : 'text-app-muted hover:text-app-text'
            "
            @click="emit('update:resumeInputMode', 'file')"
          >
            上傳履歷
          </button>
          <button
            type="button"
            class="rounded-md px-3 py-1.5 text-sm font-medium transition"
            :class="
              resumeInputMode === 'text'
                ? 'bg-brand-strong text-white'
                : 'text-app-muted hover:text-app-text'
            "
            @click="emit('update:resumeInputMode', 'text')"
          >
            貼上文字
          </button>
        </div>
      </div>

      <div v-if="resumeInputMode === 'file'" class="space-y-2">
        <input
          id="resume-file"
          ref="resumeFileInput"
          type="file"
          accept=".pdf,.docx,.txt"
          class="sr-only"
          @change="emit('file-change', $event)"
        />

        <button
          type="button"
          class="group w-full rounded-lg border border-dashed border-app-border bg-app-panel-soft p-5 text-center transition hover:border-brand-border hover:bg-app-field"
          @click="openFilePicker"
        >
          <span class="mx-auto mb-4 flex size-12 items-center justify-center rounded-full bg-brand-soft text-brand transition group-hover:bg-brand-strong group-hover:text-white">
            <Upload class="size-5" aria-hidden="true" />
          </span>
          <span class="block text-base font-semibold text-app-text">
            上傳履歷檔案
          </span>
          <span class="mt-1 block text-sm leading-6 text-app-muted">
            點擊選擇 PDF、DOCX 或 TXT
          </span>
          <span class="mt-4 flex items-center justify-center gap-2 text-xs text-app-subtle">
            <span>檔案上限 5MB</span>
            <span class="size-1 rounded-full bg-app-subtle" />
            <span>不會儲存原始檔案</span>
          </span>
          <span
            v-if="selectedFileName"
            class="mx-auto mt-4 block max-w-full truncate rounded-md border border-brand-border bg-brand-soft px-3 py-2 text-xs font-medium text-brand"
          >
            已選擇：{{ selectedFileName }}
          </span>
        </button>
      </div>

      <div v-else class="space-y-2">
        <Textarea
          id="resume-text"
          :model-value="resumeText"
          class="min-h-56 resize-none border-app-border bg-app-field text-base leading-6 text-app-text placeholder:text-app-subtle focus-visible:ring-brand"
          placeholder="貼上履歷內容，例如工作經歷、專案、技能與學歷..."
          @update:model-value="emit('update:resumeText', String($event))"
        />
      </div>
    </CardContent>
  </Card>
</template>
