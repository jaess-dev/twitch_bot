import { AppState } from "./lib/types/types";

export {};

declare global {
  interface Window {
    __APP_STATE__: AppState;
  }
}
