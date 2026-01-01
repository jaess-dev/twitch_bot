import { mount } from "svelte";
import "./app.css";
import App from "./App.svelte";
import type { AppState } from "./lib/types/types";

interface Window {
  __APP_STATE__: AppState;
}

const initialRoute = (window as any).__INITIAL_ROUTE__ ?? "/";

if (!window.location.hash) {
  window.location.hash = `#${initialRoute}`;
}

const app = mount(App, {
  target: document.getElementById("app")!,
});

export default app;
