<div
  class="relative w-40 h-40 rounded-full bg-black/80 border-4 border-yellow-500 shadow-inner flex items-center justify-center"
>
  <div
    class="absolute inset-0 rounded-full border border-yellow-400 opacity-50 animate-pulseSlow"
  ></div>
  <div class="text-yellow-400 font-bold text-xl">RADAR</div>
</div>

<style>
  @keyframes pulseSlow {
    0%,
    100% {
      transform: scale(0.98);
      opacity: 0.6;
    }
    50% {
      transform: scale(1.02);
      opacity: 0.8;
    }
  }
  .animate-pulseSlow {
    animation: pulseSlow 2s infinite ease-in-out;
  }
</style>
