import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# The old inline search container to remove
old_search_pattern = re.compile(
    r'\s*<div class="relative flex items-center h-8 header-search-container" id="inline-search-container">.*?(?=<a href="#" class="hidden sm:flex items-center hover:text-black transition">)',
    re.DOTALL
)

new_trigger = '''                    <button class="offcanvas-search-trigger hover:text-black transition flex items-center justify-center p-1 rounded-full text-gray-800"><i data-lucide="search" stroke-width="1.5" width="22" height="22"></i></button>
                    '''

# The old inline search script block to remove
old_script_pattern = re.compile(
    r'\s*<!-- Inline Search Logic -->.*?</script>',
    re.DOTALL
)

offcanvas_html_script = '''
    <!-- Offcanvas Search -->
    <div id="search-offcanvas-overlay" class="fixed inset-0 bg-black/50 z-[100] opacity-0 pointer-events-none transition-opacity duration-300"></div>
    <div id="search-offcanvas" class="fixed top-0 right-0 w-full md:w-[450px] h-full bg-white z-[110] transform translate-x-full transition-transform duration-300 ease-out shadow-2xl flex flex-col rounded-l-3xl">
        <div class="px-8 py-6 flex items-center justify-between border-b border-gray-100">
            <h3 class="text-xl font-bold text-black">Search</h3>
            <button id="close-search-btn" class="w-10 h-10 flex items-center justify-center rounded-full border border-gray-200 hover:bg-gray-50 transition text-gray-500">
                <i data-lucide="x" width="18" height="18"></i>
            </button>
        </div>
        <div class="p-8 flex-1 overflow-y-auto">
            <div class="relative mb-8">
                <i data-lucide="search" width="20" height="20" class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                <input type="text" id="offcanvas-search-input" class="w-full bg-gray-50 border-none rounded-xl py-4 pl-12 pr-4 text-sm focus:ring-2 focus:ring-black/5 transition" placeholder="Search everything...">
            </div>
            
            <!-- Mock categories/suggestions when empty -->
            <div id="search-empty-state" class="text-gray-500">
                <p class="text-xs font-semibold uppercase tracking-wider mb-4 text-gray-400">Popular Categories</p>
                <div class="flex flex-wrap gap-2">
                    <a href="headphones.html" class="px-4 py-2 rounded-xl bg-gray-50 hover:bg-gray-100 hover:text-black transition text-gray-600 text-xs font-medium">Headphones</a>
                    <a href="#" class="px-4 py-2 rounded-xl bg-gray-50 hover:bg-gray-100 hover:text-black transition text-gray-600 text-xs font-medium">Microphones</a>
                    <a href="#" class="px-4 py-2 rounded-xl bg-gray-50 hover:bg-gray-100 hover:text-black transition text-gray-600 text-xs font-medium">Smartwatches</a>
                    <a href="#" class="px-4 py-2 rounded-xl bg-gray-50 hover:bg-gray-100 hover:text-black transition text-gray-600 text-xs font-medium">Speakers</a>
                </div>
            </div>

            <!-- Dynamic results grid -->
            <div id="search-results-grid" class="grid grid-cols-1 gap-4 hidden">
                <!-- JS will inject results here -->
            </div>
            <div id="search-no-results" class="hidden text-center text-gray-500 py-12 text-sm flex-col items-center">
                <i data-lucide="search-x" width="32" height="32" class="text-gray-300 mb-3"></i>
                <p>No products found.</p>
            </div>
        </div>
    </div>

    <!-- Offcanvas Search Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const triggers = document.querySelectorAll('.offcanvas-search-trigger');
            const overlay = document.getElementById('search-offcanvas-overlay');
            const offcanvas = document.getElementById('search-offcanvas');
            const closeBtn = document.getElementById('close-search-btn');
            const input = document.getElementById('offcanvas-search-input');
            const emptyState = document.getElementById('search-empty-state');
            const resultsGrid = document.getElementById('search-results-grid');
            const noResults = document.getElementById('search-no-results');

            if(!offcanvas) return;

            const products = [
                { title: "Wireless Gaming Headphones MS920", category: "Headphones", price: "$75.66", url: "product-details.html", img: "images/most-sold-1.png" },
                { title: "Wireless Gaming Headphones DM420", category: "Headphones", price: "$117.88", url: "product-details.html", img: "images/most-sold-2.png" },
                { title: "W75 Automobili Lamborghini Headphones", category: "Headphones", price: "$247.55", url: "product-details.html", img: "images/most-sold-3.png" },
                { title: "Smart Ergonomic Wireless Headphones", category: "Headphones", price: "$48.90", url: "product-details.html", img: "images/most-sold-4.jpg" },
                { title: "Master Dynamic MW75 Active Noise-Cancelling", category: "Headphones", price: "$249.00", url: "product-details.html", img: "images/most-sold-5.png" },
                { title: "Studio Pro Microphone", category: "Microphones", price: "$129.99", url: "product-details.html", img: "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&q=80&w=400" },
                { title: "Fitness Tracker Pro", category: "Smartwatches", price: "$199.50", url: "product-details.html", img: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&q=80&w=400" },
                { title: "Portable Bluetooth Speaker", category: "Speakers", price: "$89.00", url: "product-details.html", img: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?auto=format&fit=crop&q=80&w=400" }
            ];

            function openSearch() {
                overlay.classList.remove('opacity-0', 'pointer-events-none');
                overlay.classList.add('opacity-100', 'pointer-events-auto');
                offcanvas.classList.remove('translate-x-full');
                setTimeout(() => input.focus(), 300);
            }

            function closeSearch() {
                overlay.classList.remove('opacity-100', 'pointer-events-auto');
                overlay.classList.add('opacity-0', 'pointer-events-none');
                offcanvas.classList.add('translate-x-full');
            }

            triggers.forEach(trigger => {
                trigger.addEventListener('click', (e) => {
                    e.preventDefault();
                    openSearch();
                });
            });

            closeBtn.addEventListener('click', closeSearch);
            overlay.addEventListener('click', closeSearch);

            input.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase().trim();
                
                if (query.length === 0) {
                    emptyState.classList.remove('hidden');
                    resultsGrid.classList.add('hidden');
                    noResults.classList.add('hidden');
                    return;
                }

                emptyState.classList.add('hidden');
                
                const filtered = products.filter(p => 
                    p.title.toLowerCase().includes(query) || 
                    p.category.toLowerCase().includes(query)
                );

                if (filtered.length > 0) {
                    resultsGrid.innerHTML = filtered.map(p => `
                        <a href="${p.url}" class="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-50 transition border border-transparent hover:border-gray-100 group">
                            <div class="w-14 h-14 bg-[#f8f9fa] rounded-lg flex items-center justify-center p-2 flex-shrink-0 group-hover:scale-105 transition">
                                <img src="${p.img}" alt="${p.title}" class="w-full h-full object-contain mix-blend-multiply">
                            </div>
                            <div class="flex-1 min-w-0">
                                <h4 class="text-sm font-bold text-black truncate">${p.title}</h4>
                                <p class="text-xs text-gray-500">${p.category}</p>
                            </div>
                            <div class="text-sm font-bold text-black flex-shrink-0">
                                ${p.price}
                            </div>
                        </a>
                    `).join('');
                    resultsGrid.classList.remove('hidden');
                    noResults.classList.add('hidden');
                } else {
                    resultsGrid.classList.add('hidden');
                    noResults.classList.remove('hidden');
                }
            });
        });
    </script>
</body>
'''

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already offcanvas logic is there
    if 'Offcanvas Search Logic' in content:
        continue

    # Replace header search container
    content = old_search_pattern.sub(new_trigger, content)
    
    # Remove old inline search logic if present
    content = old_script_pattern.sub('', content)

    # Inject offcanvas HTML & JS before </body>
    content = content.replace('</body>', offcanvas_html_script)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {file}")
