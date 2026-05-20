import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

# We'll replace the class of the topbar slider container
old_class = 'class="text-center flex-1 mt-2 md:mt-0 text-gray-300 flex justify-center items-center relative overflow-hidden h-6"'
new_class = 'class="text-center w-full flex-1 mt-2 md:mt-0 text-gray-300 flex justify-center items-center relative overflow-hidden h-6"'

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # also handle potential formatting differences (newlines)
    # Using regex to match the exact string allowing for newlines
    pattern = re.compile(r'class="text-center\s+flex-1\s+mt-2\s+md:mt-0\s+text-gray-300\s+flex\s+justify-center\s+items-center\s+relative\s+overflow-hidden\s+h-6"')
    
    content = pattern.sub(new_class, content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated {file}")
