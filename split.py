import os, re

base_dir = r'c:\Users\rehan shaikh\Desktop\OSINT'
file_path = os.path.join(base_dir, 'heartsint-18.html')

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Extractor helpers
def get_between(text, start, end):
    try:
        s = text.index(start)
        e = text.index(end, s)
        return text[s:e]
    except ValueError:
        return ""

def get_from(text, start):
    try:
        return text[text.index(start):]
    except ValueError:
        return ""

# HTML Blocks
head_nav_main = html[:html.find('<!-- DASHBOARD -->')]
dash_block = get_between(html, '<!-- DASHBOARD -->', '<!-- USERNAME OSINT -->')
tools_block = get_between(html, '<!-- USERNAME OSINT -->', '<!-- CDR ANALYSIS -->')
adv_block = get_between(html, '<!-- CDR ANALYSIS -->', '<!-- API SETTINGS -->')
sys_block = get_between(html, '<!-- API SETTINGS -->', '</main>')

# JS Blocks
main_js_start = html.find('<script>')
if main_js_start == -1:
    main_js_start = html.find('// ── GLOBALS ──') - 10

js_global = get_between(html, '</main>', '// ── PLATFORM DATABASE ──')
js_tools = get_between(html, '// ── PLATFORM DATABASE ──', '// ── LEAKDB ──')
js_adv_leakdb = get_between(html, '// ── LEAKDB ──', '// ── SETTINGS ──')

# Note: SETTINGS is between LEAKDB and INSTAGRAM MONITOR
js_system = get_between(html, '// ── SETTINGS ──', '// ── INSTAGRAM MONITOR ──')

js_adv_ig = get_between(html, '// ── INSTAGRAM MONITOR ──', '<script>\n// ── CDR PLATFORM ──')
if not js_adv_ig: 
    # Try finding end of script if CDR PLATFORM is not there
    js_adv_ig = get_between(html, '// ── INSTAGRAM MONITOR ──', '</script>')

js_cdr = ""
if '<script>\n// ── CDR PLATFORM ──' in html:
    js_cdr = get_from(html, '<script>\n// ── CDR PLATFORM ──')

# Rewrite the switchPanel logic in js_global
routing_logic = """
const panelGroup = {
  dashboard: 'heartsint-18.html',
  username: 'tools.html',
  email: 'tools.html',
  phone: 'tools.html',
  ip: 'tools.html',
  domain: 'tools.html',
  crypto: 'tools.html',
  cdr: 'advanced.html',
  leakdb: 'advanced.html',
  igmonitor: 'advanced.html',
  settings: 'system.html'
};

function switchPanel(id){
  if(RESTRICTED_PANELS.includes(id)&&!leaAuthenticated){
    leaPendingPanel=id;
    showLEAGate();
    return;
  }
  const targetPage = panelGroup[id];
  let currentPage = window.location.pathname.split('/').pop() || 'heartsint-18.html';
  if(!currentPage.endsWith('.html')) currentPage = 'heartsint-18.html';
  
  if (targetPage !== currentPage) {
    window.location.href = targetPage + '?panel=' + id;
    return;
  }
  
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  const targetPanel = document.getElementById('panel-'+id);
  if(targetPanel) targetPanel.classList.add('active');
  document.querySelectorAll('.nav-item').forEach(n=>{
    if(n.getAttribute('onclick') && n.getAttribute('onclick').includes("'"+id+"'")) {
       n.classList.add('active');
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
   const urlParams = new URLSearchParams(window.location.search);
   const panel = urlParams.get('panel');
   if(panel) {
      setTimeout(() => switchPanel(panel), 100);
   }
});
"""

# Find switchPanel function in js_global and replace it
# We know where it starts, but where does it end?
start_idx = js_global.find('function switchPanel(id){')
if start_idx != -1:
    end_idx = js_global.find('function addRecent(type,query){', start_idx)
    if end_idx != -1:
        # include the preceding comments for switchPanel if needed, but start_idx is precise
        js_global = js_global[:start_idx] + routing_logic + '\n\n' + js_global[end_idx:]

# Assemble files
def build_file(html_content, js_content):
    res = head_nav_main + html_content + '</main>\n</div>\n' + js_global + js_content
    # if it doesn't end with html, add closing tags
    if '</html>' not in res:
        res += '\n</script>\n</body>\n</html>'
    return res

dashboard_file = build_file(dash_block, "\n</script>\n</body>\n</html>")
tools_file = build_file(tools_block, js_tools + "\n</script>\n</body>\n</html>")
advanced_file = build_file(adv_block, js_adv_leakdb + js_adv_ig + "\n</script>\n" + js_cdr)
system_file = build_file(sys_block, js_system + "\n</script>\n</body>\n</html>")

with open(os.path.join(base_dir, 'heartsint-18.html'), 'w', encoding='utf-8') as f:
    f.write(dashboard_file)
with open(os.path.join(base_dir, 'tools.html'), 'w', encoding='utf-8') as f:
    f.write(tools_file)
with open(os.path.join(base_dir, 'advanced.html'), 'w', encoding='utf-8') as f:
    f.write(advanced_file)
with open(os.path.join(base_dir, 'system.html'), 'w', encoding='utf-8') as f:
    f.write(system_file)

print("Split completed successfully!")
