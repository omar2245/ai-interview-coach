<script setup lang="ts">
import { AlertCircle, ArrowRight } from "@lucide/vue";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";

defineProps<{
  isAnalyzing: boolean;
  errorMessage: string;
}>();

const emit = defineEmits<{
  analyze: [];
}>();
</script>

<template>
  <div class="grid gap-4 lg:grid-cols-[1fr_auto] lg:items-center">
    <Alert class="border-warning-border bg-warning-surface text-warning-text">
      <AlertCircle class="size-4" aria-hidden="true" />
      <AlertTitle class="font-semibold"> 已接上 FastAPI 假資料 </AlertTitle>
      <AlertDescription class="text-warning-text/80">
        目前後端會先回傳固定分析結果，之後再替換成 AI 產生內容。
      </AlertDescription>
    </Alert>

    <Alert
      v-if="errorMessage"
      class="border-destructive/40 bg-destructive/10 text-destructive"
    >
      <AlertCircle class="size-4" aria-hidden="true" />
      <AlertTitle class="font-semibold"> 分析失敗 </AlertTitle>
      <AlertDescription>
        {{ errorMessage }}
      </AlertDescription>
    </Alert>

    <Button
      class="h-11 cursor-pointer bg-cta-gradient px-8 text-base font-bold text-white shadow-cta hover:opacity-95 disabled:cursor-not-allowed disabled:opacity-60"
      :disabled="isAnalyzing"
      @click="emit('analyze')"
    >
      {{ isAnalyzing ? "分析中..." : "開始分析" }}
      <ArrowRight class="ml-2 size-4" aria-hidden="true" />
    </Button>
  </div>
</template>
