import re

def fix_and_prevent_scroll(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Restore the WORKING edge-to-edge canvas stretch JS function from Turn 5
    old_func_pattern = r'function ensureAspectRatio\(\)\s*\{[\s\S]*?canvasElement\.style\.width = newWidth \+ "px";\n\s*\}'
    working_js_func = """function ensureAspectRatio() {
        if (canvasElement === undefined) return;
        if (startingHeight === undefined && startingWidth === undefined) return;

        canvasElement.classList.add("active");

        canvasElement.style.height = window.innerHeight + "px";
        canvasElement.style.width = window.innerWidth + "px";
        canvasElement.style.maxWidth = "100vw";
        canvasElement.style.maxHeight = "100vh";
      }"""

    content, js_count = re.subn(old_func_pattern, working_js_func, content)

    # 2. Add lightweight anti-scroll CSS & event listener (Safe for WebGL)
    safe_anti_scroll = """
    <style>
      html, body {
        width: 100% !important;
        height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
      }
      canvas.emscripten {
        margin: 0 !important;
        padding: 0 !important;
        display: block;
      }
    </style>
    <script>
      // Prevent touch drag scrolling without modifying document layout flow
      document.addEventListener('touchmove', function(e) {
        if (e.target === document.documentElement || e.target === document.body) {
          e.preventDefault();
        }
      }, { passive: false });
    </script>
  </head>
    """

    content, css_count = re.subn(r'</head>', safe_anti_scroll, content, flags=re.IGNORECASE)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Patched successfully! (JS Restored: {js_count > 0}, Safe Scroll Prevented: {css_count > 0})")

if __name__ == "__main__":
    fix_and_prevent_scroll('index.html')