import re

def obliterate_edges_and_scroll(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the exact ensureAspectRatio function from your working code
    old_func_pattern = r'function ensureAspectRatio\(\)\s*\{[\s\S]*?canvasElement\.style\.width = newWidth \+ "px";\n\s*\}'
    
    # Apply stretch + runtime JS layout fixes (Zero HTML/CSS structural edits)
    new_func = """function ensureAspectRatio() {
        if (canvasElement === undefined) return;
        if (startingHeight === undefined && startingWidth === undefined) return;

        canvasElement.classList.add("active");

        // 1. DYNAMICALLY LOCK BODY: Prevents top/bottom page scrolling safely at runtime
        document.documentElement.style.overflow = "hidden";
        document.body.style.overflow = "hidden";
        document.body.style.margin = "0px";
        document.body.style.padding = "0px";
        
        // 2. NUKE FLEX MARGINS: Removes the automatic centering margins pushing the game down
        canvasElement.style.margin = "0px";
        canvasElement.style.padding = "0px";

        // 3. BRUTE FORCE STRETCH (Your working code)
        canvasElement.style.height = window.innerHeight + "px";
        canvasElement.style.width = window.innerWidth + "px";
        canvasElement.style.maxWidth = "100vw";
        canvasElement.style.maxHeight = "100vh";

        // 4. RESET VIEWPORT OFFSET: Snaps mobile browser address bar bounce to top
        window.scrollTo(0, 0);
      }"""

    # Apply the replacement
    new_content, count = re.subn(old_func_pattern, new_func, content)

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: Edges obliterated and scroll locked cleanly!")
    else:
        print("FAILED: Could not find the ensureAspectRatio function to replace.")

if __name__ == "__main__":
    obliterate_edges_and_scroll('index.html')