<script lang="ts">
  import { onMount } from "svelte";
  import type { AppState } from "../lib/types/types";
  import { WebSocketClient } from "../lib/web_socket";
  import Status from "../lib/components/hd2/Status.svelte";
  import C2A from "../lib/components/hd2/C2A.svelte";
  import Floater from "../lib/components/hd2/Floater.svelte";
  import Radar from "../lib/components/hd2/Radar.svelte";
  import LiveLog from "../lib/components/hd2/LiveLog.svelte";
  import Hd2Slogan from "../lib/components/hd2/Hd2Slogan.svelte";

  // import "/src/styles/hd2.css";

  const _state = window.__APP_STATE__ as AppState;

  let counter = $state(_state.counter);
  let formattedKills = $derived(counter.toLocaleString());

  let messages = $state([
    "[00:12:31] SUPPLY DROP AVAILABLE",
    "[00:12:32] ENEMY ARMOR DESTROYED",
    "[00:12:33] TEAM KILL +1",
    "[00:12:34] MISSION TIME EXTENDED",
    "[x] hello",
    "[x] bye",
    "[x] bye",
    "[x] bye",
    "[x] bye",
    "[x] bye",
    "[x] bye",
  ]);

  let title = _state.title;

  let wsClient: WebSocketClient<{ counter?: number; messages?: string[] }>;

  onMount(() => {
    wsClient = new WebSocketClient("ws://localhost:8000/ws");

    wsClient.onMessage((data) => {
      console.log(`Received ${data}`);
      if (data.counter !== undefined) {
        counter = data.counter;
      }

      if (data.messages !== undefined) {
        messages = data.messages;
      }
    });

    wsClient.connect();

    return () => wsClient.disconnect();
  });
</script>

<Status kills={formattedKills} />
<LiveLog {messages} />

<!-- <C2A /> -->
<!-- <Floater /> -->

<!--
<Radar />
 -->

<!-- <Hd2Slogan text="JaessDev" /> -->
<!-- <Hd2Slogan text="Mission is seek and destory?" /> -->

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
