<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Abdelkader Barhoumi — Mobile Engineer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #080C14;
    --surface: #0D1520;
    --surface2: #111927;
    --border: rgba(99,179,237,0.12);
    --accent: #38BDF8;
    --accent2: #818CF8;
    --accent3: #34D399;
    --text: #E2EAF4;
    --muted: #64748B;
    --glow: rgba(56,189,248,0.15);
  }

  html { scroll-behavior: smooth; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.7;
    overflow-x: hidden;
  }

  /* NOISE OVERLAY */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.5;
  }

  /* GRID BG */
  body::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(56,189,248,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(56,189,248,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
  }

  .wrapper {
    position: relative;
    z-index: 1;
    max-width: 900px;
    margin: 0 auto;
    padding: 0 24px 80px;
  }

  /* ── HERO ── */
  .hero {
    padding: 80px 0 60px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 32px;
    align-items: start;
    border-bottom: 1px solid var(--border);
  }

  .hero-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 12px;
    color: var(--accent3);
    font-family: 'Space Mono', monospace;
    margin-bottom: 20px;
    letter-spacing: 0.05em;
  }

  .hero-status span {
    width: 7px; height: 7px;
    background: var(--accent3);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
  }

  .hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 6vw, 64px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #E2EAF4 0%, var(--accent) 60%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
  }

  .hero-role {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    color: var(--accent);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 20px;
  }

  .hero-bio {
    color: #94A3B8;
    max-width: 520px;
    font-size: 15px;
    margin-bottom: 28px;
  }

  .hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    font-size: 13px;
    color: var(--muted);
  }

  .hero-meta span {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .hero-links {
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 160px;
  }

  .hero-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    text-decoration: none;
    color: var(--text);
    font-size: 13px;
    font-family: 'Space Mono', monospace;
    transition: all 0.2s;
  }

  .hero-link:hover {
    border-color: var(--accent);
    background: rgba(56,189,248,0.06);
    color: var(--accent);
  }

  /* ── SECTION ── */
  section { padding: 60px 0; border-bottom: 1px solid var(--border); }
  section:last-child { border-bottom: none; }

  .section-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 8px;
  }

  .section-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(22px, 4vw, 34px);
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 36px;
    color: var(--text);
  }

  /* ── CODE BLOCK ── */
  .code-block {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 40px;
  }

  .code-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 18px;
    border-bottom: 1px solid var(--border);
    background: var(--surface2);
  }

  .code-dot { width: 10px; height: 10px; border-radius: 50%; }
  .code-dot.r { background: #FF5F57; }
  .code-dot.y { background: #FFBD2E; }
  .code-dot.g { background: #28CA41; }

  .code-filename {
    margin-left: auto;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--muted);
  }

  .code-body {
    padding: 24px;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    line-height: 1.8;
    overflow-x: auto;
  }

  .kw { color: #818CF8; }
  .str { color: #34D399; }
  .cls { color: #38BDF8; }
  .fn { color: #FBBF24; }
  .cm { color: #475569; font-style: italic; }
  .num { color: #FB923C; }
  .punct { color: #64748B; }

  /* ── EXPERIENCE CARDS ── */
  .exp-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

  @media (max-width: 640px) { .exp-grid { grid-template-columns: 1fr; } }

  .exp-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
  }

  .exp-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: 0;
    transition: opacity 0.2s;
  }

  .exp-card:hover { border-color: rgba(56,189,248,0.3); transform: translateY(-2px); }
  .exp-card:hover::before { opacity: 1; }

  .exp-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 11px;
    font-family: 'Space Mono', monospace;
    margin-bottom: 14px;
  }

  .badge-current {
    background: rgba(52,211,153,0.1);
    color: var(--accent3);
    border: 1px solid rgba(52,211,153,0.2);
  }

  .badge-past {
    background: rgba(129,140,248,0.1);
    color: var(--accent2);
    border: 1px solid rgba(129,140,248,0.2);
  }

  .exp-company {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 4px;
  }

  .exp-role {
    font-size: 13px;
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    margin-bottom: 4px;
  }

  .exp-period {
    font-size: 12px;
    color: var(--muted);
    margin-bottom: 16px;
  }

  .exp-items {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .exp-items li {
    font-size: 13px;
    color: #94A3B8;
    padding-left: 16px;
    position: relative;
  }

  .exp-items li::before {
    content: '→';
    position: absolute;
    left: 0;
    color: var(--accent);
  }

  .exp-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 16px;
  }

  .tag {
    padding: 3px 10px;
    background: rgba(56,189,248,0.07);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 6px;
    font-size: 11px;
    font-family: 'Space Mono', monospace;
    color: var(--accent);
  }

  /* ── SKILLS ── */
  .skills-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }

  .skill-group {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    transition: border-color 0.2s;
  }

  .skill-group:hover { border-color: rgba(56,189,248,0.25); }

  .skill-group-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .skill-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .skill-list li {
    font-size: 13px;
    color: #94A3B8;
    font-family: 'Space Mono', monospace;
  }

  /* ── PROJECTS ── */
  .projects-list { display: flex; flex-direction: column; gap: 16px; }

  .project-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 28px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 20px;
    transition: border-color 0.2s, transform 0.2s;
  }

  .project-card:hover {
    border-color: rgba(56,189,248,0.3);
    transform: translateX(4px);
  }

  .project-icon {
    font-size: 32px;
    line-height: 1;
    align-self: start;
    margin-top: 4px;
  }

  .project-name {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 6px;
  }

  .project-desc {
    font-size: 13px;
    color: #94A3B8;
    margin-bottom: 14px;
    max-width: 480px;
  }

  /* ── STATS ── */
  .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }

  @media (max-width: 480px) { .stats-grid { grid-template-columns: 1fr; } }

  .stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 28px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .stat-card::after {
    content: '';
    position: absolute;
    bottom: -30px; left: 50%;
    transform: translateX(-50%);
    width: 80px; height: 80px;
    border-radius: 50%;
    background: var(--glow);
    filter: blur(20px);
  }

  .stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 6px;
  }

  .stat-label {
    font-size: 12px;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }

  .stat-sub {
    font-size: 11px;
    color: #334155;
    margin-top: 4px;
  }

  /* ── LANG BARS ── */
  .lang-list { display: flex; flex-direction: column; gap: 14px; }

  .lang-item { }
  .lang-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
  .lang-name { font-family: 'Space Mono', monospace; font-size: 12px; color: var(--text); }
  .lang-pct { font-family: 'Space Mono', monospace; font-size: 12px; color: var(--muted); }

  .lang-bar {
    height: 4px;
    background: var(--surface2);
    border-radius: 100px;
    overflow: hidden;
  }

  .lang-fill {
    height: 100%;
    border-radius: 100px;
    animation: grow 1s ease-out forwards;
    transform-origin: left;
    transform: scaleX(0);
  }

  @keyframes grow {
    to { transform: scaleX(1); }
  }

  /* ── CERTS ── */
  .certs-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }

  @media (max-width: 560px) { .certs-grid { grid-template-columns: 1fr; } }

  .cert-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-size: 13px;
  }

  .cert-icon { font-size: 16px; margin-top: 1px; flex-shrink: 0; }
  .cert-name { color: var(--text); font-weight: 500; }
  .cert-source { color: var(--muted); font-size: 11px; font-family: 'Space Mono', monospace; }

  /* ── EDUCATION ── */
  .edu-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }

  @media (max-width: 600px) { .edu-grid { grid-template-columns: 1fr; } }

  .edu-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
  }

  .edu-icon { font-size: 24px; margin-bottom: 12px; }
  .edu-school { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 15px; margin-bottom: 4px; }
  .edu-degree { font-size: 12px; color: var(--accent); font-family: 'Space Mono', monospace; margin-bottom: 4px; }
  .edu-period { font-size: 11px; color: var(--muted); }

  /* ── FOOTER ── */
  .footer {
    padding: 48px 0 0;
    text-align: center;
  }

  .footer-email {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--accent);
    text-decoration: none;
    display: inline-block;
    margin-bottom: 16px;
    transition: color 0.2s;
  }

  .footer-email:hover { color: var(--accent2); }

  .footer-quote {
    font-size: 13px;
    color: var(--muted);
    font-style: italic;
    margin-top: 32px;
  }

  /* ANIMATIONS */
  .fade-in {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeIn 0.6s ease forwards;
  }

  @keyframes fadeIn {
    to { opacity: 1; transform: translateY(0); }
  }

  .delay-1 { animation-delay: 0.1s; }
  .delay-2 { animation-delay: 0.2s; }
  .delay-3 { animation-delay: 0.3s; }
  .delay-4 { animation-delay: 0.4s; }
</style>
</head>
<body>
<div class="wrapper">

  <!-- HERO -->
  <div class="hero fade-in">
    <div>
      <div class="hero-status">
        <span></span> Open to opportunities
      </div>
      <h1>Abdelkader<br>Barhoumi</h1>
      <div class="hero-role">Mobile Software Engineer · Flutter Expert</div>
      <p class="hero-bio">
        Building scalable cross-platform applications that bridge hardware and software.
        Specializing in Flutter, embedded systems, and real-time architectures.
      </p>
      <div class="hero-meta">
        <span>📍 Tunis, Tunisia</span>
        <span>🎓 Mechatronics Eng.</span>
        <span>🗣️ AR · EN · FR</span>
        <span>⚡ 1,758 contributions</span>
      </div>
    </div>
    <div class="hero-links">
      <a href="https://www.linkedin.com/in/barhoumi23176/" class="hero-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>
        LinkedIn
      </a>
      <a href="https://github.com/AbdelkaderBarhoumi21" class="hero-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 00-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0020 4.77 5.07 5.07 0 0019.91 1S18.73.65 16 2.48a13.38 13.38 0 00-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 005 4.77a5.44 5.44 0 00-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 009 18.13V22"/></svg>
        GitHub
      </a>
      <a href="mailto:abdelkaderbarhoumi21@gmail.com" class="hero-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,12 2,6"/></svg>
        Email
      </a>
    </div>
  </div>

  <!-- ABOUT CODE BLOCK -->
  <section class="fade-in delay-1">
    <div class="section-label">// who i am</div>
    <div class="section-title">About Me</div>

    <div class="code-block">
      <div class="code-header">
        <div class="code-dot r"></div>
        <div class="code-dot y"></div>
        <div class="code-dot g"></div>
        <div class="code-filename">developer.dart</div>
      </div>
      <div class="code-body">
<span class="kw">class</span> <span class="cls">Developer</span> <span class="punct">{</span><br>
&nbsp;&nbsp;<span class="kw">final</span> <span class="cls">String</span> name <span class="punct">=</span> <span class="str">"Abdelkader Barhoumi"</span><span class="punct">;</span><br>
&nbsp;&nbsp;<span class="kw">final</span> <span class="cls">String</span> role <span class="punct">=</span> <span class="str">"Mobile Software Engineer"</span><span class="punct">;</span><br>
&nbsp;&nbsp;<span class="kw">final</span> <span class="cls">String</span> location <span class="punct">=</span> <span class="str">"Tunis, Tunisia 🇹🇳"</span><span class="punct">;</span><br><br>
&nbsp;&nbsp;<span class="kw">final</span> <span class="cls">List</span><span class="punct">&lt;</span><span class="cls">String</span><span class="punct">&gt;</span> currentlyWorkingOn <span class="punct">= [</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="str">"B2B e-commerce platform @ Stoneslane, Dubai"</span><span class="punct">,</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="str">"Healthcare appointment app @ Nexits, Paris"</span><span class="punct">,</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="str">"Open-source Flutter packages"</span><span class="punct">,</span><br>
&nbsp;&nbsp;<span class="punct">];</span><br><br>
&nbsp;&nbsp;<span class="kw">final</span> <span class="cls">Map</span><span class="punct">&lt;</span><span class="cls">String</span><span class="punct">, </span><span class="cls">List</span><span class="punct">&lt;</span><span class="cls">String</span><span class="punct">&gt;&gt;</span> expertise <span class="punct">= {</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="str">"Mobile"</span><span class="punct">:</span> <span class="punct">[</span><span class="str">"Flutter"</span><span class="punct">,</span> <span class="str">"Dart"</span><span class="punct">,</span> <span class="str">"Cross-Platform"</span><span class="punct">,</span> <span class="str">"BLE/IoT"</span><span class="punct">],</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="str">"Backend"</span><span class="punct">:</span> <span class="punct">[</span><span class="str">"Rust"</span><span class="punct">,</span> <span class="str">"Node.js"</span><span class="punct">,</span> <span class="str">"Laravel"</span><span class="punct">,</span> <span class="str">"WebSockets"</span><span class="punct">],</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="str">"Embedded"</span><span class="punct">:</span> <span class="punct">[</span><span class="str">"STM32"</span><span class="punct">,</span> <span class="str">"ESP32"</span><span class="punct">,</span> <span class="str">"nRF52"</span><span class="punct">,</span> <span class="str">"MQTT"</span><span class="punct">],</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="str">"Architecture"</span><span class="punct">:</span> <span class="punct">[</span><span class="str">"Clean Arch"</span><span class="punct">,</span> <span class="str">"BLoC"</span><span class="punct">,</span> <span class="str">"Riverpod"</span><span class="punct">,</span> <span class="str">"MVVM"</span><span class="punct">],</span><br>
&nbsp;&nbsp;<span class="punct">};</span><br><br>
&nbsp;&nbsp;<span class="kw">void</span> <span class="fn">sayHi</span><span class="punct">() =&gt;</span> <span class="fn">print</span><span class="punct">(</span><span class="str">"Let's build something amazing together!"</span><span class="punct">);</span><br>
<span class="punct">}</span>
      </div>
    </div>
  </section>

  <!-- GITHUB STATS -->
  <section class="fade-in delay-2">
    <div class="section-label">// by the numbers</div>
    <div class="section-title">GitHub Stats</div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-number">1,758</div>
        <div class="stat-label">Total Contributions</div>
        <div class="stat-sub">Jul 2024 – Present</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">33</div>
        <div class="stat-label">Longest Streak</div>
        <div class="stat-sub">Dec 15 – Jan 16</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">13</div>
        <div class="stat-label">Current Streak</div>
        <div class="stat-sub">Mar 1 – Mar 13</div>
      </div>
    </div>

    <div style="margin-top: 32px; background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 28px;">
      <div style="font-family:'Space Mono',monospace; font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:.1em; margin-bottom:20px;">Most Used Languages</div>
      <div class="lang-list">
        <div class="lang-item">
          <div class="lang-header"><span class="lang-name">C</span><span class="lang-pct">34.58%</span></div>
          <div class="lang-bar"><div class="lang-fill" style="width:34.58%; background: linear-gradient(90deg,#38BDF8,#818CF8); animation-delay:0.1s;"></div></div>
        </div>
        <div class="lang-item">
          <div class="lang-header"><span class="lang-name">C++</span><span class="lang-pct">27.78%</span></div>
          <div class="lang-bar"><div class="lang-fill" style="width:27.78%; background: linear-gradient(90deg,#818CF8,#A78BFA); animation-delay:0.2s;"></div></div>
        </div>
        <div class="lang-item">
          <div class="lang-header"><span class="lang-name">Makefile</span><span class="lang-pct">25.24%</span></div>
          <div class="lang-bar"><div class="lang-fill" style="width:25.24%; background: linear-gradient(90deg,#34D399,#38BDF8); animation-delay:0.3s;"></div></div>
        </div>
        <div class="lang-item">
          <div class="lang-header"><span class="lang-name">Rust</span><span class="lang-pct">4.79%</span></div>
          <div class="lang-bar"><div class="lang-fill" style="width:4.79%; background: linear-gradient(90deg,#FB923C,#F97316); animation-delay:0.4s;"></div></div>
        </div>
        <div class="lang-item">
          <div class="lang-header"><span class="lang-name">Dart</span><span class="lang-pct">1.42%</span></div>
          <div class="lang-bar"><div class="lang-fill" style="width:1.42%; background: linear-gradient(90deg,#38BDF8,#0284C7); animation-delay:0.5s;"></div></div>
        </div>
        <div class="lang-item">
          <div class="lang-header"><span class="lang-name">QML</span><span class="lang-pct">3.18%</span></div>
          <div class="lang-bar"><div class="lang-fill" style="width:3.18%; background: linear-gradient(90deg,#FBBF24,#F59E0B); animation-delay:0.6s;"></div></div>
        </div>
      </div>
    </div>
  </section>

  <!-- EXPERIENCE -->
  <section class="fade-in delay-2">
    <div class="section-label">// work history</div>
    <div class="section-title">Experience</div>

    <div class="exp-grid">
      <div class="exp-card">
        <div class="exp-badge badge-current">● Current</div>
        <div class="exp-company">Stoneslane 🇦🇪</div>
        <div class="exp-role">Mobile Engineer – Flutter</div>
        <div class="exp-period">Oct 2025 – Present · Full-time · Dubai</div>
        <ul class="exp-items">
          <li>B2B e-commerce platform</li>
          <li>Authentication & authorization</li>
          <li>Real-time order tracking</li>
          <li>CI/CD with Fastlane & Docker</li>
        </ul>
        <div class="exp-stack">
          <span class="tag">Flutter</span>
          <span class="tag">BLoC</span>
          <span class="tag">Firebase</span>
          <span class="tag">CI/CD</span>
        </div>
      </div>

      <div class="exp-card">
        <div class="exp-badge badge-current">● Current</div>
        <div class="exp-company">Nexits 🇫🇷</div>
        <div class="exp-role">Mobile Engineer – Flutter</div>
        <div class="exp-period">Oct 2025 – Present · Part-time · Paris</div>
        <ul class="exp-items">
          <li>Healthcare appointment app</li>
          <li>Patient profiles & records</li>
          <li>Role-based access control</li>
          <li>OpenAPI type-safe integration</li>
        </ul>
        <div class="exp-stack">
          <span class="tag">Flutter</span>
          <span class="tag">Riverpod</span>
          <span class="tag">OpenAPI</span>
          <span class="tag">Fastlane</span>
        </div>
      </div>

      <div class="exp-card">
        <div class="exp-badge badge-past">Past</div>
        <div class="exp-company">Capgemini Engineering</div>
        <div class="exp-role">Flutter Intern</div>
        <div class="exp-period">Feb – Jul 2025</div>
        <ul class="exp-items">
          <li>B2C e-commerce app</li>
          <li>Laravel REST API with JWT</li>
          <li>Qt/QML desktop dashboard</li>
        </ul>
        <div class="exp-stack">
          <span class="tag">Flutter</span>
          <span class="tag">Laravel</span>
          <span class="tag">Qt/QML</span>
          <span class="tag">PostgreSQL</span>
        </div>
      </div>

      <div class="exp-card">
        <div class="exp-badge badge-past">Past</div>
        <div class="exp-company">CMI Impianti</div>
        <div class="exp-role">Flutter Intern</div>
        <div class="exp-period">Jan – Jul 2024</div>
        <ul class="exp-items">
          <li>Robot teleoperation system</li>
          <li>WebSocket live telemetry</li>
          <li>Rust backend (Axum)</li>
        </ul>
        <div class="exp-stack">
          <span class="tag">Flutter</span>
          <span class="tag">Rust</span>
          <span class="tag">WebSockets</span>
          <span class="tag">MongoDB</span>
        </div>
      </div>
    </div>
  </section>

  <!-- SKILLS -->
  <section class="fade-in delay-3">
    <div class="section-label">// tech stack</div>
    <div class="section-title">Skills</div>

    <div class="skills-grid">
      <div class="skill-group">
        <div class="skill-group-title">📱 Mobile</div>
        <ul class="skill-list">
          <li>Flutter / Dart</li>
          <li>BLoC / Riverpod / GetX</li>
          <li>Clean Architecture</li>
          <li>Platform Channels</li>
        </ul>
      </div>
      <div class="skill-group">
        <div class="skill-group-title">⚙️ Backend</div>
        <ul class="skill-list">
          <li>Rust (Axum, Actix)</li>
          <li>Node.js / Express</li>
          <li>Laravel / PHP</li>
          <li>WebSockets / REST</li>
        </ul>
      </div>
      <div class="skill-group">
        <div class="skill-group-title">🗄️ Databases</div>
        <ul class="skill-list">
          <li>PostgreSQL / MySQL</li>
          <li>MongoDB</li>
          <li>Firebase Firestore</li>
          <li>Redis / SQLite</li>
        </ul>
      </div>
      <div class="skill-group">
        <div class="skill-group-title">🔌 Embedded / IoT</div>
        <ul class="skill-list">
          <li>STM32 / ESP32 / nRF52</li>
          <li>BLE · MQTT · Modbus</li>
          <li>FreeRTOS</li>
          <li>Qt / QML · C++</li>
        </ul>
      </div>
      <div class="skill-group">
        <div class="skill-group-title">🚀 DevOps</div>
        <ul class="skill-list">
          <li>Docker / CI/CD</li>
          <li>GitHub Actions</li>
          <li>Fastlane</li>
          <li>App Store / Play Store</li>
        </ul>
      </div>
      <div class="skill-group">
        <div class="skill-group-title">🧠 AI / ML</div>
        <ul class="skill-list">
          <li>TensorFlow Lite</li>
          <li>OpenCV</li>
          <li>LLM API Integration</li>
          <li>On-device inference</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- PROJECTS -->
  <section class="fade-in delay-3">
    <div class="section-label">// featured work</div>
    <div class="section-title">Projects</div>

    <div class="projects-list">
      <div class="project-card">
        <div>
          <div class="project-name">🛒 E-commerce Platform Suite</div>
          <div class="project-desc">Complete B2C/B2B solution with Admin, Delivery & Customer apps. Offline-first, 60 FPS animations, automated CI/CD pipeline.</div>
          <div class="exp-stack">
            <span class="tag">Flutter</span><span class="tag">BLoC</span><span class="tag">Laravel</span><span class="tag">PostgreSQL</span><span class="tag">Google Maps</span><span class="tag">Firebase</span>
          </div>
        </div>
      </div>

      <div class="project-card">
        <div>
          <div class="project-name">💬 Real-time Chat App</div>
          <div class="project-desc">Enterprise-grade messaging with group chats, read receipts, typing indicators, media sharing and E2E encryption ready.</div>
          <div class="exp-stack">
            <span class="tag">Flutter</span><span class="tag">Riverpod</span><span class="tag">Rust/Axum</span><span class="tag">WebSockets</span><span class="tag">MongoDB</span>
          </div>
        </div>
      </div>

      <div class="project-card">
        <div>
          <div class="project-name">🌱 Smart Irrigation & Plant Shop</div>
          <div class="project-desc">IoT-enabled agriculture with automated irrigation, soil moisture monitoring, and an integrated e-commerce plant shop.</div>
          <div class="exp-stack">
            <span class="tag">Flutter</span><span class="tag">ESP32</span><span class="tag">MQTT</span><span class="tag">Rust</span><span class="tag">Firebase</span>
          </div>
        </div>
      </div>

      <div class="project-card">
        <div>
          <div class="project-name">🤖 Robot Teleoperation System</div>
          <div class="project-desc">Industrial robot control with real-time telemetry, live video feed, multi-user roles, and secure operation logging.</div>
          <div class="exp-stack">
            <span class="tag">Flutter</span><span class="tag">Rust/Axum</span><span class="tag">WebSockets</span><span class="tag">Node.js</span><span class="tag">MongoDB</span>
          </div>
        </div>
      </div>

      <div class="project-card">
        <div>
          <div class="project-name">🤖 Gemini Chat App</div>
          <div class="project-desc">AI-powered chat interface with streaming responses, conversation history, syntax highlighting and secure local storage.</div>
          <div class="exp-stack">
            <span class="tag">Flutter</span><span class="tag">GetX</span><span class="tag">Gemini API</span><span class="tag">Encrypted Storage</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CERTIFICATIONS -->
  <section class="fade-in delay-3">
    <div class="section-label">// learning never stops</div>
    <div class="section-title">Certifications</div>

    <div class="certs-grid">
      <div class="cert-item">
        <div class="cert-icon">🤖</div>
        <div>
          <div class="cert-name">Claude Code in Action</div>
          <div class="cert-source">Anthropic · Jan 2026</div>
        </div>
      </div>
      <div class="cert-item">
        <div class="cert-icon">⚙️</div>
        <div>
          <div class="cert-name">CI/CD with Jenkins & Docker</div>
          <div class="cert-source">Udemy · Sep 2025</div>
        </div>
      </div>
      <div class="cert-item">
        <div class="cert-icon">🍃</div>
        <div>
          <div class="cert-name">MongoDB Developers Course</div>
          <div class="cert-source">Udemy · Sep 2025</div>
        </div>
      </div>
      <div class="cert-item">
        <div class="cert-icon">🟢</div>
        <div>
          <div class="cert-name">NodeJS Projects Bootcamp</div>
          <div class="cert-source">Udemy · Aug 2025</div>
        </div>
      </div>
      <div class="cert-item">
        <div class="cert-icon">🦀</div>
        <div>
          <div class="cert-name">Rust Programming Bootcamp</div>
          <div class="cert-source">Udemy · Jul 2025</div>
        </div>
      </div>
      <div class="cert-item">
        <div class="cert-icon">💙</div>
        <div>
          <div class="cert-name">Flutter & Firebase Chat App</div>
          <div class="cert-source">Udemy · Jun 2025</div>
        </div>
      </div>
      <div class="cert-item">
        <div class="cert-icon">🎨</div>
        <div>
          <div class="cert-name">Master Web & Mobile Design (Figma)</div>
          <div class="cert-source">Udemy · Apr 2025</div>
        </div>
      </div>
      <div class="cert-item">
        <div class="cert-icon">🌍</div>
        <div>
          <div class="cert-name">IELTS B2 + DELF B2</div>
          <div class="cert-source">British Council · Institut Français</div>
        </div>
      </div>
    </div>
  </section>

  <!-- EDUCATION -->
  <section class="fade-in delay-4">
    <div class="section-label">// academic background</div>
    <div class="section-title">Education</div>

    <div class="edu-grid">
      <div class="edu-card">
        <div class="edu-icon">🎓</div>
        <div class="edu-school">Polytech International</div>
        <div class="edu-degree">Engineering Cycle</div>
        <div class="edu-period" style="color:#94A3B8; font-size:12px;">Embedded Systems & Mobile Dev</div>
        <div class="edu-period">2022 – 2025</div>
      </div>
      <div class="edu-card">
        <div class="edu-icon">📚</div>
        <div class="edu-school">ISET Rades</div>
        <div class="edu-degree">Master's – Mechatronics</div>
        <div class="edu-period" style="color:#94A3B8; font-size:12px;">Mechatronics Engineering</div>
        <div class="edu-period">2022 – 2024</div>
      </div>
      <div class="edu-card">
        <div class="edu-icon">📖</div>
        <div class="edu-school">ISET Rades</div>
        <div class="edu-degree">Bachelor's – Electricity</div>
        <div class="edu-period" style="color:#94A3B8; font-size:12px;">Industrial Electricity</div>
        <div class="edu-period">2019 – 2022</div>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <div class="footer fade-in delay-4">
    <div style="font-family:'Space Mono',monospace; font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:.15em; margin-bottom:12px;">Let's build something great</div>
    <a href="mailto:abdelkaderbarhoumi21@gmail.com" class="footer-email">abdelkaderbarhoumi21@gmail.com</a>
    <br>
    <div style="display:flex; justify-content:center; gap:16px; margin-top:16px; flex-wrap:wrap;">
      <a href="https://www.linkedin.com/in/barhoumi23176/" class="hero-link" style="font-size:12px;">LinkedIn</a>
      <a href="https://github.com/AbdelkaderBarhoumi21" class="hero-link" style="font-size:12px;">GitHub</a>
    </div>
    <div class="footer-quote">"First, solve the problem. Then, write the code." — John Johnson</div>
    <div style="margin-top:32px; font-family:'Space Mono',monospace; font-size:11px; color:#1E293B;">
      Built with ❤️ · Abdelkader Barhoumi 2026
    </div>
  </div>

</div>
</body>
</html>
