import re

with open('index.html', 'r') as f:
    content = f.read()

pattern = r'(<h3 class="font-bold text-\[\#111\] mb-4 line-clamp-2 text-\[20px\] leading-tight">)(.*?)(</h3>)'

def replace_func(match):
    h3_start = match.group(1).replace('leading-tight"', 'leading-tight hover:underline"')
    inner_content = match.group(2)
    h3_end = match.group(3)
    return f'<a href="product-details.html">\n                                {h3_start}{inner_content}{h3_end}\n                            </a>'

new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(new_content)
