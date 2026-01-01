// src/lib/WebSocketClient.ts
export type MessageHandler<T = any> = (data: T) => void;

export class WebSocketClient<T = any> {
  private ws: WebSocket | null = null;
  private url: string;
  private handlers: MessageHandler<T>[] = [];

  constructor(url: string) {
    this.url = url;
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log("WebSocket connected to", this.url);
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as T;
        this.handlers.forEach((handler) => handler(data));
      } catch (e) {
        console.error("Failed to parse WebSocket message", e);
      }
    };

    this.ws.onclose = () => {
      console.log("WebSocket disconnected. Retrying in 2s...");
      setTimeout(() => this.connect(), 2000); // auto-reconnect
    };

    this.ws.onerror = (err) => {
      console.error("WebSocket error", err);
    };
  }

  send(data: T) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  onMessage(handler: MessageHandler<T>) {
    this.handlers.push(handler);
  }

  disconnect() {
    this.ws?.close();
    this.ws = null;
  }
}
