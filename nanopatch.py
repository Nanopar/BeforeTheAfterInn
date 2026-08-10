import re

def obliterate_landscape_gap(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the exact ensureAspectRatio function
    old_func_pattern = r'function ensureAspectRatio\(\)\s*\{[\s\S]*?canvasElement\.style\.width = newWidth \+ "px";\n\s*\}'
    
    # Overwrite ensureAspectRatio to target true physical viewport & continuously snap
    new_func = """function ensureAspectRatio() {
        if (canvasElement === undefined) return;

        canvasElement.classList.add("active");

        // 1. Force body and html to stop scroll bounces
        document.documentElement.style.overflow = "hidden";
        document.body.style.overflow = "hidden";
        document.body.style.margin = "0px";
        document.body.style.padding = "0px";
        canvasElement.style.margin = "0px";
        canvasElement.style.padding = "0px";

        // 2. Determine actual max landscape/portrait dimensions regardless of address bar lag
        var w = Math.max(window.innerWidth, document.documentElement.clientWidth);
        var h = Math.max(window.innerHeight, document.documentElement.clientHeight);

        // On mobile orientation shifts, use the full visual viewport if available
        if (window.visualViewport) {
          w = window.visualViewport.width;
          h = window.visualViewport.height;
        }

        canvasElement.style.width = w + "px";
        canvasElement.style.height = h + "px";
        canvasElement.style.maxWidth = "100vw";
        canvasElement.style.maxHeight = "100vh";

        window.scrollTo(0, 0);
      }

      // Re-trigger on visual viewport resize (when mobile URL bar hides/shows)
      if (window.visualViewport) {
        window.visualViewport.addEventListener('resize', ensureAspectRatio);
      }"""

    new_content, count = re.subn(old_func_pattern, new_func, content)

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: Landscape gap eliminated!")
    else:
        print("FAILED: Could not find function.")

if __name__ == "__main__":
    obliterate_landscape_gap('index.html')