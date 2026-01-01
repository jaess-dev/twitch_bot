<script lang="ts">
  import { onMount } from "svelte";
  import type { AppState } from "../lib/types/types";
  import { WebSocketClient } from "../lib/web_socket";

  const _state = window.__APP_STATE__ as AppState;

  let counter = $state(_state.team_kill_counter);
  let formattedKills = $derived(counter.toLocaleString());

  const title = "Team Kills";

  let wsClient: WebSocketClient<{ counter: number }>;

  onMount(() => {
    wsClient = new WebSocketClient("ws://localhost:8000/ws");

    wsClient.onMessage((data) => {
      console.log(`Received ${data}`);
      if (data.counter !== undefined) {
        counter = data.counter;
      }
    });

    wsClient.connect();

    return () => wsClient.disconnect();
  });
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

<style>
  :root {
    background-color: transparent !important;
    margin: 0;
    padding: 0;
  }

  :global(.font-runic) {
    font-family: "MedievalSharp", monospace;
  }
</style>
