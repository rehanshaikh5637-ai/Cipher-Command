import os

base_dir = r'c:\Users\rehan shaikh\Desktop\OSINT'
files = ['heartsint-18.html', 'tools.html', 'advanced.html', 'system.html']

target = """  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  document.getElementById('panel-'+id).classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n=>{if(n.getAttribute('onclick')?.includes("'"+id+"'"))n.classList.add('active');});
}"""

for f in files:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Replace if exists
        content = content.replace(target, '')
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

print("Fixed syntaxes!")
