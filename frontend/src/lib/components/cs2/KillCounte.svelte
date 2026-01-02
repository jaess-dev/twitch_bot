<script lang="ts">
  let { title } = $props();
  let formattedKills = $derived(title.toLocaleString());
</script>

<div
  class="fixed top-6 right-6 z-50 flex flex-col items-end pointer-events-none"
>
  <div
    class="flex items-center justify-end px-5 py-2 rounded-lg bg-black/70 backdrop-blur-md text-white font-runic text-lg shadow-lg transition-all duration-300"
  >
    <!-- class:flash={flash} -->

    <span class="text-3xl mr-3 text-yellow-300">{title}:</span>
    <span class="text-3xl font-bold text-yellow-300">{formattedKills}</span>
  </div>
</div>

<style></style>
