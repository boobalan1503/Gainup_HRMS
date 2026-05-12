"""
All HTML templates stored as Python multi-line strings.
render(name, **ctx) does a simple key-substitution via Jinja2 from string.
"""

from jinja2 import Environment, BaseLoader, select_autoescape

_env = Environment(loader=BaseLoader(), autoescape=select_autoescape(["html"]))
_env.globals["min"] = min
_env.globals["max"] = max


def render(template_str: str, **ctx) -> str:
    t = _env.from_string(template_str)
    return t.render(**ctx)


# ─── SHARED CSS ───────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:14px}
body{font-family:'Poppins',sans-serif;background:#F0F2FF;color:#1E293B;display:flex;min-height:100vh;overflow-x:hidden}
a{text-decoration:none;color:inherit}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-thumb{background:#CBD5E1;border-radius:99px}

/* Sidebar */
.sidebar{position:fixed;top:0;left:0;bottom:0;width:255px;background:#0F172A;display:flex;flex-direction:column;transition:width .25s;z-index:100;overflow:hidden}
.sidebar.collapsed{width:68px}
.sidebar.collapsed .brand-text,.sidebar.collapsed .nav-label,.sidebar.collapsed .nav-item span,.sidebar.collapsed .nav-section,.sidebar.collapsed .adm-details{display:none}
.sidebar.collapsed .nav-item{justify-content:center;padding:12px 0}
.sidebar-header{padding:18px 14px 14px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,.07)}
.brand{display:flex;align-items:center;gap:10px;overflow:hidden}
.brand-icon{width:36px;height:36px;background:#6C63FF;border-radius:9px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:15px;flex-shrink:0}
.brand-name{display:block;font-weight:700;font-size:15px;color:#fff}
.brand-sub{display:block;font-size:10px;color:rgba(255,255,255,.35);letter-spacing:.4px}
.toggle-btn{background:rgba(255,255,255,.07);border:none;cursor:pointer;color:rgba(255,255,255,.45);width:26px;height:26px;border-radius:6px;display:flex;align-items:center;justify-content:center;transition:.2s;flex-shrink:0}
.toggle-btn:hover{background:rgba(255,255,255,.13);color:#fff}
.sidebar-nav{flex:1;padding:14px 10px;overflow-y:auto;display:flex;flex-direction:column;gap:2px}
.nav-section{font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;color:rgba(255,255,255,.22);padding:10px 8px 3px}
.nav-item{display:flex;align-items:center;gap:11px;padding:9px 11px;border-radius:9px;color:rgba(255,255,255,.52);font-size:13px;font-weight:500;transition:.18s;white-space:nowrap}
.nav-item i{font-size:14px;min-width:17px;text-align:center}
.nav-item:hover{background:rgba(255,255,255,.07);color:rgba(255,255,255,.9)}
.nav-item.active{background:rgba(108,99,255,.22);color:#fff}
.nav-item.active i{color:#6C63FF}
.sidebar-footer{padding:14px;border-top:1px solid rgba(255,255,255,.07);display:flex;align-items:center;justify-content:space-between;gap:8px}
.adm-info{display:flex;align-items:center;gap:9px;overflow:hidden}
.adm-avatar{width:32px;height:32px;background:linear-gradient(135deg,#6C63FF,#FF6584);border-radius:9px;display:flex;align-items:center;justify-content:center;font-weight:700;color:#fff;font-size:13px;flex-shrink:0}
.adm-name{display:block;font-size:12px;font-weight:600;color:#fff}
.adm-role{display:block;font-size:10px;color:rgba(255,255,255,.32)}
.logout-a{color:rgba(255,255,255,.32);background:rgba(255,255,255,.05);width:30px;height:30px;border-radius:7px;display:flex;align-items:center;justify-content:center;transition:.18s;flex-shrink:0}
.logout-a:hover{color:#FF5B5B;background:rgba(255,91,91,.1)}

/* Main */
.main-content{margin-left:255px;flex:1;display:flex;flex-direction:column;min-height:100vh;transition:margin-left .25s}
.main-content.expanded{margin-left:68px}

/* Topbar */
.topbar{position:sticky;top:0;background:rgba(240,242,255,.88);backdrop-filter:blur(14px);border-bottom:1px solid #E2E8F0;padding:0 24px;height:62px;display:flex;align-items:center;justify-content:space-between;z-index:50}
.topbar-left{display:flex;align-items:center;gap:14px}
.pg-title h1{font-size:17px;font-weight:700;line-height:1}
.breadcrumb{font-size:11px;color:#94A3B8;display:flex;align-items:center;gap:5px;margin-top:2px}
.breadcrumb a{color:#6C63FF}
.breadcrumb a::after{content:"/";margin-left:5px;color:#CBD5E1}
.topbar-right{display:flex;align-items:center;gap:14px}
.date-pill{display:flex;align-items:center;gap:6px;font-size:11px;color:#64748B;background:#fff;padding:5px 11px;border-radius:20px;border:1px solid #E2E8F0}
.date-pill i{color:#6C63FF}
.adm-badge{display:flex;align-items:center;gap:7px;background:#fff;border:1px solid #E2E8F0;padding:4px 11px 4px 4px;border-radius:20px;font-size:12px;font-weight:600}
.adm-sm{width:24px;height:24px;background:linear-gradient(135deg,#6C63FF,#FF6584);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff}

/* Content */
.content{padding:24px;flex:1}

/* Alert */
.alert{margin:10px 24px 0;padding:11px 18px;border-radius:8px;font-size:12px;font-weight:500;display:flex;align-items:center;gap:9px;animation:sd .3s ease}
.alert-success{background:#D1FAE5;color:#065F46;border-left:4px solid #00C48C}
.alert-danger{background:#FEE2E2;color:#991B1B;border-left:4px solid #FF5B5B}
@keyframes sd{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}

/* Cards */
.card{background:#fff;border-radius:14px;padding:22px;box-shadow:0 4px 22px rgba(108,99,255,.07);border:1px solid rgba(226,232,240,.5)}
.card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
.card-title{font-size:14px;font-weight:700}
.card-sub{font-size:11px;color:#94A3B8;margin-top:2px}

/* Stat Cards */
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:18px;margin-bottom:24px}
.stat-card{background:#fff;border-radius:14px;padding:20px 22px;box-shadow:0 4px 22px rgba(108,99,255,.07);border:1px solid rgba(226,232,240,.5);display:flex;align-items:center;gap:16px;transition:.22s;position:relative;overflow:hidden}
.stat-card:hover{transform:translateY(-3px);box-shadow:0 8px 30px rgba(108,99,255,.13)}
.stat-icon{width:50px;height:50px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:21px;flex-shrink:0}
.si-purple{background:#EEF0FF;color:#6C63FF} .si-green{background:#ECFDF5;color:#00C48C}
.si-red{background:#FEF2F2;color:#FF5B5B}    .si-orange{background:#FFFBEB;color:#FFB800}
.si-blue{background:#EFF6FF;color:#3B82F6}
.stat-val{font-size:25px;font-weight:800;line-height:1}
.stat-lbl{font-size:11px;color:#64748B;margin-top:3px}
.stat-note{font-size:10px;margin-top:5px;display:flex;align-items:center;gap:3px}
.stat-note.up{color:#00C48C} .stat-note.dn{color:#FF5B5B}

/* Table */
.tbl-wrap{overflow-x:auto;border-radius:8px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
thead th{background:#F8F9FE;padding:11px 15px;text-align:left;font-weight:600;color:#64748B;font-size:10.5px;letter-spacing:.4px;text-transform:uppercase;border-bottom:1px solid #E2E8F0;white-space:nowrap}
tbody tr{border-bottom:1px solid #E2E8F0;transition:background .14s}
tbody tr:last-child{border-bottom:none}
tbody tr:hover{background:#F8F9FE}
tbody td{padding:12px 15px;vertical-align:middle}

/* Badges */
.badge{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:20px;font-size:10.5px;font-weight:600;white-space:nowrap}
.badge::before{content:'';width:5px;height:5px;border-radius:50%;background:currentColor}
.b-present{background:#ECFDF5;color:#059669} .b-absent{background:#FEF2F2;color:#DC2626}
.b-half{background:#FFFBEB;color:#D97706}    .b-leave{background:#EFF6FF;color:#3B82F6}
.b-success{background:#ECFDF5;color:#059669} .b-danger{background:#FEF2F2;color:#DC2626}
.b-warning{background:#FFFBEB;color:#D97706} .b-info{background:#EFF6FF;color:#3B82F6}
.b-purple{background:#F5F3FF;color:#7C3AED}

/* Buttons */
.btn{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:8px;font-family:'Poppins',sans-serif;font-size:12px;font-weight:600;cursor:pointer;border:none;transition:.2s;text-decoration:none;white-space:nowrap}
.btn-primary{background:#6C63FF;color:#fff} .btn-primary:hover{background:#5A52D5;box-shadow:0 4px 12px rgba(108,99,255,.35)}
.btn-success{background:#00C48C;color:#fff} .btn-success:hover{background:#00A87A}
.btn-danger{background:#FF5B5B;color:#fff}  .btn-danger:hover{background:#E04444}
.btn-outline{background:transparent;border:1.5px solid #E2E8F0;color:#64748B}
.btn-outline:hover{border-color:#6C63FF;color:#6C63FF;background:#EEF0FF}
.btn-sm{padding:5px 11px;font-size:11px}
.btn-icon{padding:7px}

/* Forms */
.fg{margin-bottom:16px}
.fg label{display:block;margin-bottom:5px;font-size:11px;font-weight:600;color:#64748B;text-transform:uppercase;letter-spacing:.4px}
.fc{width:100%;padding:9px 12px;border:1.5px solid #E2E8F0;border-radius:8px;font-family:'Poppins',sans-serif;font-size:12.5px;color:#1E293B;background:#fff;outline:none;transition:.18s}
.fc:focus{border-color:#6C63FF;box-shadow:0 0 0 3px rgba(108,99,255,.1)}
.fc::placeholder{color:#CBD5E1}
select.fc{cursor:pointer}
.form-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}

/* Search */
.search-wrap{position:relative;flex:1;max-width:300px}
.search-wrap i{position:absolute;left:11px;top:50%;transform:translateY(-50%);color:#CBD5E1;font-size:12px}
.search-wrap input{width:100%;padding:8px 12px 8px 32px;border:1.5px solid #E2E8F0;border-radius:8px;font-family:'Poppins',sans-serif;font-size:12.5px;background:#fff;outline:none;transition:.18s}
.search-wrap input:focus{border-color:#6C63FF}

/* Pagination */
.pagination{display:flex;align-items:center;gap:5px;flex-wrap:wrap}
.pg-btn{min-width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:7px;font-size:12px;font-weight:600;border:1.5px solid #E2E8F0;background:#fff;color:#64748B;cursor:pointer;transition:.18s}
.pg-btn:hover,.pg-btn.active{background:#6C63FF;color:#fff;border-color:#6C63FF}

/* Emp cell */
.emp-cell{display:flex;align-items:center;gap:9px}
.emp-av{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#6C63FF,#FF6584);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:12px;flex-shrink:0}
.emp-name{font-weight:600;color:#1E293B}
.emp-id{font-size:10.5px;color:#94A3B8}

/* Status radio */
.sradio{display:flex;gap:5px;flex-wrap:wrap}
.sradio input[type=radio]{display:none}
.sradio label{padding:3px 9px;border-radius:20px;border:1.5px solid #E2E8F0;font-size:10.5px;font-weight:600;cursor:pointer;transition:.16s;white-space:nowrap}
.sradio input[value="Present"]:checked+label{background:#ECFDF5;color:#059669;border-color:#059669}
.sradio input[value="Absent"]:checked+label{background:#FEF2F2;color:#DC2626;border-color:#DC2626}
.sradio input[value="Half Day (First Half)"]:checked+label,
.sradio input[value="Half Day (Second Half)"]:checked+label{background:#FFFBEB;color:#D97706;border-color:#D97706}
.sradio input[value="Leave"]:checked+label{background:#EFF6FF;color:#3B82F6;border-color:#3B82F6}

/* Calendar */
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}
.cal-hdr{text-align:center;font-size:10px;font-weight:700;color:#94A3B8;padding:5px 0;text-transform:uppercase;letter-spacing:.4px}
.cal-day{aspect-ratio:1;border-radius:7px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:11px;font-weight:600;transition:.16s;border:1.5px solid transparent}
.cal-day.today{border-color:#6C63FF;color:#6C63FF}
.cal-day.c-present{background:#ECFDF5;color:#059669}
.cal-day.c-absent{background:#FEF2F2;color:#DC2626}
.cal-day.c-half{background:#FFFBEB;color:#D97706}
.cal-day.c-leave{background:#EFF6FF;color:#3B82F6}
.cal-day.c-wknd{background:#F8F9FE;color:#CBD5E1}
.cal-dot{width:4px;height:4px;border-radius:50%;background:currentColor;margin-top:2px}

/* Salary Slip */
.slip-wrap{max-width:740px;margin:0 auto}
.slip-hdr{background:linear-gradient(135deg,#6C63FF,#5A52D5);color:#fff;padding:30px 34px;border-radius:14px 14px 0 0}
.slip-body{background:#fff;padding:30px 34px;border-radius:0 0 14px 14px;border:1px solid #E2E8F0;border-top:none}
.slip-sec{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.9px;color:#94A3B8;margin-bottom:10px;padding-bottom:7px;border-bottom:1px solid #E2E8F0}
.slip-row{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid #F0F2FF;font-size:12.5px}
.slip-row:last-child{border-bottom:none}
.slip-total{font-weight:700;font-size:13px;color:#1E293B}
.slip-net{background:#EEF0FF;border-radius:10px;padding:15px 18px;margin-top:14px;display:flex;justify-content:space-between;align-items:center}
.slip-net-lbl{font-weight:700;color:#6C63FF;font-size:13px}
.slip-net-val{font-size:21px;font-weight:800;color:#6C63FF}

/* Quick action grid */
.qa-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.qa-item{text-align:center;padding:16px 10px;border-radius:11px;transition:.2s;cursor:pointer}
.qa-item:hover{transform:translateY(-2px)}
.qa-item i{font-size:20px;margin-bottom:7px;display:block}
.qa-item span{font-size:11px;font-weight:600}

/* Chart */
.chart-box{position:relative;height:210px}

/* Util */
.flex{display:flex}.flex-center{display:flex;align-items:center}.gap-8{gap:8px}.gap-12{gap:12px}
.mt-4{margin-top:4px}.mt-8{margin-top:8px}.mt-16{margin-top:16px}.mt-20{margin-top:20px}
.mb-16{margin-bottom:16px}.mb-20{margin-bottom:20px}
.text-sm{font-size:11.5px}.text-muted{color:#64748B}.text-right{text-align:right}
.fw-bold{font-weight:700}.w-full{width:100%}
.row-2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.row-3{display:grid;grid-template-columns:2fr 1fr;gap:18px}
code{background:#F8F9FE;padding:2px 7px;border-radius:4px;font-size:11px;color:#6C63FF}

@media(max-width:768px){
  .sidebar{transform:translateX(-100%)}.sidebar.mob-open{transform:translateX(0)}
  .main-content{margin-left:0!important}.mob-btn{display:flex!important}
  .content{padding:14px}.topbar{padding:0 14px}
  .stats-grid{grid-template-columns:repeat(2,1fr)}.row-2,.row-3{grid-template-columns:1fr}
}
@media print{
  .sidebar,.topbar,.btn,.alert,.no-print{display:none!important}
  .main-content{margin-left:0!important}.content{padding:0}
}
</style>
"""

# ─── SHARED JS ────────────────────────────────────────────────────────────────
JS = """
<script>
function toggleSidebar(){
  const s=document.getElementById('sb'),m=document.getElementById('mc'),ic=document.getElementById('tg-ic');
  s.classList.toggle('collapsed');m.classList.toggle('expanded');
  ic.className=s.classList.contains('collapsed')?'fas fa-chevron-right':'fas fa-chevron-left';
  localStorage.setItem('sc',s.classList.contains('collapsed'));
}
function mobMenu(){document.getElementById('sb').classList.toggle('mob-open')}
(function(){
  if(localStorage.getItem('sc')==='true'){
    const s=document.getElementById('sb'),m=document.getElementById('mc'),ic=document.getElementById('tg-ic');
    if(s){s.classList.add('collapsed');m?.classList.add('expanded');if(ic)ic.className='fas fa-chevron-right';}
  }
  const el=document.getElementById('cur-date');
  if(el){const o={weekday:'short',year:'numeric',month:'short',day:'numeric'};el.textContent=new Date().toLocaleDateString('en-IN',o);}
  setTimeout(()=>{document.querySelectorAll('.alert').forEach(a=>{a.style.transition='opacity .4s';a.style.opacity=0;setTimeout(()=>a.remove(),400);});},4000);
})();
function confirmDel(fid,name){if(confirm('Remove "'+name+'" ? This cannot be undone.')){document.getElementById(fid).submit();}}
function printSlip(){window.print();}
function markAll(status){document.querySelectorAll('input[type=radio]').forEach(r=>{if(r.value===status)r.checked=true;});}
</script>
"""

# ─── LAYOUT wrapper ───────────────────────────────────────────────────────────
def _layout(body: str, active: str, admin_username: str,
            page_title: str, breadcrumb: str,
            success: str = "", error: str = "") -> str:

    alert = ""
    if success:
        alert = f'<div class="alert alert-success"><i class="fas fa-check-circle"></i> {success}</div>'
    elif error:
        alert = f'<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> {error}</div>'

    def nav(href, icon, label, key):
        cls = "nav-item active" if active == key else "nav-item"
        return f'<a href="{href}" class="{cls}"><i class="fas fa-{icon}"></i><span>{label}</span></a>'

    av = admin_username[0].upper()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{page_title} – AttendPro</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
{CSS}
</head>
<body>
<aside class="sidebar" id="sb">
  <div class="sidebar-header">
    <div class="brand">
      <div class="brand-icon"><i class="fas fa-building"></i></div>
      <div class="brand-text"><span class="brand-name">AttendPro</span><span class="brand-sub">HRMS System</span></div>
    </div>
    <button class="toggle-btn" onclick="toggleSidebar()"><i class="fas fa-chevron-left" id="tg-ic"></i></button>
  </div>
  <nav class="sidebar-nav">
    <div class="nav-section">Main</div>
    {nav('/dashboard','th-large','Dashboard','dashboard')}
    {nav('/employees','users','Employees','employees')}
    <div class="nav-section">Operations</div>
    {nav('/attendance','calendar-check','Mark Attendance','attendance')}
    {nav('/attendance/history','history','Att. History','attendance-history')}
    <div class="nav-section">Payroll</div>
    {nav('/salary','money-bill-wave','Salary','salary')}
  </nav>
  <div class="sidebar-footer">
    <div class="adm-info">
      <div class="adm-avatar">{av}</div>
      <div class="adm-details"><span class="adm-name">{admin_username}</span><span class="adm-role">Administrator</span></div>
    </div>
    <a href="/logout" class="logout-a" title="Logout"><i class="fas fa-sign-out-alt"></i></a>
  </div>
</aside>
<main class="main-content" id="mc">
  <header class="topbar">
    <div class="topbar-left">
      <button style="display:none;background:none;border:none;cursor:pointer;font-size:17px;color:#64748B" class="mob-btn" onclick="mobMenu()"><i class="fas fa-bars"></i></button>
      <div class="pg-title"><h1>{page_title}</h1><nav class="breadcrumb">{breadcrumb}</nav></div>
    </div>
    <div class="topbar-right">
      <div class="date-pill"><i class="fas fa-calendar-alt"></i><span id="cur-date"></span></div>
      <div class="adm-badge"><div class="adm-sm">{av}</div><span>{admin_username}</span></div>
    </div>
  </header>
  {alert}
  <div class="content">{body}</div>
</main>
{JS}
</body></html>"""


# ─── LOGIN PAGE ───────────────────────────────────────────────────────────────
LOGIN_TMPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Login – AttendPro HRMS</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
{{ CSS }}
<style>
body{display:flex;min-height:100vh}
.login-left{flex:1;background:#0F172A;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:50px 36px;position:relative;overflow:hidden}
.login-left::before{content:'';position:absolute;width:380px;height:380px;background:radial-gradient(circle,rgba(108,99,255,.25) 0%,transparent 70%);top:-80px;right:-80px;border-radius:50%}
.login-left::after{content:'';position:absolute;width:280px;height:280px;background:radial-gradient(circle,rgba(255,101,132,.15) 0%,transparent 70%);bottom:-60px;left:-60px;border-radius:50%}
.login-illo{position:relative;z-index:1;text-align:center}
.login-illo .big-i{font-size:70px;color:#6C63FF;opacity:.85;margin-bottom:22px;filter:drop-shadow(0 8px 22px rgba(108,99,255,.4))}
.login-illo h2{font-size:24px;font-weight:800;color:#fff;margin-bottom:8px}
.login-illo p{color:rgba(255,255,255,.4);font-size:13px;max-width:260px}
.login-right{width:440px;display:flex;align-items:center;justify-content:center;padding:36px}
.login-box{width:100%}
.login-logo{display:flex;align-items:center;gap:11px;margin-bottom:30px}
.login-logo-icon{width:42px;height:42px;background:#6C63FF;border-radius:11px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:19px}
.login-logo h1{font-size:19px;font-weight:800}
.login-logo span{font-size:10px;color:#94A3B8}
.login-title{font-size:22px;font-weight:800;margin-bottom:5px}
.login-sub{font-size:12.5px;color:#64748B;margin-bottom:28px}
.login-footer{margin-top:20px;text-align:center;font-size:11.5px;color:#94A3B8}
@media(max-width:768px){.login-left{display:none}.login-right{width:100%}}
</style>
</head>
<body>
<div class="login-left">
  <div class="login-illo">
    <div class="big-i"><i class="fas fa-building"></i></div>
    <h2>Streamline HR Operations</h2>
    <p>Attendance tracking, salary management and employee records — all in one place.</p>
    <div style="margin-top:30px;display:flex;gap:14px;justify-content:center;flex-wrap:wrap">
      <div style="background:rgba(255,255,255,.06);border-radius:11px;padding:10px 18px;text-align:center">
        <div style="font-size:20px;font-weight:800;color:#fff">99.9%</div>
        <div style="font-size:10px;color:rgba(255,255,255,.3);margin-top:2px">Uptime</div>
      </div>
      <div style="background:rgba(255,255,255,.06);border-radius:11px;padding:10px 18px;text-align:center">
        <div style="font-size:20px;font-weight:800;color:#fff">∞</div>
        <div style="font-size:10px;color:rgba(255,255,255,.3);margin-top:2px">Employees</div>
      </div>
      <div style="background:rgba(255,255,255,.06);border-radius:11px;padding:10px 18px;text-align:center">
        <div style="font-size:20px;font-weight:800;color:#fff">Real-time</div>
        <div style="font-size:10px;color:rgba(255,255,255,.3);margin-top:2px">Analytics</div>
      </div>
    </div>
  </div>
</div>
<div class="login-right">
  <div class="login-box">
    <div class="login-logo">
      <div class="login-logo-icon"><i class="fas fa-building"></i></div>
      <div><h1>AttendPro</h1><span>HRMS System v1.0</span></div>
    </div>
    <h2 class="login-title">Welcome back 👋</h2>
    <p class="login-sub">Sign in to access the admin dashboard</p>
    {% if error %}<div class="alert alert-danger" style="margin:0 0 18px;border-radius:8px"><i class="fas fa-exclamation-circle"></i> {{ error }}</div>{% endif %}
    <form method="POST" action="/login">
      <div class="fg">
        <label>Username</label>
        <div style="position:relative">
          <i class="fas fa-user" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#CBD5E1;font-size:12px"></i>
          <input type="text" name="username" class="fc" style="padding-left:34px" placeholder="Enter username" value="admin" required/>
        </div>
      </div>
      <div class="fg">
        <label>Password</label>
        <div style="position:relative">
          <i class="fas fa-lock" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#CBD5E1;font-size:12px"></i>
          <input type="password" name="password" id="pwd" class="fc" style="padding-left:34px;padding-right:38px" placeholder="Enter password" value="admin123" required/>
          <button type="button" onclick="togglePwd()" style="position:absolute;right:11px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:#CBD5E1"><i class="fas fa-eye" id="pwd-eye"></i></button>
        </div>
      </div>
      <button type="submit" class="btn btn-primary w-full" style="justify-content:center;padding:11px;font-size:13px;margin-top:4px">
        <i class="fas fa-sign-in-alt"></i> Sign In
      </button>
    </form>
    <div class="login-footer">Default credentials: <strong>admin</strong> / <strong>admin123</strong></div>
  </div>
</div>
<script>function togglePwd(){const i=document.getElementById('pwd'),e=document.getElementById('pwd-eye');i.type=i.type==='password'?'text':'password';e.className=i.type==='password'?'fas fa-eye':'fas fa-eye-slash';}</script>
</body></html>"""


# ─── DASHBOARD ────────────────────────────────────────────────────────────────
DASHBOARD_TMPL = """
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-icon si-purple"><i class="fas fa-users"></i></div>
    <div><div class="stat-val">{{ total_employees }}</div><div class="stat-lbl">Total Employees</div><div class="stat-note up"><i class="fas fa-check-circle"></i> Active staff</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon si-green"><i class="fas fa-user-check"></i></div>
    <div><div class="stat-val">{{ today_summary.present }}</div><div class="stat-lbl">Present Today</div><div class="stat-note up"><i class="fas fa-chart-line"></i> {{ today_summary.rate }}% rate</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon si-red"><i class="fas fa-user-times"></i></div>
    <div><div class="stat-val">{{ today_summary.absent }}</div><div class="stat-lbl">Absent Today</div><div class="stat-note dn"><i class="fas fa-minus"></i> Incl. unmarked</div></div>
  </div>
  <div class="stat-card">
    <div class="stat-icon si-orange"><i class="fas fa-rupee-sign"></i></div>
    <div><div class="stat-val">₹{{ "{:,.0f}".format(total_payroll) }}</div><div class="stat-lbl">Monthly Payroll</div><div class="stat-note up"><i class="fas fa-calendar"></i> {{ month_name }} {{ year }}</div></div>
  </div>
</div>

<div class="row-2 mb-20">
  <div class="card">
    <div class="card-header"><div><div class="card-title">Attendance Trend</div><div class="card-sub">Last 7 working days</div></div><span class="badge b-info">Weekly</span></div>
    <div class="chart-box"><canvas id="barChart"></canvas></div>
  </div>
  <div class="card">
    <div class="card-header"><div><div class="card-title">Today's Breakdown</div><div class="card-sub">{{ today_str }}</div></div></div>
    <div style="display:flex;align-items:center;gap:20px">
      <div style="flex:1;max-width:160px"><canvas id="donut" height="160"></canvas></div>
      <div style="flex:1;display:flex;flex-direction:column;gap:9px">
        <div style="display:flex;align-items:center;justify-content:space-between;font-size:12.5px"><div style="display:flex;align-items:center;gap:7px"><div style="width:9px;height:9px;border-radius:3px;background:#00C48C"></div>Present</div><strong>{{ today_summary.present }}</strong></div>
        <div style="display:flex;align-items:center;justify-content:space-between;font-size:12.5px"><div style="display:flex;align-items:center;gap:7px"><div style="width:9px;height:9px;border-radius:3px;background:#FF5B5B"></div>Absent</div><strong>{{ today_summary.absent }}</strong></div>
        <div style="display:flex;align-items:center;justify-content:space-between;font-size:12.5px"><div style="display:flex;align-items:center;gap:7px"><div style="width:9px;height:9px;border-radius:3px;background:#FFB800"></div>Half Day</div><strong>{{ today_summary.half_day }}</strong></div>
        <div style="border-top:1px solid #E2E8F0;padding-top:9px;margin-top:2px"><div style="font-size:11px;color:#64748B">Attendance Rate</div><div style="font-size:21px;font-weight:800;color:#6C63FF">{{ today_summary.rate }}%</div></div>
      </div>
    </div>
  </div>
</div>

<div class="row-3">
  <div class="card">
    <div class="card-header"><div class="card-title">Quick Actions</div></div>
    <div class="qa-grid">
      <a href="/attendance" class="qa-item" style="background:#EEF0FF;color:#6C63FF"><i class="fas fa-calendar-check"></i><span>Mark Attendance</span></a>
      <a href="/employees/add" class="qa-item" style="background:#ECFDF5;color:#00C48C"><i class="fas fa-user-plus"></i><span>Add Employee</span></a>
      <a href="/salary" class="qa-item" style="background:#FFFBEB;color:#FFB800"><i class="fas fa-money-bill-wave"></i><span>Process Salary</span></a>
      <a href="/attendance/history" class="qa-item" style="background:#EFF6FF;color:#3B82F6"><i class="fas fa-history"></i><span>View History</span></a>
      <a href="/employees" class="qa-item" style="background:#FDF2FF;color:#9333EA"><i class="fas fa-users-cog"></i><span>Manage Staff</span></a>
      <a href="/salary" class="qa-item" style="background:#FFF1F2;color:#FF6584"><i class="fas fa-file-invoice-dollar"></i><span>Salary Slips</span></a>
    </div>
  </div>
  <div class="card">
    <div class="card-header"><div class="card-title">Payroll Summary</div><span class="badge b-warning">{{ month_name }}</span></div>
    <div style="display:flex;flex-direction:column;gap:11px">
      <div style="padding:13px;background:#F8F9FE;border-radius:9px">
        <div style="font-size:10px;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:.4px">Total Payroll Est.</div>
        <div style="font-size:22px;font-weight:800;margin-top:3px">₹{{ "{:,.0f}".format(total_payroll) }}</div>
      </div>
      {% if monthly_processed > 0 %}
      <div style="padding:13px;background:#ECFDF5;border-radius:9px">
        <div style="font-size:10px;color:#059669;font-weight:600;text-transform:uppercase;letter-spacing:.4px">Processed This Month</div>
        <div style="font-size:22px;font-weight:800;color:#059669;margin-top:3px">₹{{ "{:,.0f}".format(monthly_processed) }}</div>
      </div>
      {% else %}
      <div style="padding:13px;background:#FFFBEB;border-radius:9px;text-align:center">
        <i class="fas fa-clock" style="color:#FFB800;font-size:18px;margin-bottom:5px"></i>
        <div style="font-size:12px;color:#D97706;font-weight:600">No salaries processed yet</div>
      </div>
      {% endif %}
      <a href="/salary" class="btn btn-primary" style="justify-content:center">
        <i class="fas fa-arrow-right"></i> Go to Payroll
      </a>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const trend={{ trend_json }};
new Chart(document.getElementById('barChart'),{type:'bar',data:{labels:trend.map(d=>d.date),datasets:[{label:'Present',data:trend.map(d=>d.present),backgroundColor:'#00C48C',borderRadius:5,borderSkipped:false},{label:'Absent',data:trend.map(d=>d.absent),backgroundColor:'#FF5B5B',borderRadius:5,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{family:'Poppins',size:10}}}},scales:{x:{stacked:true,grid:{display:false},ticks:{font:{family:'Poppins',size:10}}},y:{stacked:true,beginAtZero:true,grid:{color:'#F0F2FF'},ticks:{font:{family:'Poppins',size:10}}}}}});
new Chart(document.getElementById('donut'),{type:'doughnut',data:{labels:['Present','Absent','Half Day'],datasets:[{data:[{{ today_summary.present }},{{ today_summary.absent }},{{ today_summary.half_day }}],backgroundColor:['#00C48C','#FF5B5B','#FFB800'],borderWidth:0,hoverOffset:5}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},cutout:'70%'}});
</script>
"""


# ─── EMPLOYEES LIST ───────────────────────────────────────────────────────────
EMPLOYEE_LIST_TMPL = """
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;flex-wrap:wrap;gap:10px">
  <div><div style="font-size:15px;font-weight:700">Employee Directory</div><div class="text-sm text-muted mt-4">{{ total }} total employees</div></div>
  <div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap">
    <form method="GET" action="/employees" style="display:flex;gap:7px;align-items:center">
      <div class="search-wrap"><i class="fas fa-search"></i><input type="text" name="search" placeholder="Search name, ID, role…" value="{{ search }}"/></div>
      <button type="submit" class="btn btn-outline btn-sm"><i class="fas fa-search"></i></button>
    </form>
    <a href="/employees/add" class="btn btn-primary"><i class="fas fa-user-plus"></i> Add Employee</a>
  </div>
</div>

<div class="card">
  <div class="tbl-wrap">
    <table>
      <thead><tr><th>Employee</th><th>ID</th><th>Department</th><th>Role</th><th>Gross Salary</th><th>Joining</th><th>Status</th><th>Actions</th></tr></thead>
      <tbody>
      {% for emp in employees %}
      <tr>
        <td><div class="emp-cell"><div class="emp-av">{{ emp.name[0]|upper }}</div><div><div class="emp-name">{{ emp.name }}</div><div class="emp-id">{{ emp.email or 'No email' }}</div></div></div></td>
        <td><code>{{ emp.employee_id }}</code></td>
        <td>{{ emp.department or '—' }}</td>
        <td>{{ emp.role or '—' }}</td>
        <td><strong>₹{{ "{:,.0f}".format(emp.gross_salary) }}</strong></td>
        <td>{{ emp.joining_date.strftime('%d %b %Y') if emp.joining_date else '—' }}</td>
        <td>{% if emp.is_active %}<span class="badge b-success">Active</span>{% else %}<span class="badge b-danger">Inactive</span>{% endif %}</td>
        <td>
          <div style="display:flex;gap:5px">
            <a href="/employees/{{ emp.id }}/edit" class="btn btn-outline btn-sm btn-icon" title="Edit"><i class="fas fa-edit"></i></a>
            <form id="del-{{ emp.id }}" method="POST" action="/employees/{{ emp.id }}/delete" style="display:inline">
              <button type="button" class="btn btn-danger btn-sm btn-icon" onclick="confirmDel('del-{{ emp.id }}','{{ emp.name }}')"><i class="fas fa-trash"></i></button>
            </form>
          </div>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="8" style="text-align:center;padding:36px;color:#94A3B8"><i class="fas fa-users" style="font-size:28px;margin-bottom:8px;display:block"></i>No employees found{% if search %} for "{{ search }}"{% endif %}</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
  {% if total_pages > 1 %}
  <div style="padding:14px 18px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid #E2E8F0;flex-wrap:wrap;gap:10px">
    <span class="text-sm text-muted">Showing {{ (page-1)*per_page+1 }}–{{ [page*per_page,total]|min }} of {{ total }}</span>
    <div class="pagination">
      {% if page > 1 %}<a href="?page={{ page-1 }}&search={{ search }}" class="pg-btn"><i class="fas fa-chevron-left"></i></a>{% endif %}
      {% for p in range(1,total_pages+1) %}<a href="?page={{ p }}&search={{ search }}" class="pg-btn {{ 'active' if p==page else '' }}">{{ p }}</a>{% endfor %}
      {% if page < total_pages %}<a href="?page={{ page+1 }}&search={{ search }}" class="pg-btn"><i class="fas fa-chevron-right"></i></a>{% endif %}
    </div>
  </div>
  {% endif %}
</div>
"""


# ─── EMPLOYEE FORM ────────────────────────────────────────────────────────────
EMPLOYEE_FORM_TMPL = """
<div style="max-width:700px">
  <div class="card">
    <div class="card-header">
      <div><div class="card-title">{{ 'Update Employee Details' if employee else 'New Employee' }}</div><div class="card-sub">{{ 'Modify information below' if employee else 'Fill in details to register a new employee' }}</div></div>
      {% if employee %}<div class="emp-av" style="width:38px;height:38px;font-size:15px">{{ employee.name[0]|upper }}</div>{% endif %}
    </div>
    {% if form_error %}<div class="alert alert-danger" style="margin:0 0 16px;border-radius:8px"><i class="fas fa-exclamation-circle"></i> {{ form_error }}</div>{% endif %}
    <form method="POST" action="{{ '/employees/'+employee.id|string+'/edit' if employee else '/employees/add' }}">
      <div class="form-grid">
        <div class="fg"><label>Employee ID *</label>
          <input type="text" name="employee_id" class="fc" placeholder="EMP001"
            value="{{ employee.employee_id if employee else (fd.employee_id if fd else '') }}"
            {{ 'readonly style="background:#F8F9FE;cursor:not-allowed"' if employee else '' }} required/>
        </div>
        <div class="fg"><label>Full Name *</label>
          <input type="text" name="name" class="fc" placeholder="Arjun Sharma"
            value="{{ employee.name if employee else (fd.name if fd else '') }}" required/>
        </div>
        <div class="fg"><label>Email Address</label>
          <input type="email" name="email" class="fc" placeholder="employee@company.com"
            value="{{ employee.email or '' if employee else '' }}"/>
        </div>
        <div class="fg"><label>Phone</label>
          <input type="tel" name="phone" class="fc" placeholder="9876543210"
            value="{{ employee.phone or '' if employee else '' }}"/>
        </div>
        <div class="fg"><label>Role / Designation</label>
          <input type="text" name="role" class="fc" placeholder="Senior Developer"
            value="{{ employee.role or '' if employee else (fd.role if fd else '') }}"/>
        </div>
        <div class="fg"><label>Department</label>
          <select name="department" class="fc">
            <option value="">Select department</option>
            {% for dept in ['Engineering','Design','Product','Marketing','Sales','Human Resources','Finance','Operations','Analytics','Infrastructure','Legal'] %}
            <option value="{{ dept }}" {{ 'selected' if (employee and employee.department==dept) or (fd and fd.department==dept) else '' }}>{{ dept }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="fg"><label>Gross Salary (Monthly) *</label>
          <div style="position:relative">
            <span style="position:absolute;left:11px;top:50%;transform:translateY(-50%);color:#94A3B8;font-weight:700">₹</span>
            <input type="number" name="gross_salary" id="gs" class="fc" style="padding-left:26px" placeholder="75000"
              value="{{ employee.gross_salary if employee else (fd.gross_salary if fd else '') }}" min="1" required/>
          </div>
        </div>
        <div class="fg"><label>Joining Date</label>
          <input type="date" name="joining_date" class="fc"
            value="{{ employee.joining_date.isoformat() if employee and employee.joining_date else '' }}"/>
        </div>
      </div>
      <div id="sal-preview" style="display:none;background:#EEF0FF;border-radius:9px;padding:14px;margin-bottom:16px">
        <div style="font-size:11px;font-weight:700;color:#6C63FF;margin-bottom:10px;text-transform:uppercase;letter-spacing:.5px"><i class="fas fa-calculator"></i> Salary Breakdown Preview</div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px" id="sal-grid"></div>
      </div>
      <div style="display:flex;gap:10px;margin-top:6px">
        <button type="submit" class="btn btn-primary"><i class="fas fa-{{ 'save' if employee else 'user-plus' }}"></i> {{ 'Update Employee' if employee else 'Add Employee' }}</button>
        <a href="/employees" class="btn btn-outline"><i class="fas fa-times"></i> Cancel</a>
      </div>
    </form>
  </div>
</div>
<script>
const gs=document.getElementById('gs'),pr=document.getElementById('sal-preview'),gr=document.getElementById('sal-grid');
function upd(){
  const g=parseFloat(gs.value)||0;if(g<=0){pr.style.display='none';return;}pr.style.display='block';
  const b=(g*.40).toFixed(0),h=(g*.20).toFixed(0),t=(g*.10).toFixed(0),m=(g*.05).toFixed(0),s=(g-b-h-t-m).toFixed(0),pf=(b*.12).toFixed(0),esi=g<=21000?(g*.0075).toFixed(0):0,net=(g-pf-esi).toFixed(0);
  const f=n=>'₹'+parseInt(n).toLocaleString('en-IN');
  gr.innerHTML=`<div style="font-size:11px"><span style="color:#94A3B8;display:block;margin-bottom:2px">Basic (40%)</span><strong>${f(b)}</strong></div><div style="font-size:11px"><span style="color:#94A3B8;display:block;margin-bottom:2px">HRA (20%)</span><strong>${f(h)}</strong></div><div style="font-size:11px"><span style="color:#94A3B8;display:block;margin-bottom:2px">Transport</span><strong>${f(t)}</strong></div><div style="font-size:11px"><span style="color:#94A3B8;display:block;margin-bottom:2px">PF Deduction</span><strong style="color:#FF5B5B">-${f(pf)}</strong></div><div style="font-size:11px"><span style="color:#94A3B8;display:block;margin-bottom:2px">ESI</span><strong style="color:#FF5B5B">-${f(esi)}</strong></div><div style="font-size:11px"><span style="color:#6C63FF;display:block;margin-bottom:2px;font-weight:700">Net (est.)</span><strong style="color:#6C63FF">${f(net)}</strong></div>`;
}
gs.addEventListener('input',upd);upd();
</script>
"""


# ─── ATTENDANCE MARK ──────────────────────────────────────────────────────────
ATTENDANCE_MARK_TMPL = """
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:10px">
  <div><div style="font-size:15px;font-weight:700">Daily Attendance</div><div class="text-sm text-muted mt-4">{{ employees|length }} employees</div></div>
  <div style="display:flex;align-items:center;gap:9px;flex-wrap:wrap">
    <form method="GET" style="display:flex;align-items:center;gap:7px">
      <input type="date" name="selected_date" class="fc" style="width:175px" value="{{ selected_date }}" max="{{ today }}" onchange="this.form.submit()"/>
    </form>
    <a href="/attendance/history" class="btn btn-outline"><i class="fas fa-history"></i> History</a>
  </div>
</div>

<div style="background:#EEF0FF;border-radius:9px;padding:12px 18px;margin-bottom:18px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px">
  <div style="display:flex;align-items:center;gap:11px">
    <div style="width:40px;height:40px;background:#6C63FF;border-radius:9px;display:flex;align-items:center;justify-content:center;color:#fff"><i class="fas fa-calendar-day" style="font-size:16px"></i></div>
    <div><div style="font-weight:700;color:#6C63FF">{{ selected_date_fmt }}</div><div style="font-size:11px;color:#64748B">{{ already_marked }} already marked</div></div>
  </div>
  <div style="display:flex;gap:7px">
    <button type="button" onclick="markAll('Present')" class="btn btn-success btn-sm"><i class="fas fa-check"></i> All Present</button>
    <button type="button" onclick="markAll('Absent')" class="btn btn-danger btn-sm"><i class="fas fa-times"></i> All Absent</button>
  </div>
</div>

<form method="POST" action="/attendance/bulk-mark">
  <input type="hidden" name="attendance_date" value="{{ selected_date }}"/>
  <div class="card">
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Employee</th><th>Role</th><th>Status</th><th>Check In</th><th>Check Out</th></tr></thead>
        <tbody>
        {% for emp in employees %}
        {% set rec = records_map.get(emp.id) %}
        <tr>
          <td><div class="emp-cell"><div class="emp-av">{{ emp.name[0]|upper }}</div><div><div class="emp-name">{{ emp.name }}</div><div class="emp-id">{{ emp.employee_id }}</div></div></div></td>
          <td><span class="text-sm text-muted">{{ emp.role or '—' }}</span></td>
          <td>
            <div class="sradio">
              {% for st, lbl in [('Present','✓ Present'),('Absent','✗ Absent'),('Half Day (First Half)','½ First'),('Half Day (Second Half)','½ Second'),('Leave','🏖 Leave')] %}
              <input type="radio" name="status_{{ emp.id }}" id="s_{{ emp.id }}_{{ loop.index }}" value="{{ st }}"
                {{ 'checked' if (rec and rec.status.value==st) or (not rec and st=='Present') else '' }}/>
              <label for="s_{{ emp.id }}_{{ loop.index }}">{{ lbl }}</label>
              {% endfor %}
            </div>
          </td>
          <td><input type="time" name="check_in_{{ emp.id }}" class="fc" style="width:105px" value="{{ rec.check_in or '09:00' if rec else '09:00' }}"/></td>
          <td><input type="time" name="check_out_{{ emp.id }}" class="fc" style="width:105px" value="{{ rec.check_out or '18:00' if rec else '18:00' }}"/></td>
        </tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
    <div style="padding:14px 18px;border-top:1px solid #E2E8F0;display:flex;align-items:center;justify-content:flex-end;gap:9px">
      <a href="/attendance" class="btn btn-outline"><i class="fas fa-undo"></i> Reset</a>
      <button type="submit" class="btn btn-primary" style="min-width:150px"><i class="fas fa-save"></i> Save Attendance</button>
    </div>
  </div>
</form>
"""


# ─── ATTENDANCE HISTORY ───────────────────────────────────────────────────────
ATTENDANCE_HISTORY_TMPL = """
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;flex-wrap:wrap;gap:10px">
  <div style="font-size:15px;font-weight:700">Attendance History</div>
  <form method="GET" style="display:flex;gap:7px;align-items:center;flex-wrap:wrap">
    <select name="employee_id" class="fc" style="width:195px" onchange="this.form.submit()">
      <option value="">Select Employee</option>
      {% for emp in employees %}<option value="{{ emp.id }}" {{ 'selected' if employee_id and employee_id==emp.id else '' }}>{{ emp.name }} ({{ emp.employee_id }})</option>{% endfor %}
    </select>
    <select name="month" class="fc" style="width:130px">
      {% for m,mn in [(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December')] %}
      <option value="{{ m }}" {{ 'selected' if m==month else '' }}>{{ mn }}</option>{% endfor %}
    </select>
    <select name="year" class="fc" style="width:95px">
      {% for y in [2023,2024,2025,2026] %}<option value="{{ y }}" {{ 'selected' if y==year else '' }}>{{ y }}</option>{% endfor %}
    </select>
    <button type="submit" class="btn btn-primary btn-sm"><i class="fas fa-search"></i></button>
  </form>
</div>

{% if selected_employee %}
<div class="stats-grid" style="grid-template-columns:repeat(6,1fr);margin-bottom:18px">
  <div class="stat-card" style="padding:14px"><div class="stat-icon si-green" style="width:36px;height:36px;font-size:14px;border-radius:9px"><i class="fas fa-check"></i></div><div><div class="stat-val" style="font-size:18px">{{ stats.present }}</div><div class="stat-lbl">Present</div></div></div>
  <div class="stat-card" style="padding:14px"><div class="stat-icon si-red" style="width:36px;height:36px;font-size:14px;border-radius:9px"><i class="fas fa-times"></i></div><div><div class="stat-val" style="font-size:18px">{{ stats.absent }}</div><div class="stat-lbl">Absent</div></div></div>
  <div class="stat-card" style="padding:14px"><div class="stat-icon si-orange" style="width:36px;height:36px;font-size:14px;border-radius:9px"><i class="fas fa-adjust"></i></div><div><div class="stat-val" style="font-size:18px">{{ stats.half_days }}</div><div class="stat-lbl">Half Days</div></div></div>
  <div class="stat-card" style="padding:14px"><div class="stat-icon si-purple" style="width:36px;height:36px;font-size:14px;border-radius:9px"><i class="fas fa-umbrella-beach"></i></div><div><div class="stat-val" style="font-size:18px">{{ stats.leaves }}</div><div class="stat-lbl">Leaves</div></div></div>
  <div class="stat-card" style="padding:14px"><div class="stat-icon si-blue" style="width:36px;height:36px;font-size:14px;border-radius:9px"><i class="fas fa-calculator"></i></div><div><div class="stat-val" style="font-size:18px">{{ "%.1f"|format(stats.effective_present) }}</div><div class="stat-lbl">Eff. Days</div></div></div>
  <div class="stat-card" style="padding:14px;background:linear-gradient(135deg,#6C63FF,#FF6584);border:none">
    <div style="width:36px;height:36px;background:rgba(255,255,255,.2);border-radius:9px;display:flex;align-items:center;justify-content:center"><i class="fas fa-percentage" style="color:#fff;font-size:14px"></i></div>
    <div><div style="font-size:18px;font-weight:800;color:#fff">{% if records %}{{ "%.0f"|format(stats.effective_present/records|length*100) }}%{% else %}—{% endif %}</div><div style="font-size:11px;color:rgba(255,255,255,.7)">Rate</div></div>
  </div>
</div>

<div class="row-2">
  <!-- Calendar -->
  <div class="card">
    <div class="card-header" style="margin-bottom:14px"><div class="card-title">{{ month_name }} {{ year }}</div></div>
    <div style="display:flex;flex-wrap:wrap;gap:7px;margin-bottom:13px">
      <div style="display:flex;align-items:center;gap:4px;font-size:10.5px"><div style="width:9px;height:9px;border-radius:3px;background:#ECFDF5;border:1px solid #059669"></div>Present</div>
      <div style="display:flex;align-items:center;gap:4px;font-size:10.5px"><div style="width:9px;height:9px;border-radius:3px;background:#FEF2F2;border:1px solid #DC2626"></div>Absent</div>
      <div style="display:flex;align-items:center;gap:4px;font-size:10.5px"><div style="width:9px;height:9px;border-radius:3px;background:#FFFBEB;border:1px solid #D97706"></div>Half</div>
      <div style="display:flex;align-items:center;gap:4px;font-size:10.5px"><div style="width:9px;height:9px;border-radius:3px;background:#EFF6FF;border:1px solid #3B82F6"></div>Leave</div>
    </div>
    <div class="cal-grid">
      {% for day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'] %}<div class="cal-hdr">{{ day }}</div>{% endfor %}
      {% for week in calendar_grid %}
        {% for day in week %}
          {% if day == 0 %}<div></div>
          {% else %}
            {% set dk = "%04d-%02d-%02d"|format(year,month,day) %}
            {% set info = cal_data.get(dk) %}
            <div class="cal-day
              {{ 'c-present' if info and 'Present'==info.status else '' }}
              {{ 'c-absent' if info and 'Absent'==info.status else '' }}
              {{ 'c-half' if info and 'Half' in info.status else '' }}
              {{ 'c-leave' if info and 'Leave'==info.status else '' }}
              {{ 'c-wknd' if loop.index0 >= 5 else '' }}
            " title="{{ dk }}{% if info %} · {{ info.status }}{% if info.check_in %} · In:{{ info.check_in }}{% endif %}{% endif %}">
              {{ day }}<div class="cal-dot"></div>
            </div>
          {% endif %}
        {% endfor %}
      {% endfor %}
    </div>
  </div>

  <!-- Records -->
  <div class="card">
    <div class="card-header">
      <div><div class="card-title">{{ selected_employee.name }}</div><div class="card-sub">{{ selected_employee.employee_id }} · {{ selected_employee.role or 'Employee' }}</div></div>
      <a href="/salary?month={{ month }}&year={{ year }}" class="btn btn-outline btn-sm"><i class="fas fa-calculator"></i> Salary</a>
    </div>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Date</th><th>Day</th><th>Status</th><th>In</th><th>Out</th></tr></thead>
        <tbody>
        {% for rec in records %}
        {% set s = rec.status.value if rec.status.value is defined else rec.status|string %}
        <tr>
          <td><strong>{{ rec.date.strftime('%d %b') }}</strong></td>
          <td class="text-sm text-muted">{{ rec.date.strftime('%a') }}</td>
          <td>
            {% if 'Present'==s %}<span class="badge b-present">Present</span>
            {% elif 'Absent'==s %}<span class="badge b-absent">Absent</span>
            {% elif 'Half' in s %}<span class="badge b-half">Half Day</span>
            {% elif 'Leave'==s %}<span class="badge b-leave">Leave</span>
            {% else %}<span class="badge">{{ s }}</span>{% endif %}
          </td>
          <td class="text-sm">{{ rec.check_in or '—' }}</td>
          <td class="text-sm">{{ rec.check_out or '—' }}</td>
        </tr>
        {% else %}
        <tr><td colspan="5" style="text-align:center;padding:28px;color:#94A3B8">No records for this month</td></tr>
        {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</div>

{% else %}
<div class="card" style="text-align:center;padding:52px 20px">
  <i class="fas fa-calendar-alt" style="font-size:42px;color:#CBD5E1;margin-bottom:13px;display:block"></i>
  <h3 style="color:#64748B;margin-bottom:6px">Select an Employee</h3>
  <p class="text-muted text-sm">Choose an employee and month to view attendance history</p>
</div>
{% endif %}
"""


# ─── SALARY LIST ──────────────────────────────────────────────────────────────
SALARY_LIST_TMPL = """
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;flex-wrap:wrap;gap:10px">
  <div><div style="font-size:15px;font-weight:700">Salary Management</div><div class="text-sm text-muted mt-4">{{ month_name }} {{ year }}</div></div>
  <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
    <form method="GET" style="display:flex;gap:7px;align-items:center">
      <select name="month" class="fc" style="width:130px" onchange="this.form.submit()">
        {% for m,mn in [(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),(7,'July'),(8,'August'),(9,'September'),(10,'October'),(11,'November'),(12,'December')] %}
        <option value="{{ m }}" {{ 'selected' if m==month else '' }}>{{ mn }}</option>{% endfor %}
      </select>
      <select name="year" class="fc" style="width:90px" onchange="this.form.submit()">
        {% for y in [2023,2024,2025,2026] %}<option value="{{ y }}" {{ 'selected' if y==year else '' }}>{{ y }}</option>{% endfor %}
      </select>
    </form>
    {% if unprocessed %}
    <form method="POST" action="/salary/generate-all" style="display:inline">
      <input type="hidden" name="month" value="{{ month }}"/><input type="hidden" name="year" value="{{ year }}"/>
      <button type="submit" class="btn btn-primary"><i class="fas fa-magic"></i> Generate All</button>
    </form>
    {% endif %}
  </div>
</div>

<!-- Summary Cards -->
<div class="stats-grid" style="grid-template-columns:repeat(4,1fr);margin-bottom:20px">
  <div class="stat-card" style="padding:16px"><div class="stat-icon si-purple" style="width:40px;height:40px;font-size:16px;border-radius:10px"><i class="fas fa-file-invoice-dollar"></i></div><div><div class="stat-val" style="font-size:18px">{{ records|length }}</div><div class="stat-lbl">Processed</div></div></div>
  <div class="stat-card" style="padding:16px"><div class="stat-icon si-green" style="width:40px;height:40px;font-size:16px;border-radius:10px"><i class="fas fa-check-circle"></i></div><div><div class="stat-val" style="font-size:18px">{{ paid_count }}</div><div class="stat-lbl">Paid</div></div></div>
  <div class="stat-card" style="padding:16px"><div class="stat-icon si-orange" style="width:40px;height:40px;font-size:16px;border-radius:10px"><i class="fas fa-rupee-sign"></i></div><div><div class="stat-val" style="font-size:16px">₹{{ "{:,.0f}".format(total_net) }}</div><div class="stat-lbl">Net Payable</div></div></div>
  <div class="stat-card" style="padding:16px"><div class="stat-icon si-red" style="width:40px;height:40px;font-size:16px;border-radius:10px"><i class="fas fa-clock"></i></div><div><div class="stat-val" style="font-size:18px">{{ unprocessed|length }}</div><div class="stat-lbl">Pending</div></div></div>
</div>

<!-- Unprocessed employees -->
{% if unprocessed %}
<div class="card mb-16">
  <div class="card-header"><div class="card-title" style="color:#D97706"><i class="fas fa-exclamation-triangle" style="margin-right:6px"></i>Pending Salary Generation</div></div>
  <div style="display:flex;flex-wrap:wrap;gap:8px">
    {% for emp in unprocessed %}
    <form method="POST" action="/salary/generate" style="display:inline">
      <input type="hidden" name="employee_id" value="{{ emp.id }}"/>
      <input type="hidden" name="month" value="{{ month }}"/>
      <input type="hidden" name="year" value="{{ year }}"/>
      <input type="hidden" name="other_deductions" value="0"/>
      <button type="submit" class="btn btn-outline btn-sm"><i class="fas fa-play"></i> {{ emp.name }}</button>
    </form>
    {% endfor %}
  </div>
</div>
{% endif %}

<!-- Processed records -->
<div class="card">
  <div class="tbl-wrap">
    <table>
      <thead><tr><th>Employee</th><th>Gross</th><th>Days Present</th><th>LOP</th><th>Deductions</th><th>Net Salary</th><th>Status</th><th>Actions</th></tr></thead>
      <tbody>
      {% for rec in records %}
      <tr>
        <td><div class="emp-cell"><div class="emp-av">{{ rec.employee.name[0]|upper }}</div><div><div class="emp-name">{{ rec.employee.name }}</div><div class="emp-id">{{ rec.employee.employee_id }}</div></div></div></td>
        <td>₹{{ "{:,.0f}".format(rec.gross_salary) }}</td>
        <td><strong>{{ "%.1f"|format(rec.days_present) }}</strong><span class="text-muted text-sm"> / {{ rec.total_working_days }}</span></td>
        <td>{% if rec.lop_deduction > 0 %}<span style="color:#DC2626;font-weight:600">₹{{ "{:,.0f}".format(rec.lop_deduction) }}</span>{% else %}<span class="text-muted">—</span>{% endif %}</td>
        <td style="color:#DC2626">₹{{ "{:,.0f}".format(rec.pf_deduction+rec.esi_deduction+rec.other_deductions+rec.lop_deduction) }}</td>
        <td><strong style="color:#059669;font-size:13px">₹{{ "{:,.0f}".format(rec.net_salary) }}</strong></td>
        <td>{% if rec.is_paid %}<span class="badge b-success">Paid</span>{% else %}<span class="badge b-warning">Pending</span>{% endif %}</td>
        <td>
          <div style="display:flex;gap:5px">
            <a href="/salary/slip/{{ rec.id }}" class="btn btn-outline btn-sm" title="View Slip"><i class="fas fa-file-alt"></i></a>
            {% if not rec.is_paid %}
            <form method="POST" action="/salary/mark-paid/{{ rec.id }}" style="display:inline">
              <input type="hidden" name="month" value="{{ month }}"/><input type="hidden" name="year" value="{{ year }}"/>
              <button type="submit" class="btn btn-success btn-sm" title="Mark Paid"><i class="fas fa-check"></i></button>
            </form>
            {% endif %}
          </div>
        </td>
      </tr>
      {% else %}
      <tr><td colspan="8" style="text-align:center;padding:36px;color:#94A3B8"><i class="fas fa-file-invoice-dollar" style="font-size:28px;margin-bottom:8px;display:block"></i>No salary records for this month</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>
"""


# ─── SALARY SLIP ──────────────────────────────────────────────────────────────
SALARY_SLIP_TMPL = """
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px" class="no-print">
  <div style="font-size:15px;font-weight:700">Salary Slip</div>
  <div style="display:flex;gap:8px">
    <a href="/salary?month={{ record.month }}&year={{ record.year }}" class="btn btn-outline btn-sm"><i class="fas fa-arrow-left"></i> Back</a>
    <button onclick="printSlip()" class="btn btn-primary btn-sm"><i class="fas fa-print"></i> Print</button>
  </div>
</div>

<div class="slip-wrap">
  <div class="slip-hdr">
    <div style="display:flex;align-items:flex-start;justify-content:space-between">
      <div>
        <div style="font-size:22px;font-weight:800;margin-bottom:4px">AttendPro HRMS</div>
        <div style="font-size:12px;opacity:.7">Salary Slip — {{ month_name }} {{ record.year }}</div>
      </div>
      <div style="text-align:right">
        <div style="background:rgba(255,255,255,.15);border-radius:8px;padding:8px 14px">
          <div style="font-size:10px;opacity:.7;text-transform:uppercase;letter-spacing:.5px">Net Salary</div>
          <div style="font-size:22px;font-weight:800">₹{{ "{:,.0f}".format(record.net_salary) }}</div>
        </div>
      </div>
    </div>
    <div style="margin-top:20px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
      <div><div style="font-size:10px;opacity:.6;margin-bottom:3px">Employee Name</div><div style="font-weight:600">{{ employee.name }}</div></div>
      <div><div style="font-size:10px;opacity:.6;margin-bottom:3px">Employee ID</div><div style="font-weight:600">{{ employee.employee_id }}</div></div>
      <div><div style="font-size:10px;opacity:.6;margin-bottom:3px">Department</div><div style="font-weight:600">{{ employee.department or '—' }}</div></div>
      <div><div style="font-size:10px;opacity:.6;margin-bottom:3px">Designation</div><div style="font-weight:600">{{ employee.role or '—' }}</div></div>
      <div><div style="font-size:10px;opacity:.6;margin-bottom:3px">Pay Period</div><div style="font-weight:600">{{ month_name }} {{ record.year }}</div></div>
      <div><div style="font-size:10px;opacity:.6;margin-bottom:3px">Payment Status</div><div style="font-weight:600">{% if record.is_paid %}✅ Paid{% else %}⏳ Pending{% endif %}</div></div>
    </div>
  </div>

  <div class="slip-body">
    <!-- Attendance -->
    <div style="background:#F8F9FE;border-radius:9px;padding:14px;margin-bottom:20px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;text-align:center">
      <div><div style="font-size:10px;color:#94A3B8;font-weight:600;text-transform:uppercase;letter-spacing:.4px">Working Days</div><div style="font-size:19px;font-weight:800;margin-top:3px">{{ record.total_working_days }}</div></div>
      <div><div style="font-size:10px;color:#059669;font-weight:600;text-transform:uppercase;letter-spacing:.4px">Days Present</div><div style="font-size:19px;font-weight:800;color:#059669;margin-top:3px">{{ "%.1f"|format(record.days_present) }}</div></div>
      <div><div style="font-size:10px;color:#DC2626;font-weight:600;text-transform:uppercase;letter-spacing:.4px">Days Absent</div><div style="font-size:19px;font-weight:800;color:#DC2626;margin-top:3px">{{ "%.1f"|format(record.days_absent) }}</div></div>
      <div><div style="font-size:10px;color:#D97706;font-weight:600;text-transform:uppercase;letter-spacing:.4px">Half Days</div><div style="font-size:19px;font-weight:800;color:#D97706;margin-top:3px">{{ record.half_days }}</div></div>
    </div>

    <div class="row-2">
      <!-- Earnings -->
      <div>
        <div class="slip-sec">Earnings</div>
        <div class="slip-row"><span>Basic Pay (40%)</span><span>₹{{ "{:,.2f}".format(record.basic_pay) }}</span></div>
        <div class="slip-row"><span>HRA (20%)</span><span>₹{{ "{:,.2f}".format(record.hra) }}</span></div>
        <div class="slip-row"><span>Transport Allowance</span><span>₹{{ "{:,.2f}".format(record.transport_allowance) }}</span></div>
        <div class="slip-row"><span>Medical Allowance</span><span>₹{{ "{:,.2f}".format(record.medical_allowance) }}</span></div>
        <div class="slip-row"><span>Special Allowance</span><span>₹{{ "{:,.2f}".format(record.special_allowance) }}</span></div>
        <div class="slip-row slip-total"><span>Total Earnings</span><span style="color:#059669">₹{{ "{:,.2f}".format(total_earnings) }}</span></div>
      </div>
      <!-- Deductions -->
      <div>
        <div class="slip-sec">Deductions</div>
        <div class="slip-row"><span>PF (12% of Basic)</span><span style="color:#DC2626">₹{{ "{:,.2f}".format(record.pf_deduction) }}</span></div>
        <div class="slip-row"><span>ESI{% if record.esi_deduction==0 %} (N/A){% endif %}</span><span style="color:#DC2626">₹{{ "{:,.2f}".format(record.esi_deduction) }}</span></div>
        {% if record.lop_deduction > 0 %}<div class="slip-row"><span>Loss of Pay (LOP)</span><span style="color:#DC2626">₹{{ "{:,.2f}".format(record.lop_deduction) }}</span></div>{% endif %}
        {% if record.other_deductions > 0 %}<div class="slip-row"><span>Other Deductions</span><span style="color:#DC2626">₹{{ "{:,.2f}".format(record.other_deductions) }}</span></div>{% endif %}
        <div class="slip-row slip-total"><span>Total Deductions</span><span style="color:#DC2626">₹{{ "{:,.2f}".format(total_deductions) }}</span></div>
      </div>
    </div>

    <div class="slip-net">
      <div><div class="slip-net-lbl">NET SALARY PAYABLE</div><div style="font-size:11px;color:#6C63FF;opacity:.7;margin-top:2px">{{ month_name }} {{ record.year }}</div></div>
      <div class="slip-net-val">₹{{ "{:,.2f}".format(record.net_salary) }}</div>
    </div>

    <div style="margin-top:20px;padding-top:16px;border-top:1px dashed #E2E8F0;display:flex;justify-content:space-between;font-size:11px;color:#94A3B8">
      <span>Generated by AttendPro HRMS</span>
      <span>This is a computer-generated payslip and does not require a signature.</span>
    </div>
  </div>
</div>
"""
