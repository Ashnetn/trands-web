import glob
import re

old_header_btn_variants = [
    '<button class="hover:text-black transition"><i data-lucide="search" stroke-width="1.5" width="22"\n                            height="22"></i></button>',
    '<button class="hover:text-black transition"><i data-lucide="search" stroke-width="1.5" width="22" height="22"></i></button>',
    '<button class="hover:text-black transition"><i data-lucide="search" stroke-width="1.5" width="22" height="22" ></i></button>'
]

new_header_html = """
<div class="relative flex items-center h-8 header-search-container" id="inline-search-container">
    <input type="text" class="header-search-input w-0 opacity-0 transition-all duration-300 border-none outline-none bg-gray-100 placeholder-gray-400 text-sm h-full rounded-full px-0 focus:ring-0 focus:outline-none focus:w-48 md:focus:w-64 focus:px-4 focus:opacity-100" placeholder="Search products...">
    <button class="header-search-btn hover:text-black transition flex items-center justify-center p-1 rounded-full text-gray-800 z-10"><i data-lucide="search" stroke-width="1.5" width="22" height="22"></i></button>
    <!-- Dropdown -->
    <div class="header-search-dropdown absolute top-full right-0 mt-4 w-[300px] md:w-[350px] bg-white shadow-2xl rounded-2xl border border-gray-100 overflow-hidden opacity-0 pointer-events-none transition-opacity duration-300 flex-col z-[100]">
        <!-- Search Results Area -->
        <div class="search-results max-h-[400px] overflow-y-auto w-full p-4">
            <!-- Mock categories/suggestions when empty -->
            <div class="search-empty-state text-gray-500">
                <p class="text-xs font-semibold uppercase tracking-wider mb-3">Popular Categories</p>
                <div class="flex flex-wrap gap-2">
                    <a href="headphones.html" class="px-3 py-1.5 rounded-full border border-gray-200 hover:border-black transition text-black text-xs">Headphones</a>
                    <a href="#" class="px-3 py-1.5 rounded-full border border-gray-200 hover:border-black transition text-black text-xs">Microphones</a>
                    <a href="#" class="px-3 py-1.5 rounded-full border border-gray-200 hover:border-black transition text-black text-xs">Smartwatches</a>
                    <a href="#" class="px-3 py-1.5 rounded-full border border-gray-200 hover:border-black transition text-black text-xs">Speakers</a>
                </div>
            </div>

            <!-- Dynamic results grid -->
            <div class="search-results-grid grid grid-cols-1 gap-3 hidden">
                <!-- JS will inject results here -->
            </div>
            <div class="search-no-results hidden text-center text-gray-500 py-6 text-sm">
                No products found.
            </div>
        </div>
    </div>
</div>
"""

new_js = """
    <!-- Inline Search Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const containers = document.querySelectorAll('.header-search-container');
            
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

            containers.forEach(container => {
                const btn = container.querySelector('.header-search-btn');
                const input = container.querySelector('.header-search-input');
                const dropdown = container.querySelector('.header-search-dropdown');
                const emptyState = container.querySelector('.search-empty-state');
                const resultsGrid = container.querySelector('.search-results-grid');
                const noResults = container.querySelector('.search-no-results');
                
                let isOpen = false;

                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (!isOpen) {
                        input.focus();
                    } else {
                        input.blur();
                    }
                });

                input.addEventListener('focus', () => {
                    isOpen = true;
                    dropdown.classList.remove('opacity-0', 'pointer-events-none');
                    dropdown.classList.add('opacity-100', 'pointer-events-auto');
                });

                input.addEventListener('blur', (e) => {
                    // Small timeout to allow clicking results before closing
                    setTimeout(() => {
                        isOpen = false;
                        dropdown.classList.add('opacity-0', 'pointer-events-none');
                        dropdown.classList.remove('opacity-100', 'pointer-events-auto');
                        input.value = '';
                        renderResults('');
                    }, 200);
                });

                input.addEventListener('input', (e) => {
                    renderResults(e.target.value.trim().toLowerCase());
                });

                function renderResults(query) {
                    if (!query) {
                        emptyState.classList.remove('hidden');
                        resultsGrid.classList.add('hidden');
                        noResults.classList.add('hidden');
                        return;
                    }

                    const filtered = products.filter(p => 
                        p.title.toLowerCase().includes(query) || 
                        p.category.toLowerCase().includes(query)
                    );

                    emptyState.classList.add('hidden');
                    
                    if (filtered.length === 0) {
                        resultsGrid.classList.add('hidden');
                        noResults.classList.remove('hidden');
                    } else {
                        noResults.classList.add('hidden');
                        resultsGrid.classList.remove('hidden');
                        
                        resultsGrid.innerHTML = filtered.map(p => `
                            <a href="${p.url}" class="group flex items-center p-2 rounded-xl hover:bg-gray-50 transition cursor-pointer">
                                <div class="w-12 h-12 bg-[#f5f5f5] rounded-lg flex items-center justify-center p-1 mr-3 overflow-hidden flex-shrink-0">
                                    <img src="${p.img}" class="w-full h-full object-contain mix-blend-multiply group-hover:scale-110 transition duration-300">
                                </div>
                                <div class="flex-1 overflow-hidden">
                                    <h4 class="text-xs font-bold text-black truncate group-hover:underline">${p.title}</h4>
                                    <p class="text-xs font-medium text-gray-500 mt-0.5">${p.price}</p>
                                </div>
                            </a>
                        `).join('');
                    }
                }
            });
        });
    </script>
"""

for filepath in glob.glob('*.html'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Remove old overlay HTML and script
    # The old overlay started with <!-- Full-screen Search Overlay --> and ended before </body>
    content = re.sub(r'<!-- Full-screen Search Overlay -->.*?<!-- Search Logic -->\s*<script>.*?</script>', '', content, flags=re.DOTALL)
    
    # 2. Replace header search button
    # Let's use a regex to find the button wrapping the search lucide icon exactly
    content = re.sub(r'<button class="hover:text-black transition">\s*<i data-lucide="search" stroke-width="1.5" width="22"[\s\r\n]*height="22"></i>\s*</button>', new_header_html, content)
    
    # 3. Append new script before </body>
    if new_js not in content:
        content = content.replace('</body>', f"{new_js}\n</body>")
        
    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"No changes for {filepath}")

