#!/usr/bin/env python3
import http.server, socketserver, urllib.request, urllib.error
import json, os, sys, time, socket, threading, webbrowser

import os
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1498220624626057348/UcYbJyIFXpWjPJy-nezRP1jooIK_DVIugcAYiNO-WkwHS5AOWDg0qMRs6iSH97YkXIU4"

def send_discord(title, message):
    try:
        import json as _json
        payload = _json.dumps({
            "embeds": [{
                "title": title,
                "description": message,
                "color": 15158332
            }]
        }).encode("utf-8")
        req = urllib.request.Request(
            DISCORD_WEBHOOK,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
        print(f"[Discord] Sent: {title}")
    except Exception as e:
        print(f"[Discord] Error: {e}")

PORT = int(os.environ.get("PORT", 7788))
api_key = ""
prev_errors = set()

HTML = '<!DOCTYPE html>\n<html lang="th">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">\n<meta name="theme-color" content="#22d3a0">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<meta name="apple-mobile-web-app-title" content="n8n Monitor">\n<link rel="manifest" href="/manifest.json">\n<link rel="apple-touch-icon" href="/icon-192.png">\n<title>n8n Workflow Monitor</title>\n<style>\n@import url(\'https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=IBM+Plex+Sans+Thai:wght@300;400;500;600&display=swap\');\n:root{\n  --bg:#0a0c0f;--bg2:#111318;--bg3:#181b22;--panel:#1a1d26;\n  --border:#252836;--border2:#2e3347;\n  --text:#e2e6f0;--text2:#8b92a8;--text3:#555d78;\n  --green:#22d3a0;--green-bg:#0d2b22;--green-border:#1a5940;\n  --red:#f56565;--red-bg:#2a1010;--red-border:#5c2020;\n  --amber:#f5a623;--amber-bg:#2a1f08;--amber-border:#5c3d10;\n  --blue:#60a5fa;\n  --safe-top: env(safe-area-inset-top);\n  --safe-bottom: env(safe-area-inset-bottom);\n}\n*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}\nhtml,body{height:100%;overflow-x:hidden}\nbody{font-family:\'IBM Plex Sans Thai\',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding-bottom:calc(80px + var(--safe-bottom))}\n\n/* Header */\nheader{background:var(--bg2);border-bottom:1px solid var(--border);padding:calc(16px + var(--safe-top)) 20px 14px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}\n.logo-area{display:flex;align-items:center;gap:10px}\n.logo-icon{width:34px;height:34px;background:linear-gradient(135deg,#22d3a0,#0ea5e9);border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:15px;color:#000;font-family:\'JetBrains Mono\',monospace;flex-shrink:0}\n.logo-text{font-size:14px;font-weight:600}\n.logo-sub{font-size:10px;color:var(--text3);font-family:\'JetBrains Mono\',monospace}\n.header-actions{display:flex;align-items:center;gap:8px}\n.icon-btn{width:36px;height:36px;border-radius:10px;border:1px solid var(--border2);background:var(--bg3);display:flex;align-items:center;justify-content:center;cursor:pointer;color:var(--text2);transition:all .2s;flex-shrink:0}\n.icon-btn:active{transform:scale(0.94);background:var(--border)}\n.icon-btn.spinning svg{animation:spin .8s linear infinite}\n.notif-btn{border-color:var(--amber-border);background:var(--amber-bg);color:var(--amber)}\n.notif-btn.active{border-color:var(--green-border);background:var(--green-bg);color:var(--green)}\n\n/* Stats */\n.stats-bar{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border-bottom:1px solid var(--border)}\n.stat-item{background:var(--bg2);padding:12px 8px;text-align:center}\n.stat-num{font-size:24px;font-weight:600;font-family:\'JetBrains Mono\',monospace;line-height:1}\n.stat-label{font-size:9px;color:var(--text3);margin-top:3px;text-transform:uppercase;letter-spacing:0.6px}\n.stat-green .stat-num{color:var(--green)}\n.stat-red .stat-num{color:var(--red)}\n.stat-amber .stat-num{color:var(--amber)}\n.stat-blue .stat-num{color:var(--blue)}\n\n/* Alert */\n.alert-banner{background:var(--red-bg);border-bottom:2px solid var(--red-border);padding:12px 20px;font-size:13px;color:var(--red);display:flex;align-items:center;gap:10px;animation:slideDown .3s ease}\n.alert-banner.hidden{display:none}\n@keyframes slideDown{from{transform:translateY(-100%)}to{transform:translateY(0)}}\n\n/* Main */\nmain{padding:16px}\n.section-title{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--text3);font-family:\'JetBrains Mono\',monospace;margin-bottom:12px}\n\n/* Cards */\n.workflow-list{display:flex;flex-direction:column;gap:12px}\n.wf-card{background:var(--panel);border:1px solid var(--border);border-radius:16px;overflow:hidden;transition:all .3s}\n.wf-card.status-ok{border-color:var(--green-border)}\n.wf-card.status-error{border-color:var(--red-border);animation:error-pulse 3s ease-in-out infinite}\n@keyframes error-pulse{0%,100%{box-shadow:0 0 0 0 transparent}50%{box-shadow:0 0 0 4px rgba(245,101,101,0.12)}}\n.wf-accent{height:3px}\n.status-ok .wf-accent{background:var(--green)}\n.status-error .wf-accent{background:var(--red)}\n.status-loading .wf-accent{background:var(--border2)}\n\n.wf-header{padding:14px 16px 10px;display:flex;align-items:center;justify-content:space-between;gap:10px;cursor:pointer}\n.wf-title-area{flex:1;min-width:0}\n.wf-name{font-size:14px;font-weight:600;line-height:1.3}\n.wf-id{font-size:10px;font-family:\'JetBrains Mono\',monospace;color:var(--text3);margin-top:2px}\n.wf-right{display:flex;align-items:center;gap:8px;flex-shrink:0}\n\n.badge{display:flex;align-items:center;gap:5px;padding:5px 10px;border-radius:20px;font-size:11px;font-weight:500;font-family:\'JetBrains Mono\',monospace;white-space:nowrap}\n.badge-ok{background:var(--green-bg);color:var(--green);border:1px solid var(--green-border)}\n.badge-error{background:var(--red-bg);color:var(--red);border:1px solid var(--red-border)}\n.badge-loading{background:var(--bg3);color:var(--text3);border:1px solid var(--border)}\n.badge-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}\n.badge-ok .badge-dot{background:var(--green);animation:pulse-g 2s infinite}\n.badge-error .badge-dot{background:var(--red);animation:pulse-r 1.5s infinite}\n.badge-loading .badge-dot{background:var(--text3);animation:blink 1s step-end infinite}\n@keyframes pulse-g{0%,100%{opacity:1}50%{opacity:0.4}}\n@keyframes pulse-r{0%,100%{opacity:1}50%{opacity:0.2}}\n@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}\n@keyframes spin{to{transform:rotate(360deg)}}\n\n.chevron{transition:transform .3s;color:var(--text3)}\n.wf-card.expanded .chevron{transform:rotate(180deg)}\n\n/* Executions */\n.wf-body{border-top:1px solid var(--border);display:none}\n.wf-card.expanded .wf-body{display:block}\n\n.exec-header{display:grid;grid-template-columns:20px 1fr 80px 60px;gap:6px;padding:8px 16px;background:var(--bg3);border-bottom:1px solid var(--border);font-size:9px;text-transform:uppercase;letter-spacing:.6px;color:var(--text3);font-family:\'JetBrains Mono\',monospace}\n.exec-row{display:grid;grid-template-columns:20px 1fr 80px 60px;gap:6px;padding:10px 16px;border-bottom:1px solid var(--border);align-items:center}\n.exec-row:last-child{border-bottom:none}\n.exec-status-icon{width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0}\n.icon-ok{background:var(--green-bg);border:1px solid var(--green-border)}\n.icon-error{background:var(--red-bg);border:1px solid var(--red-border)}\n.icon-run{background:var(--amber-bg);border:1px solid var(--amber-border)}\n.exec-id{font-family:\'JetBrains Mono\',monospace;font-size:11px;color:var(--text2)}\n.exec-time{font-family:\'JetBrains Mono\',monospace;font-size:10px;color:var(--text3)}\n.exec-dur{font-family:\'JetBrains Mono\',monospace;font-size:10px;color:var(--text3);text-align:right}\n\n.exec-err{background:var(--red-bg);border-top:1px solid var(--red-border);padding:8px 16px;font-size:11px;color:#ff9090;font-family:\'JetBrains Mono\',monospace;word-break:break-all;line-height:1.5}\n\n.wf-footer{padding:10px 16px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid var(--border);background:var(--bg3)}\n.wf-link{font-size:11px;color:var(--text3);text-decoration:none;display:flex;align-items:center;gap:4px;font-family:\'JetBrains Mono\',monospace}\n.last-check{font-size:10px;color:var(--text3);font-family:\'JetBrains Mono\',monospace}\n\n/* Skeleton */\n.skeleton{background:linear-gradient(90deg,var(--bg3) 25%,var(--border) 50%,var(--bg3) 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:4px;height:10px}\n@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}\n.no-exec{padding:16px;text-align:center;color:var(--text3);font-size:12px;font-family:\'JetBrains Mono\',monospace}\n\n/* Bottom nav */\n.bottom-nav{position:fixed;bottom:0;left:0;right:0;background:var(--bg2);border-top:1px solid var(--border);padding:10px 20px calc(10px + var(--safe-bottom));display:flex;align-items:center;justify-content:space-between;z-index:100}\n.refresh-info{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--text2);font-family:\'JetBrains Mono\',monospace}\n.live-dot{width:7px;height:7px;border-radius:50%;background:var(--green);animation:pulse-g 2s infinite}\n.refresh-btn-big{background:var(--green-bg);border:1px solid var(--green-border);color:var(--green);padding:8px 18px;border-radius:10px;font-size:13px;font-weight:500;cursor:pointer;font-family:\'IBM Plex Sans Thai\',sans-serif;display:flex;align-items:center;gap:6px;transition:all .2s}\n.refresh-btn-big:active{transform:scale(0.96)}\n.refresh-btn-big.spinning svg{animation:spin .8s linear infinite}\n\n/* Install prompt */\n.install-banner{background:var(--blue-bg,#0d1c38);border:1px solid var(--blue);border-radius:12px;padding:14px 16px;margin-bottom:14px;display:flex;align-items:center;gap:12px;cursor:pointer}\n.install-banner.hidden{display:none}\n.install-banner-text{flex:1}\n.install-banner-text strong{font-size:13px;display:block;color:var(--blue)}\n.install-banner-text span{font-size:11px;color:var(--text2)}\n.install-btn{background:var(--blue);color:#000;padding:7px 14px;border-radius:8px;font-size:12px;font-weight:600;white-space:nowrap;border:none;cursor:pointer}\n\n/* Modal */\n.modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);z-index:200;display:flex;align-items:flex-end}\n.modal-overlay.hidden{display:none}\n.modal{background:var(--panel);border-radius:20px 20px 0 0;padding:24px 20px calc(24px + var(--safe-bottom));width:100%;border-top:1px solid var(--border2)}\n.modal h2{font-size:16px;font-weight:600;margin-bottom:6px}\n.modal p{font-size:13px;color:var(--text2);margin-bottom:18px;line-height:1.6}\n.modal label{font-size:11px;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;display:block;margin-bottom:6px;font-family:\'JetBrains Mono\',monospace}\n.modal input{width:100%;background:var(--bg3);border:1px solid var(--border2);border-radius:10px;padding:12px 14px;color:var(--text);font-size:14px;font-family:\'JetBrains Mono\',monospace;margin-bottom:16px;outline:none}\n.modal input:focus{border-color:var(--green)}\n.modal-btns{display:flex;gap:10px}\n.btn-primary{flex:1;background:var(--green-bg);border:1px solid var(--green-border);color:var(--green);padding:13px;border-radius:12px;font-size:14px;font-weight:500;cursor:pointer;font-family:\'IBM Plex Sans Thai\',sans-serif}\n.btn-cancel{background:transparent;border:1px solid var(--border2);color:var(--text2);padding:13px 18px;border-radius:12px;font-size:14px;cursor:pointer}\n</style>\n</head>\n<body>\n\n<!-- Settings Modal -->\n<div class="modal-overlay hidden" id="modal-overlay">\n  <div class="modal">\n    <h2>⚙ ตั้งค่า API</h2>\n    <p>ใส่ n8n API Key เพื่อดึงข้อมูล Executions<br>n8n → Settings → API → Create API Key</p>\n    <label>N8N API KEY</label>\n    <input type="password" id="api-key-input" placeholder="n8n_api_xxxxxxxx..." autocomplete="off" />\n    <div class="modal-btns">\n      <button class="btn-cancel" onclick="closeModal()">ยกเลิก</button>\n      <button class="btn-primary" onclick="saveKey()">บันทึก</button>\n    </div>\n  </div>\n</div>\n\n<header>\n  <div class="logo-area">\n    <div class="logo-icon">n8</div>\n    <div>\n      <div class="logo-text">Workflow Monitor</div>\n      <div class="logo-sub">LIVE EXECUTION TRACKER</div>\n    </div>\n  </div>\n  <div class="header-actions">\n    <div class="icon-btn notif-btn" id="notif-btn" onclick="toggleNotifications()" title="เปิด/ปิดแจ้งเตือน">\n      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0"/></svg>\n    </div>\n    <div class="icon-btn" onclick="openModal()" title="ตั้งค่า">\n      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>\n    </div>\n  </div>\n</header>\n\n<div class="stats-bar">\n  <div class="stat-item stat-blue"><div class="stat-num" id="stat-total">–</div><div class="stat-label">Workflows</div></div>\n  <div class="stat-item stat-green"><div class="stat-num" id="stat-ok">–</div><div class="stat-label">OK</div></div>\n  <div class="stat-item stat-red"><div class="stat-num" id="stat-err">–</div><div class="stat-label">Error</div></div>\n  <div class="stat-item stat-amber"><div class="stat-num" id="stat-rate">–</div><div class="stat-label">Success%</div></div>\n</div>\n\n<div class="alert-banner hidden" id="alert-banner">\n  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0zM12 9v4M12 17h.01"/></svg>\n  <span id="alert-text"></span>\n</div>\n\n<main>\n  <div class="install-banner hidden" id="install-banner" onclick="installApp()">\n    <div style="font-size:28px">📲</div>\n    <div class="install-banner-text">\n      <strong>ติดตั้งเป็นแอพ</strong>\n      <span>เปิดได้เหมือนแอพปกติ + รับ notification</span>\n    </div>\n    <button class="install-btn">ติดตั้ง</button>\n  </div>\n\n  <div class="section-title">// WORKFLOW STATUS</div>\n  <div class="workflow-list" id="workflow-list"></div>\n</main>\n\n<div class="bottom-nav">\n  <div class="refresh-info">\n    <div class="live-dot"></div>\n    <span>รีเฟรชใน <span id="countdown">30</span>s</span>\n  </div>\n  <button class="refresh-btn-big" id="refresh-btn" onclick="refreshAll()">\n    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2v6h-6M3 12a9 9 0 0115-6.7L21 8M3 22v-6h6M21 12a9 9 0 01-15 6.7L3 16"/></svg>\n    Refresh\n  </button>\n</div>\n\n<script>\nconst REFRESH_SEC = 30;\nconst PROXY = `${location.origin}/proxy`;\n\nconst WORKFLOWS = [\n  { id:\'k1vilVKLUMcZjUBH\', name:\'✨ LINE Bot - Main Router\',     base:\'https://yuttachai-n8n.duckdns.org\' },\n  { id:\'TlUYXM2Ehd733gxR\', name:\'Sup WH: Master Workflow\',       base:\'https://yuttachai-n8n.duckdns.org\' },\n  { id:\'qYOPgdzXUw2TegOj\', name:\'Sup Warehouse Location Update\', base:\'https://yuttachai-n8n.duckdns.org\' },\n  { id:\'QAnKuEB6zcMfC844\', name:\'Sup Order Status Automation\',   base:\'https://yuttachai-n8n.duckdns.org\' },\n];\n\nlet wfData = {}, apiKey = localStorage.getItem(\'n8n_api_key\')||\'\';\nlet countdown = REFRESH_SEC, timer = null;\nlet notifEnabled = localStorage.getItem(\'notif_enabled\') === \'1\';\nlet prevErrors = JSON.parse(localStorage.getItem(\'prev_errors\')||\'[]\');\nlet deferredInstall = null;\n\n// ===== PWA =====\nif (\'serviceWorker\' in navigator) {\n  navigator.serviceWorker.register(\'/sw.js\').catch(console.error);\n}\nwindow.addEventListener(\'beforeinstallprompt\', e => {\n  e.preventDefault();\n  deferredInstall = e;\n  document.getElementById(\'install-banner\').classList.remove(\'hidden\');\n});\nwindow.addEventListener(\'appinstalled\', () => {\n  document.getElementById(\'install-banner\').classList.add(\'hidden\');\n  deferredInstall = null;\n});\n\nasync function installApp() {\n  if (!deferredInstall) return;\n  deferredInstall.prompt();\n  const { outcome } = await deferredInstall.userChoice;\n  if (outcome === \'accepted\') document.getElementById(\'install-banner\').classList.add(\'hidden\');\n}\n\n// ===== NOTIFICATIONS =====\nfunction updateNotifBtn() {\n  const btn = document.getElementById(\'notif-btn\');\n  btn.classList.toggle(\'active\', notifEnabled);\n  btn.title = notifEnabled ? \'แจ้งเตือน: เปิดอยู่\' : \'แจ้งเตือน: ปิดอยู่\';\n}\n\nasync function toggleNotifications() {\n  if (!notifEnabled) {\n    if (!(\'Notification\' in window)) { alert(\'Browser นี้ไม่รองรับ Notification\'); return; }\n    const perm = await Notification.requestPermission();\n    if (perm !== \'granted\') { alert(\'กรุณาอนุญาต Notification ในการตั้งค่า Browser\'); return; }\n    notifEnabled = true;\n  } else {\n    notifEnabled = false;\n  }\n  localStorage.setItem(\'notif_enabled\', notifEnabled ? \'1\' : \'0\');\n  updateNotifBtn();\n}\n\nfunction sendDesktopNotif(title, body, tag) {\n  if (!notifEnabled || Notification.permission !== \'granted\') return;\n  // Try service worker notification first (works on mobile too)\n  if (\'serviceWorker\' in navigator && navigator.serviceWorker.controller) {\n    navigator.serviceWorker.ready.then(reg => {\n      reg.showNotification(title, {\n        body, tag, icon: \'/icon-192.png\', badge: \'/icon-192.png\',\n        vibrate: [200, 100, 200], renotify: true,\n        data: { url: location.href }\n      });\n    });\n  } else {\n    new Notification(title, { body, tag, icon: \'/icon-192.png\' });\n  }\n}\n\nfunction checkAndNotify(newErrors) {\n  if (!notifEnabled) return;\n  const newErrIds = newErrors.map(w => w.id);\n  const brandNew = newErrors.filter(w => !prevErrors.includes(w.id));\n  if (brandNew.length > 0) {\n    const names = brandNew.map(w => w.name.replace(/[✨❗]/g,\'\')).join(\', \');\n    sendDesktopNotif(\n      `🔴 n8n Error (${brandNew.length} workflow)`,\n      names,\n      \'n8n-error\'\n    );\n  }\n  prevErrors = newErrIds;\n  localStorage.setItem(\'prev_errors\', JSON.stringify(prevErrors));\n}\n\n// ===== MODAL =====\nfunction openModal() {\n  document.getElementById(\'api-key-input\').value = apiKey;\n  document.getElementById(\'modal-overlay\').classList.remove(\'hidden\');\n  setTimeout(() => document.getElementById(\'api-key-input\').focus(), 300);\n}\nfunction closeModal() { document.getElementById(\'modal-overlay\').classList.add(\'hidden\'); }\nfunction saveKey() {\n  const v = document.getElementById(\'api-key-input\').value.trim();\n  if (!v) { alert(\'กรุณาใส่ API Key\'); return; }\n  apiKey = v;\n  localStorage.setItem(\'n8n_api_key\', apiKey);\n  closeModal();\n  refreshAll();\n  if (!timer) startCountdown();\n}\ndocument.getElementById(\'api-key-input\').addEventListener(\'keydown\', e => { if(e.key===\'Enter\') saveKey(); });\ndocument.getElementById(\'modal-overlay\').addEventListener(\'click\', e => { if(e.target===e.currentTarget) closeModal(); });\n\n// ===== RENDER =====\nfunction renderCards() {\n  document.getElementById(\'workflow-list\').innerHTML =\n    WORKFLOWS.map(wf => cardHTML(wf, wfData[wf.id]??null)).join(\'\');\n}\n\nfunction cardHTML(wf, data) {\n  const loading = data===null;\n  const errored = data&&(data.hasError||data.connectionError);\n  const cls = loading?\'status-loading\':errored?\'status-error\':\'status-ok\';\n  const badge = loading\n    ? `<div class="badge badge-loading"><div class="badge-dot"></div>Loading</div>`\n    : errored\n      ? `<div class="badge badge-error"><div class="badge-dot"></div>ERROR</div>`\n      : `<div class="badge badge-ok"><div class="badge-dot"></div>OK</div>`;\n\n  let body = \'\';\n  if (loading) {\n    body = `<div class="wf-body" style="display:block"><div style="padding:14px 16px;display:flex;flex-direction:column;gap:8px">\n      <div class="skeleton" style="width:75%"></div><div class="skeleton" style="width:55%"></div>\n    </div></div>`;\n  } else if (data&&data.connectionError) {\n    body = `<div class="wf-body"><div class="exec-err">❌ ${esc(data.errorMessage||\'Connection failed\')}</div>\n      <div class="wf-footer"><a class="wf-link" href="${wf.base}/workflow/${wf.id}/executions" target="_blank">Open in n8n ↗</a>\n      <span class="last-check">${new Date().toLocaleTimeString(\'th-TH\')}</span></div></div>`;\n  } else if (data&&data.executions&&data.executions.length>0) {\n    const rows = data.executions.slice(0,5).map(ex => {\n      const err = ex.status===\'error\'||ex.status===\'crashed\';\n      const run = ex.status===\'running\'||ex.status===\'waiting\';\n      const ic = err?\'icon-error\':run?\'icon-run\':\'icon-ok\';\n      const ch = err?\'✕\':run?\'◌\':\'✓\';\n      const col = err?\'#f56565\':run?\'#f5a623\':\'#22d3a0\';\n      const t = ex.startedAt?ago(ex.startedAt):\'–\';\n      const d = ex.stoppedAt&&ex.startedAt?dur(new Date(ex.stoppedAt)-new Date(ex.startedAt)):run?\'running…\':\'–\';\n      const errMsg = err&&ex.data?.resultData?.error?.message\n        ? `<div class="exec-err">⚠ ${esc(String(ex.data.resultData.error.message).slice(0,120))}</div>` : \'\';\n      return `<div class="exec-row">\n        <div class="exec-status-icon ${ic}"><span style="color:${col};font-size:9px;font-weight:700">${ch}</span></div>\n        <div class="exec-id">#${ex.id}</div><div class="exec-time">${t}</div><div class="exec-dur">${d}</div>\n      </div>${errMsg}`;\n    }).join(\'\');\n    body = `<div class="wf-body">\n      <div class="exec-header"><div></div><div>EXEC ID</div><div>STARTED</div><div style="text-align:right">DUR</div></div>\n      ${rows}\n      <div class="wf-footer"><a class="wf-link" href="${wf.base}/workflow/${wf.id}/executions" target="_blank">Open in n8n ↗</a>\n      <span class="last-check">${new Date().toLocaleTimeString(\'th-TH\')}</span></div>\n    </div>`;\n  } else {\n    body = `<div class="wf-body"><div class="no-exec">ไม่พบ executions</div>\n      <div class="wf-footer"><a class="wf-link" href="${wf.base}/workflow/${wf.id}/executions" target="_blank">Open in n8n ↗</a></div>\n    </div>`;\n  }\n\n  return `<div class="wf-card ${cls}" id="card-${wf.id}">\n    <div class="wf-accent"></div>\n    <div class="wf-header" onclick="toggleCard(\'${wf.id}\')">\n      <div class="wf-title-area">\n        <div class="wf-name">${esc(wf.name)}</div>\n        <div class="wf-id">${wf.id}</div>\n      </div>\n      <div class="wf-right">\n        ${badge}\n        <div class="chevron">\n          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>\n        </div>\n      </div>\n    </div>\n    ${body}\n  </div>`;\n}\n\nfunction toggleCard(id) {\n  const el = document.getElementById(`card-${id}`);\n  if (el) el.classList.toggle(\'expanded\');\n}\n\n// ===== FETCH =====\nasync function fetchWF(wf) {\n  try {\n    const url = `${wf.base}/api/v1/executions?workflowId=${wf.id}&limit=8&includeData=true`;\n    const r = await fetch(`${PROXY}?url=${encodeURIComponent(url)}&key=${encodeURIComponent(apiKey)}`);\n    if (!r.ok) throw new Error(`HTTP ${r.status}`);\n    const j = await r.json();\n    const execs = j.data||j.results||[];\n    const latestExec = execs.length > 0 ? execs.reduce((a,b) => Number(String(b.id).replace(/\D/g,''))||0 > Number(String(a.id).replace(/\D/g,''))||0 ? b : a) : null;\n    const latestStatus = latestExec ? latestExec.status : null;\n    return { executions: execs, hasError: latestStatus === \'error\' || latestStatus === \'crashed\' };\n  } catch(e) {\n    return { executions:[], hasError:true, connectionError:true, errorMessage:e.message };\n  }\n}\n\nasync function refreshAll() {\n  const btn = document.getElementById(\'refresh-btn\');\n  btn.classList.add(\'spinning\');\n  const res = await Promise.allSettled(WORKFLOWS.map(wf => fetchWF(wf)));\n  res.forEach((r,i) => { if(r.status===\'fulfilled\') wfData[WORKFLOWS[i].id]=r.value; });\n\n  // Update each card individually (preserve expanded state)\n  WORKFLOWS.forEach(wf => {\n    const el = document.getElementById(`card-${wf.id}`);\n    const wasExpanded = el?.classList.contains(\'expanded\');\n    if (el) {\n      const tmp = document.createElement(\'div\');\n      tmp.innerHTML = cardHTML(wf, wfData[wf.id]??null);\n      const newCard = tmp.firstElementChild;\n      if (wasExpanded) newCard.classList.add(\'expanded\');\n      el.replaceWith(newCard);\n    }\n  });\n\n  updateStats();\n  updateAlert();\n  btn.classList.remove(\'spinning\');\n  document.getElementById(\'last-update\') && (document.getElementById(\'last-update\').textContent = new Date().toLocaleTimeString(\'th-TH\'));\n}\n\nfunction updateStats() {\n  const total = WORKFLOWS.length;\n  let errC=0,succE=0,totE=0;\n  const errWfs = [];\n  WORKFLOWS.forEach(wf => {\n    const d = wfData[wf.id];\n    if (!d) return;\n    if (d.hasError||d.connectionError) { errC++; errWfs.push(wf); }\n    (d.executions||[]).forEach(ex => { totE++; if(ex.status===\'success\') succE++; });\n  });\n  const ok = WORKFLOWS.filter(wf => { const d=wfData[wf.id]; return d&&!d.hasError&&!d.connectionError; }).length;\n  document.getElementById(\'stat-total\').textContent = total;\n  document.getElementById(\'stat-ok\').textContent = ok;\n  document.getElementById(\'stat-err\').textContent = errC;\n  document.getElementById(\'stat-rate\').textContent = totE>0?Math.round(succE/totE*100)+\'%\':\'–\';\n  checkAndNotify(errWfs);\n}\n\nfunction updateAlert() {\n  const errWfs = WORKFLOWS.filter(wf => { const d=wfData[wf.id]; return d&&(d.hasError||d.connectionError); });\n  const b = document.getElementById(\'alert-banner\');\n  if (errWfs.length>0) {\n    document.getElementById(\'alert-text\').textContent = `⚠ ${errWfs.length} workflow มีปัญหา: ${errWfs.map(w=>w.name.replace(/[✨❗]/g,\'\')).join(\', \')}`;\n    b.classList.remove(\'hidden\');\n  } else {\n    b.classList.add(\'hidden\');\n  }\n}\n\nfunction startCountdown() {\n  countdown = REFRESH_SEC;\n  clearInterval(timer);\n  timer = setInterval(() => {\n    countdown--;\n    const el = document.getElementById(\'countdown\');\n    if (el) el.textContent = countdown;\n    if (countdown <= 0) { countdown = REFRESH_SEC; refreshAll(); }\n  }, 1000);\n}\n\nfunction ago(d) {\n  const s = Math.floor((Date.now()-new Date(d))/1000);\n  if(s<60) return s+\'s ago\';\n  if(s<3600) return Math.floor(s/60)+\'m ago\';\n  if(s<86400) return Math.floor(s/3600)+\'h ago\';\n  return Math.floor(s/86400)+\'d ago\';\n}\nfunction dur(ms) {\n  if(ms<0||isNaN(ms)) return \'–\';\n  if(ms<1000) return ms+\'ms\';\n  if(ms<60000) return (ms/1000).toFixed(1)+\'s\';\n  return Math.floor(ms/60000)+\'m\'+Math.floor((ms%60000)/1000)+\'s\';\n}\nfunction esc(s) {\n  return String(s).replace(/&/g,\'&amp;\').replace(/</g,\'&lt;\').replace(/>/g,\'&gt;\');\n}\n\n// ===== INIT =====\nupdateNotifBtn();\nrenderCards(); // show skeletons immediately\nif (!apiKey) {\n  openModal();\n} else {\n  refreshAll();\n  startCountdown();\n}\n</script>\n</body>\n</html>\n'


MANIFEST = '{"name": "n8n Workflow Monitor", "short_name": "n8n Monitor", "description": "Monitor n8n workflow executions", "start_url": "/", "display": "standalone", "background_color": "#0a0c0f", "theme_color": "#22d3a0", "orientation": "portrait-primary", "icons": [{"src": "/icon.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"}, {"src": "/icon.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}'
SW_JS = "const CACHE='n8n-v1';\nself.addEventListener('install',e=>{self.skipWaiting();});\nself.addEventListener('activate',e=>{e.waitUntil(clients.claim());});\nself.addEventListener('fetch',e=>{\n  if(e.request.url.includes('/proxy?'))return;\n  e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)));\n});\nself.addEventListener('push',e=>{\n  const d=e.data?e.data.json():{};\n  e.waitUntil(self.registration.showNotification(d.title||'n8n Monitor',{\n    body:d.body||'มีการแจ้งเตือนใหม่',\n    icon:'/icon.png',tag:'n8n',renotify:true,vibrate:[200,100,200]\n  }));\n});\nself.addEventListener('notificationclick',e=>{\n  e.notification.close();\n  e.waitUntil(clients.matchAll({type:'window'}).then(l=>{\n    if(l.length>0){l[0].focus();return;}\n    clients.openWindow('/');\n  }));\n});"
ICON_PNG = __import__('base64').b64decode('iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAIAAADdvvtQAAACpklEQVR4nO3OQQkAMQDEwGg55fVUQ+ehnyUQGAHDd0/yjPkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOo/bff3U50NzNmAAAAAElFTkSuQmCC')

MANIFEST_JSON = '{"name": "n8n Workflow Monitor", "short_name": "n8n Monitor", "description": "Monitor n8n workflow executions", "start_url": "/", "display": "standalone", "background_color": "#0a0c0f", "theme_color": "#22d3a0", "orientation": "portrait-primary", "icons": [{"src": "/icon.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"}, {"src": "/icon.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}'
SW_CODE = "const CACHE='n8n-v1';\nself.addEventListener('install',e=>{self.skipWaiting();});\nself.addEventListener('activate',e=>{e.waitUntil(clients.claim());});\nself.addEventListener('fetch',e=>{\n  if(e.request.url.includes('/proxy?'))return;\n  e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)));\n});"
ICON_DATA = __import__('base64').b64decode('iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAIAAADdvvtQAAACpklEQVR4nO3OQQkAMQDEwGg55fVUQ+ehnyUQGAHDd0/yjPkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOoMR9EjfkgaswHUWM+iBrzQdSYD6LGfBA15oOo/bff3U50NzNmAAAAAElFTkSuQmCC')

def send_toast(title, body):
    try:
        import subprocess
        ps = f"Add-Type -AssemblyName System.Windows.Forms; $n = New-Object System.Windows.Forms.NotifyIcon; $n.Icon = [System.Drawing.SystemIcons]::Warning; $n.BalloonTipTitle = '{title}'; $n.BalloonTipText = '{body}'; $n.Visible = $True; $n.ShowBalloonTip(8000); Start-Sleep 9; $n.Dispose()"
        subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps], creationflags=0x08000000)
    except Exception as e:
        print(f"[Toast] {e}")

def monitor():
    global prev_errors
    time.sleep(10)
    WFS = [
        ("k1vilVKLUMcZjUBH", "LINE Bot - Main Router"),
        ("TlUYXM2Ehd733gxR", "Sup WH: Master Workflow"),
        ("qYOPgdzXUw2TegOj", "Sup Warehouse Location Update"),
        ("QAnKuEB6zcMfC844", "Sup Order Status Automation"),
    ]
    while True:
        if api_key:
            current = set()
            for wf_id, wf_name in WFS:
                try:
                    url = f"https://yuttachai-n8n.duckdns.org/api/v1/executions?workflowId={wf_id}&limit=5"
                    req = urllib.request.Request(url, headers={"X-N8N-API-KEY": api_key, "Accept": "application/json"})
                    with urllib.request.urlopen(req, timeout=10) as r:
                        execs = json.loads(r.read()).get("data") or []
                        if execs:
                            latest = max(execs, key=lambda e: int(''.join(filter(str.isdigit, str(e.get('id','0')))) or '0')) if execs else None
                            if latest and latest.get("status") in ("error","crashed"):
                                # ดึง error message
                                err_msg = ""
                                try:
                                    rd = latest.get("data", {}).get("resultData", {})
                                    err_msg = rd.get("error", {}).get("message", "") or ""
                                    if not err_msg:
                                        # ลองหาจาก lastNodeExecuted
                                        last_node = rd.get("lastNodeExecuted", "")
                                        run_data = rd.get("runData", {})
                                        if last_node and last_node in run_data:
                                            node_data = run_data[last_node]
                                            if node_data and len(node_data) > 0:
                                                err_msg = node_data[0].get("error", {}).get("message", "") or ""
                                except: pass
                                current.add(f"{wf_id}|{wf_name}|{err_msg[:200]}")
                except: pass
            new_err = current - prev_errors
            if new_err:
                names = ", ".join(x.split("|")[1] for x in new_err)
                send_toast(f"n8n Error ({len(new_err)} workflow)", names)
                lines = []
                for x in new_err:
                    parts = x.split("|")
                    name = parts[1] if len(parts) > 1 else x
                    err = parts[2] if len(parts) > 2 and parts[2] else "ไม่ทราบสาเหตุ"
                    lines.append(f"• **{name}**\n  ❌ {err}")
                send_discord(
                    f"🔴 n8n Workflow Error ({len(new_err)} workflow)",
                    "\n\n".join(lines)
                )
                print(f"[Alert] {names}")
            prev_errors = current
        time.sleep(30)

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
    def do_OPTIONS(self):
        self.send_response(200); self.send_cors()
        self.send_header("Content-Length","0"); self.end_headers()
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        p = urlparse(self.path)
        if p.path == "/proxy":
            params = parse_qs(p.query)
            target = params.get("url",[""])[0]
            key = params.get("key",[""])[0]
            global api_key
            if key: api_key = key
            try:
                req = urllib.request.Request(target, headers={"X-N8N-API-KEY": key, "Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=10) as r:
                    data = r.read()
                    self.send_response(200)
                    self.send_header("Content-Type","application/json")
                    self.send_cors()
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers(); self.wfile.write(data)
            except urllib.error.HTTPError as e:
                body = e.read()
                self.send_response(e.code)
                self.send_header("Content-Type","application/json")
                self.send_cors()
                self.send_header("Content-Length", str(len(body)))
                self.end_headers(); self.wfile.write(body)
            except Exception as e:
                err = json.dumps({"error": str(e)}).encode()
                self.send_response(502)
                self.send_header("Content-Type","application/json")
                self.send_cors()
                self.send_header("Content-Length", str(len(err)))
                self.end_headers(); self.wfile.write(err)
            return
        # Serve PWA files
        if p.path == '/manifest.json':
            b = MANIFEST_JSON.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type','application/manifest+json')
            self.send_cors()
            self.send_header('Content-Length',str(len(b)))
            self.end_headers(); self.wfile.write(b)
            return
        if p.path == '/sw.js':
            b = SW_CODE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type','application/javascript')
            self.send_cors()
            self.send_header('Content-Length',str(len(b)))
            self.end_headers(); self.wfile.write(b)
            return
        if p.path == '/icon.png':
            self.send_response(200)
            self.send_header('Content-Type','image/png')
            self.send_cors()
            self.send_header('Content-Length',str(len(ICON_DATA)))
            self.end_headers(); self.wfile.write(ICON_DATA)
            return
        # Serve HTML
        html = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.send_cors()
        self.send_header("Content-Length", str(len(html)))
        self.end_headers(); self.wfile.write(html)

def get_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8",80)); return s.getsockname()[0]
    except: return "YOUR_IP"

if __name__ == "__main__":
    # Check already running
    pass

    threading.Thread(target=monitor, daemon=True).start()
    # No browser on cloud server

    ip = get_ip()
    print("=" * 50)
    print("  n8n Workflow Monitor กำลังทำงาน!")
    print(f"  Desktop : http://localhost:{PORT}/")
    print(f"  Mobile  : http://{ip}:{PORT}/")
    print("  กด Ctrl+C เพื่อหยุด")
    print("=" * 50)

    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nหยุดแล้ว")
