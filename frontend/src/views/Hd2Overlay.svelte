<script lang="ts">
  import { onMount } from "svelte";
  import type { AppState } from "../lib/types/types";
  import { WebSocketClient } from "../lib/web_socket";
  import Status from "../lib/components/hd2/Status.svelte";
  import LiveLog from "../lib/components/hd2/LiveLog.svelte";

  // import "/src/styles/hd2.css";

  const _state = window.__APP_STATE__ as AppState;

  let counter = $state(_state.counter);
  let formattedKills = $derived(counter.toLocaleString());

  let serverMessages = $state([
    // "[jaessdev] A really long message which should span over multiple lines lets see",
    // "[00:12:31] SUPPLY DROP AVAILABLE",
    // "[00:12:32] ENEMY ARMOR DESTROYED",
    // "[00:12:33] TEAM KILL +1",
    // "[00:12:34] MISSION TIME EXTENDED",
    // "[x] hello",
    // "[x] bye",
    // "[x] bye",
    // "[x] bye",
    // "[x] bye",
    // "[x] bye",
    // "[x] bye",
  ]);

  let messages = $derived.by(() => {
    let m = serverMessages.slice();
    m.reverse();
    return m;
  });

  let title = _state.title;

  let wsClient: WebSocketClient<{ counter?: number; messages?: string[] }>;

  onMount(() => {
    wsClient = new WebSocketClient(`ws://${window.location.host}/ws`);

    wsClient.onMessage((data) => {
      console.log(`Received ${data}`);
      if (data.counter !== undefined) {
        counter = data.counter;
      }

      if (data.messages !== undefined) {
        serverMessages = data.messages;
      }
    });

    wsClient.connect();

    return () => wsClient.disconnect();
  });
</script>

<Status kills={formattedKills} useLower={true}/>
<LiveLog messages={messages} />

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
