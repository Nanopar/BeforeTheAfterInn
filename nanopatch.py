import re

def fix_gx_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 1. Replace the ensureAspectRatio function
    old_aspect_func = re.search(r'function ensureAspectRatio\(\) \{.*?\n\s*\}', html_content, re.DOTALL)
    
    new_aspect_func = """function ensureAspectRatio() {
        if (canvasElement === undefined) {
          return;
        }

        if (!CHANGE_ASPECT_RATIO) {
          return;
        }
        
        if (startingHeight === undefined && startingWidth === undefined) {
          return;
        }

        canvasElement.classList.add("active");

        const maxWidth = window.innerWidth;
        const maxHeight = window.innerHeight;
        var newHeight, newWidth;

        var heightQuotient = startingHeight / maxHeight;
        var widthQuotient = startingWidth / maxWidth;

        if (heightQuotient > widthQuotient) {
          newHeight = maxHeight;
          newWidth = newHeight * startingAspect;
        } else {
          newWidth = maxWidth;
          newHeight = newWidth / startingAspect;
        }

        canvasElement.style.height = newHeight + "px";
        canvasElement.style.width = newWidth + "px";
        canvasElement.style.maxWidth = "100vw";
        canvasElement.style.maxHeight = "100vh";
      }"""

    if old_aspect_func:
        html_content = html_content.replace(old_aspect_func.group(0), new_aspect_func)

    # 2. Replace the resizeObserver block to add staggered timeouts
    old_observer = re.search(r'const resizeObserver = new ResizeObserver\(.+?\);\s*resizeObserver\.observe\(.+?\);', html_content, re.DOTALL)
    
    new_observer = """const resizeObserver = new ResizeObserver(() => {
        window.requestAnimationFrame(ensureAspectRatio);
        setTimeout(() => window.requestAnimationFrame(ensureAspectRatio), 50);
        setTimeout(() => window.requestAnimationFrame(ensureAspectRatio), 250);
      });
      resizeObserver.observe(document.body);"""

    if old_observer:
        html_content = html_content.replace(old_observer.group(0), new_observer)

    # Write the fixed content back out
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Successfully patched HTML scaling routines!")

if __name__ == "__main__":
    # Change 'index.html' to the path of your exported file if needed
    fix_gx_html('index.html')