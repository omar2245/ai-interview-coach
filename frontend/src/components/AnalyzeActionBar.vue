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
