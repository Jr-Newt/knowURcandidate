import json
import os
import glob
from pathlib import Path

# Find all browser subagent logs
log_pattern = r"C:\Users\LEGION\.gemini\antigravity\brain\15b12f7b-9718-4261-a720-7c31277a2f51\.system_generated\**\*.json"
log_files = glob.glob(log_pattern, recursive=True)

print(f"Found {len(log_files)} json files in .system_generated")

# Sort by modification time (newest first)
log_files.sort(key=os.path.getmtime, reverse=True)

html_content = None

for file_path in log_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for the network request response or DOM extraction
            if "CandidateCustomFilter" in content and ("<html" in content or "<div" in content):
                print(f"Found potential HTML in {file_path}")
                # Try to parse as JSON if it's a structured log
                try:
                    data = json.loads(content)
                    # We would need complex extraction here depending on the log structure
                    # But as a simple fallback, let's just find the first large HTML-like string
                    import re
                    # Look for a large block starting with <html or <!DOCTYPE
                    html_match = re.search(r'(<html.*?</html\s*>)', content, re.IGNORECASE | re.DOTALL)
                    if not html_match:
                        # Sometimes it's double-escaped JSON
                        html_match = re.search(r'(<div class="row".*?)', content, re.IGNORECASE | re.DOTALL)
                        
                    if html_match and len(html_match.group(1)) > 10000:
                        html_content = html_match.group(1).replace('\\"', '"').replace('\\n', '\n')
                        break
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        continue
        
if html_content:
    out_path = Path("d:/knowyourcandidate/scraper/output/kerala_candidates_raw.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully extracted {len(html_content)} bytes of HTML to {out_path}")
else:
    print("Could not find HTML content in recent logs.")

