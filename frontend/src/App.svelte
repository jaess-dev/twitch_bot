<script lang="ts">
  import { onMount } from "svelte";
  import Overlay from "./views/Overlay.svelte";
  // import Home from "./Home.svelte";
  // import About from "./About.svelte";

  let route = "home";

  function updateRoute() {
    route = window.location.hash.replace("#/", "") || "home";
  }

  onMount(() => {
    updateRoute();
    window.addEventListener("hashchange", updateRoute);
    return () => window.removeEventListener("hashchange", updateRoute);
  });

  const state = window.__APP_STATE__;
</script>

{#if route === "home"}
  <p>Home</p>
{:else if route === "overlay"}
  <Overlay />
{:else}
  <p>Not found</p>
{/if}
