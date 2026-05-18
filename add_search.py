import os
import glob

html_code = """
    <!-- Full-screen Search Overlay -->
    <div id="search-overlay" class="fixed inset-0 bg-white/95 backdrop-blur-sm z-[100] flex flex-col hidden opacity-0 transition-opacity duration-300">
        <div class="container mx-auto px-4 py-8 flex justify-end">
            <button id="close-search" class="text-black hover:opacity-70 transition p-2">
                <i data-lucide="x" width="32" height="32" stroke-width="1.5"></i>
            </button>
        </div>
        <div class="container mx-auto px-4 md:px-8 max-w-4xl flex-1 flex flex-col pt-10">
            <div class="relative w-full border-b-2 border-black pb-2 mb-8">
                <i data-lucide="search" class="absolute left-0 top-1/2 -translate-y-1/2 text-gray-400" width="28" height="28" stroke-width="2"></i>
                <input type="text" id="search-input" placeholder="Search products..." autocomplete="off" class="w-full bg-transparent text-3xl md:text-5xl font-light text-black placeholder-gray-300 outline-none pl-12 py-2">
            </div>
            
            <!-- Search Results Area -->
            <div id="search-results" class="flex-1 overflow-y-auto w-full pb-20">
                <!-- Mock categories/suggestions when empty -->
                <div id="search-empty-state" class="text-gray-500">
                    <p class="text-sm font-semibold uppercase tracking-wider mb-4">Popular Categories</p>
                    <div class="flex flex-wrap gap-4">
                        <a href="headphones.html" class="px-5 py-2 rounded-full border border-gray-200 hover:border-black transition text-black text-sm">Headphones</a>
                        <a href="#" class="px-5 py-2 rounded-full border border-gray-200 hover:border-black transition text-black text-sm">Microphones</a>
                        <a href="#" class="px-5 py-2 rounded-full border border-gray-200 hover:border-black transition text-black text-sm">Smartwatches</a>
                        <a href="#" class="px-5 py-2 rounded-full border border-gray-200 hover:border-black transition text-black text-sm">Speakers</a>
                    </div>
                </div>

                <!-- Dynamic results grid -->
                <div id="search-results-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 hidden">
                    <!-- JS will inject results here -->
                </div>
                <div id="search-no-results" class="hidden text-center text-gray-500 py-10">
                    No products found for your query.
                </div>
            </div>
        </div>
    </div>
"""

js_code = """
    <!-- Search Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {
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

            if (!searchOverlay || allSearchBtns.length === 0) return;

            allSearchBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    searchOverlay.classList.remove('hidden');
                    setTimeout(() => {
                        searchOverlay.classList.remove('opacity-0');
                        searchInput.focus();
                    }, 10);
                    document.body.style.overflow = 'hidden';
                });
            });

            closeSearch.addEventListener('click', () => {
                searchOverlay.classList.add('opacity-0');
                setTimeout(() => {
                    searchOverlay.classList.add('hidden');
                }, 300);
                document.body.style.overflow = '';
                searchInput.value = '';
                renderResults('');
            });

            searchInput.addEventListener('input', (e) => {
                renderResults(e.target.value.trim().toLowerCase());
            });

            function renderResults(query) {
                if (!query) {
                    searchEmptyState.classList.remove('hidden');
                    searchResultsGrid.classList.add('hidden');
                    searchNoResults.classList.add('hidden');
                    return;
                }

                const filtered = products.filter(p => 
                    p.title.toLowerCase().includes(query) || 
                    p.category.toLowerCase().includes(query)
                );

                searchEmptyState.classList.add('hidden');
                
                if (filtered.length === 0) {
                    searchResultsGrid.classList.add('hidden');
                    searchNoResults.classList.remove('hidden');
                } else {
                    searchNoResults.classList.add('hidden');
                    searchResultsGrid.classList.remove('hidden');
                    
                    searchResultsGrid.innerHTML = filtered.map(p => `
                        <a href="${p.url}" class="group flex items-center p-4 border border-gray-100 rounded-2xl hover:border-black transition cursor-pointer bg-white">
                            <div class="w-20 h-20 bg-[#f5f5f5] rounded-xl flex items-center justify-center p-2 mr-4 overflow-hidden flex-shrink-0">
                                <img src="${p.img}" class="w-full h-full object-contain mix-blend-multiply group-hover:scale-110 transition duration-300">
                            </div>
                            <div class="flex-1 overflow-hidden">
                                <p class="text-[11px] text-gray-500 uppercase tracking-wider mb-1">${p.category}</p>
                                <h4 class="text-sm font-bold text-black truncate group-hover:underline">${p.title}</h4>
                                <p class="text-sm font-medium text-black mt-1">${p.price}</p>
                            </div>
                        </a>
                    `).join('');
                }
            }
        });
    </script>
"""

import sys

for filepath in glob.glob('*.html'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'id="search-overlay"' in content:
        print(f"Skipping {filepath}, search overlay already exists.")
        continue

    if '</body>' in content:
        content = content.replace('</body>', f"{html_code}\n{js_code}\n</body>")
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")
    else:
        print(f"Error: </body> not found in {filepath}")
