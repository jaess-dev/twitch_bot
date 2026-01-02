<script lang="ts">
</script>

<div
  class="fixed bottom-6 right-6 bg-black/80 backdrop-blur-md border-l-4 border-yellow-500 text-yellow-300 px-4 py-2 rounded-md shadow-lg animate-fadeIn"
>
  <div class="font-bold text-lg">ALERT</div>
  <div class="text-sm">Enemy armor dropped!</div>
</div>

<style>
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  .animate-fadeIn {
    animation: fadeIn 0.3s ease-out forwards;
  }
</style>
