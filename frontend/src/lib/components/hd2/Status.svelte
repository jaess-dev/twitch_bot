<script>
  import Hd2Slogan from "./Hd2Slogan.svelte";

  let { kills } = $props();
</script>

<div
  class="fixed top-0 left-0 right-0
         grid grid-cols-[1fr_auto_1fr]
         items-center
         px-4 py-2
         bg-black/70 backdrop-blur-md
         border-b border-yellow-600
         text-yellow-300 text-sm font-bold"
>
  <div class="justify-self-start flex space-x-4">
    <!-- <span>MISSION TIME: <span class="text-white">00:12:34</span></span> -->
    <!-- <span>WAVE: <span class="text-white">03</span></span> -->
  </div>

  <div class="justify-self-center">
    <Hd2Slogan text="JaessDev" />
  </div>

  <div class="justify-self-end flex space-x-4">
    <span>TEAM KILLS: <span class="text-white">{kills}</span></span>
    <!-- <span>SUPPLY: <span class="text-white">45%</span></span> -->
  </div>
</div>

<style>
</style>
