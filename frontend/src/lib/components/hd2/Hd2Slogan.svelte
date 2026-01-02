<script>
  let { text, reatio = 1.8 } = $props();
</script>

<div>
  <div class="hd2-stack">
    <div class="hd2-bar">
      <span class="hd2-text">{text}</span>
    </div>

    <div class="hd2-underline"></div>
  </div>
</div>

<style>
  .hd2-stack {
    --line-ratio: 1;
    --underline-ratio: (1 + (var(--line-ratio) * 2 - 0.2));
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }

  .hd2-bar {
    display: inline-flex;
    align-items: center;
    position: relative;
  }

  .hd2-text {
    color: #facc15;
    font-weight: 700;
    letter-spacing: 0.15em;
    white-space: nowrap;
    padding: 0 5px;
  }

  .hd2-text::before,
  .hd2-text::after {
    content: "";
    height: 6px;
    width: calc(100% * var(--line-ratio));
    background: #facc15;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
  }

  .hd2-text::before {
    right: 100%;
    margin-right: 12px;
    transform: translateY(-50%) skewX(45deg);
  }

  .hd2-text::after {
    left: 100%;
    margin-left: 12px;
    transform: translateY(-50%) skewX(-45deg);
  }

  .hd2-underline {
    height: 8px;
    background: #facc15;
    width: calc(var(--underline-ratio) * 100%);
    position: relative;
    top: -8px;
  }

  .hd2-underline::before,
  .hd2-underline::after {
    content: "";
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    background: #facc15;
  }

  .hd2-underline::before {
    left: -12px;
    transform: skewX(45deg);
  }

  .hd2-underline::after {
    right: -12px;
    transform: skewX(-45deg);
  }
</style>
