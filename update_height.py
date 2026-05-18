with open('index.html', 'r') as f:
    content = f.read()

content = content.replace('h-[340px]', 'h-[440px]')

with open('index.html', 'w') as f:
    f.write(content)

print("Done updating height.")
