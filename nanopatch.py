import re

def obliterate_edges(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the exact ensureAspectRatio function from your HTML
    old_func_pattern = r'function ensureAspectRatio\(\)\s*\{[\s\S]*?canvasElement\.style\.width = newWidth \+ "px";\n\s*\}'
    
    # Replace it with a pure, math-free 100% stretch
    new_func = """function ensureAspectRatio() {
        if (canvasElement === undefined) return;
        if (startingHeight === undefined && startingWidth === undefined) return;

        canvasElement.classList.add("active");

        // BRUTE FORCE: Stretch to the exact screen size. No aspect ratio math. No black bars.
        canvasElement.style.height = window.innerHeight + "px";
        canvasElement.style.width = window.innerWidth + "px";
        
        // Ensure CSS doesn't restrict it either
        canvasElement.style.maxWidth = "100vw";
        canvasElement.style.maxHeight = "100vh";
      }"""

    # Apply the replacement
    new_content, count = re.subn(old_func_pattern, new_func, content)

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: Edges obliterated. The canvas will now ALWAYS stretch to fill the screen.")
    else:
        print("FAILED: Could not find the ensureAspectRatio function to replace.")

if __name__ == "__main__":
    obliterate_edges('index.html')