<script lang="ts">
  let { messages }: { messages: string[] } = $props();
</script>

<div
  class="
    fixed
    right-6
    top-1/2
    -translate-y-1/2
    w-full
    max-w-lg
    h-36
    overflow-y-auto
    bg-black/70
    backdrop-blur-sm
    border
    border-yellow-600
    text-yellow-300
    text-xs
    font-mono
    p-3
    rounded-lg
    shadow-lg
    text-left
  "
>
  {#each messages as message}
    <div class="leading-tight">{message}</div>
  {/each}
</div>

<style>
</style>
