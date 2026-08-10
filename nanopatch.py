import re

def apply_full_mobile_fix(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Force Canvas Stretch (Obliterates Side Borders)
    old_func_pattern = r'function ensureAspectRatio\(\)\s*\{[\s\S]*?canvasElement\.style\.width = newWidth \+ "px";\n\s*\}'
    new_func = """function ensureAspectRatio() {
        if (canvasElement === undefined) return;
        if (startingHeight === undefined && startingWidth === undefined) return;

        canvasElement.classList.add("active");

        canvasElement.style.height = window.innerHeight + "px";
        canvasElement.style.width = window.innerWidth + "px";
        canvasElement.style.maxWidth = "100vw";
        canvasElement.style.maxHeight = "100vh";
      }"""

    content, js_count = re.subn(old_func_pattern, new_func, content)

    # 2. Inject Anti-Scroll & Edge-Pinning CSS (Nukes Top/Bottom Scrolling)
    anti_scroll_css = """
    <style>
      html, body {
        width: 100vw !important;
        height: 100vh !important;
        height: 100svh !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        touch-action: none !important;
      }
      
      canvas.emscripten {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
      }
    </style>
  </head>
    """

    content, css_count = re.subn(r'</head>', anti_scroll_css, content, flags=re.IGNORECASE)

    # Write patched file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Patch complete! (JS Stretched: {js_count > 0}, Anti-Scroll Applied: {css_count > 0})")

if __name__ == "__main__":
    apply_full_mobile_fix('index.html')