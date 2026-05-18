import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Image container height
content = re.sub(r'relative h-64 mb-6 flex flex-col', r'relative h-[340px] mb-8 flex flex-col', content)

# 2. Badge styles
content = re.sub(r'text-\[11px\] font-bold px-3 py-1 rounded-full', r'text-[13px] font-bold px-3.5 py-1.5 rounded-full', content)
content = re.sub(r'width="10"\s+height="10"', r'width="12" height="12"', content)

# 3. Image height
content = re.sub(r'class="h-\[80%\] object-contain mix-blend-multiply', r'class="h-[90%] w-full object-contain mix-blend-multiply', content)

# 4. Text Category
content = re.sub(r'<p class="text-\[12px\] text-gray-500 mb-2">([^<]+)</p>', r'<p class="text-[14px] text-gray-500 mb-2 font-medium">\1</p>', content)

# 5. Text Title
content = re.sub(r'<h3 class="font-bold text-\[#111\] mb-3 line-clamp-2 text-\[15px\]', r'<h3 class="font-bold text-[#111] mb-4 line-clamp-2 text-[20px] leading-tight', content)

# 6. Text Price container
content = re.sub(r'class="flex items-center text-\[13px\]">', r'class="flex items-center text-[17px]">', content)

# 7. Price current
content = re.sub(r'<span\s+class="font-bold text-\[#111\] mr-2">', r'<span class="text-[#111] font-medium mr-2">', content)
content = re.sub(r'<span class="font-bold text-\[#111\]">', r'<span class="text-[#111] font-medium">', content)

# 8. Price strikethrough
content = re.sub(r'<span\s+class="text-gray-400 line-through">', r'<span class="text-[#999] line-through font-medium">', content)

with open('index.html', 'w') as f:
    f.write(content)

print("Done updating index.html")
