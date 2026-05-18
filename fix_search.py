import glob

for filepath in glob.glob('*.html'):
    with open(filepath, 'r') as f:
        content = f.read()

    # The block to replace
    old_code = """
            const searchBtns = document.querySelectorAll('button:has(i[data-lucide="search"])');
            const searchOverlay = document.getElementById('search-overlay');
            const closeSearch = document.getElementById('close-search');
            const searchInput = document.getElementById('search-input');
            const searchResultsGrid = document.getElementById('search-results-grid');
            const searchEmptyState = document.getElementById('search-empty-state');
            const searchNoResults = document.getElementById('search-no-results');

            // Fallback for Safari which doesn't support :has() completely in all versions
            // Alternative way to find search buttons
            let allSearchBtns = Array.from(searchBtns);
            if (allSearchBtns.length === 0) {
                const searchIcons = document.querySelectorAll('i[data-lucide="search"]');
                searchIcons.forEach(icon => {
                    const btn = icon.closest('button');
                    if (btn && !allSearchBtns.includes(btn)) allSearchBtns.push(btn);
                });
            }
"""

    new_code = """
            const searchOverlay = document.getElementById('search-overlay');
            const closeSearch = document.getElementById('close-search');
            const searchInput = document.getElementById('search-input');
            const searchResultsGrid = document.getElementById('search-results-grid');
            const searchEmptyState = document.getElementById('search-empty-state');
            const searchNoResults = document.getElementById('search-no-results');

            // Cross-browser way to find search buttons
            let allSearchBtns = [];
            const searchIcons = document.querySelectorAll('i[data-lucide="search"]');
            searchIcons.forEach(icon => {
                const btn = icon.closest('button');
                if (btn && !allSearchBtns.includes(btn)) allSearchBtns.push(btn);
                
                // If it's a link instead of a button
                const link = icon.closest('a');
                if (link && !allSearchBtns.includes(link)) allSearchBtns.push(link);
            });
"""

    # If the exact block isn't found because of whitespace, let's do a more robust replacement
    if old_code.strip() in content:
        content = content.replace(old_code.strip(), new_code.strip())
    else:
        # Fallback regex or robust replace
        import re
        content = re.sub(
            r'const searchBtns = document\.querySelectorAll\(\'button:has\(i\[data-lucide="search"\]\)\'\);.*?(?=const products = \[)',
            new_code.strip() + "\n\n            ",
            content,
            flags=re.DOTALL
        )

    # Also add lucide.createIcons() call inside renderResults
    # Find `searchResultsGrid.innerHTML = filtered.map`... block
    content = content.replace("`).join('');\n                }", "`).join('');\n                    if(typeof lucide !== 'undefined') lucide.createIcons();\n                }")

    with open(filepath, 'w') as f:
        f.write(content)

print("Fixed search script in all html files.")
