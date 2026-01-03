<script lang="ts">
  let { messages }: { messages: string[] } = $props();
</script>

<div
  class="
    fixed
    right-2
    top-[55%]
    -translate-y-full
    w-[25%]
    max-h-32
    overflow-hidden
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
    flex
    flex-col-reverse
    gap-1
  "
>
  {#each messages as message}
    <div class="leading-tight whitespace-pre-wrap">
      {message}
    </div>
  {/each}
</div>
