/* Base Design Tokens */
:root {
    --bg-primary: #0b0f19;
    --bg-secondary: #121826;
    
    /* Glassmorphism settings */
    --glass-bg: rgba(18, 24, 38, 0.65);
    --glass-border: rgba(255, 255, 255, 0.06);
    --glass-hover-bg: rgba(255, 255, 255, 0.03);
    
    /* Color Palette */
    --primary: #6366f1;       /* Indigo */
    --primary-glow: rgba(99, 102, 241, 0.15);
    --secondary: #10b981;     /* Emerald */
    --secondary-glow: rgba(16, 185, 129, 0.15);
    --blue: #3b82f6;          /* Bright Blue */
    --blue-glow: rgba(59, 130, 246, 0.15);
    --amber: #f59e0b;         /* Amber */
    --amber-glow: rgba(245, 158, 11, 0.15);
    
    /* Text Colors */
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    /* Borders & Rounding */
    --border-radius-sm: 8px;
    --border-radius-md: 12px;
    --border-radius-lg: 16px;
    --border-radius-xl: 24px;
    --border-color: rgba(255, 255, 255, 0.08);
    
    /* Transitions */
    --transition-fast: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-normal: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Base resets & document settings */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
}

/* Background Ambient Orbs */
.bg-glow {
    position: fixed;
    border-radius: 50%;
    filter: blur(140px);
    z-index: -1;
    pointer-events: none;
    opacity: 0.45;
}

.bg-glow-1 {
    width: 500px;
    height: 500px;
    top: -100px;
    left: -100px;
    background: radial-gradient(circle, var(--primary) 0%, rgba(99, 102, 241, 0) 70%);
}

.bg-glow-2 {
    width: 600px;
    height: 600px;
    bottom: -150px;
    right: -100px;
    background: radial-gradient(circle, var(--secondary) 0%, rgba(16, 185, 129, 0) 70%);
}

.bg-glow-3 {
    width: 400px;
    height: 400px;
    top: 30%;
    left: 40%;
    background: radial-gradient(circle, var(--blue) 0%, rgba(59, 130, 246, 0) 70%);
    opacity: 0.25;
}

/* Glassmorphic Panel Layout */
.glass-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    transition: transform var(--transition-normal), border-color var(--transition-fast), box-shadow var(--transition-normal);
}

.glass-card:hover {
    border-color: rgba(255, 255, 255, 0.12);
}

/* Application Layout grid */
.app-container {
    display: grid;
    grid-template-columns: 260px 1fr;
    min-height: 100vh;
}

/* Sidebar Navigation */
.sidebar {
    background: rgba(11, 15, 25, 0.85);
    border-right: 1px solid var(--border-color);
    padding: 2.5rem 1.5rem;
    display: flex;
    flex-direction: column;
    height: 100vh;
    position: sticky;
    top: 0;
}

.brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 3rem;
}

.brand-icon {
    background: linear-gradient(135deg, var(--primary) 0%, var(--blue) 100%);
    width: 40px;
    height: 40px;
    border-radius: var(--border-radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.brand h2 {
    font-size: 1.5rem;
    background: linear-gradient(to right, #ffffff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

.nav-menu {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex-grow: 1;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: var(--text-secondary);
    text-decoration: none;
    padding: 0.85rem 1rem;
    border-radius: var(--border-radius-md);
    font-weight: 500;
    transition: var(--transition-fast);
}

.nav-item i {
    width: 20px;
    height: 20px;
    transition: transform var(--transition-fast);
}

.nav-item:hover {
    color: var(--text-primary);
    background: var(--glass-hover-bg);
}

.nav-item:hover i {
    transform: translateX(3px);
}

.nav-item.active {
    color: var(--text-primary);
    background: var(--primary-glow);
    border: 1px solid rgba(99, 102, 241, 0.25);
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.05);
}

.sidebar-footer {
    border-top: 1px solid var(--border-color);
    padding-top: 1.5rem;
    font-size: 0.75rem;
    color: var(--text-muted);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.badge {
    background: rgba(16, 185, 129, 0.1);
    color: var(--secondary);
    border: 1px solid rgba(16, 185, 129, 0.2);
    padding: 2px 8px;
    border-radius: 20px;
    width: fit-content;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Main Content Dashboard Area */
.main-content {
    padding: 2.5rem;
    overflow-y: auto;
}

/* Top Header & Filter Bar */
.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
}

.header-title h1 {
    font-size: 2.25rem;
    letter-spacing: -0.5px;
}

.header-title .subtitle {
    color: var(--primary);
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 0.25rem;
    display: block;
}

.filter-panel {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 0.75rem 1.5rem;
}

.filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.filter-group label {
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.filter-group label i {
    width: 12px;
    height: 12px;
}

.custom-select {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.4rem 1.5rem 0.4rem 0.75rem;
    border-radius: var(--border-radius-sm);
    font-size: 0.85rem;
    outline: none;
    cursor: pointer;
    transition: var(--transition-fast);
    appearance: none;
    -webkit-appearance: none;
    background-image: url("data:image/svg+xml;utf8,<svg fill='white' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
    background-repeat: no-repeat;
    background-position: right 4px center;
    background-size: 16px;
}

.custom-select:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px var(--primary-glow);
}

.select-sm {
    padding: 0.25rem 1.5rem 0.25rem 0.5rem;
    font-size: 0.8rem;
}

.custom-input {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 0.5rem 0.75rem;
    border-radius: var(--border-radius-sm);
    font-size: 0.85rem;
    outline: none;
    transition: var(--transition-fast);
}

.custom-input:focus {
    border-color: var(--primary);
}

/* Button components */
.btn {
    background: var(--primary);
    color: #fff;
    border: none;
    padding: 0.5rem 1.25rem;
    border-radius: var(--border-radius-sm);
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: var(--transition-fast);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.btn:hover {
    background: #4f46e5;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    transform: translateY(-1px);
}

.btn:active {
    transform: translateY(0);
}

.btn-secondary {
    background: rgba(255, 255, 255, 0.08);
    color: var(--text-primary);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-secondary:hover {
    background: rgba(255, 255, 255, 0.12);
    box-shadow: none;
}

.btn-sm {
    padding: 0.35rem 0.75rem;
    font-size: 0.8rem;
}

.btn-icon-only {
    padding: 0.5rem;
    justify-content: center;
    align-items: center;
}

/* View Pages */
.page-view {
    display: none;
    animation: fadeIn var(--transition-normal);
}

.page-view.active {
    display: block;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* KPI Summary Grid */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2.5rem;
}

.kpi-card {
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
}

.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45);
}

.kpi-icon {
    width: 48px;
    height: 48px;
    border-radius: var(--border-radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
}

.kpi-icon i {
    width: 24px;
    height: 24px;
}

.icon-blue {
    background: var(--blue-glow);
    color: var(--blue);
    border: 1px solid rgba(59, 130, 246, 0.15);
}

.icon-emerald {
    background: var(--secondary-glow);
    color: var(--secondary);
    border: 1px solid rgba(16, 185, 129, 0.15);
}

.icon-indigo {
    background: var(--primary-glow);
    color: var(--primary);
    border: 1px solid rgba(99, 102, 241, 0.15);
}

.icon-amber {
    background: var(--amber-glow);
    color: var(--amber);
    border: 1px solid rgba(245, 158, 11, 0.15);
}

.kpi-details h3 {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.25rem;
}

.kpi-value-container {
    display: flex;
    align-items: baseline;
    gap: 0.25rem;
}

.kpi-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.kpi-unit {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-secondary);
}

.kpi-desc {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 0.25rem;
}

/* Visualization Panel */
.charts-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2.5rem;
}

@media (max-width: 1024px) {
    .charts-grid {
        grid-template-columns: 1fr;
    }
}

.chart-card {
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-color);
}

.chart-header-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.chart-header-left i {
    width: 20px;
    height: 20px;
}

.chart-header h3 {
    font-size: 1.1rem;
    font-weight: 600;
}

.chart-metric-info {
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 500;
}

.chart-body {
    position: relative;
    width: 100%;
    min-height: 280px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.text-blue { color: var(--blue); }
.text-emerald { color: var(--secondary); }

/* Table Panels */
.table-section {
    padding: 1.5rem;
}

.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.25rem;
    gap: 1rem;
    flex-wrap: wrap;
}

.table-header-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.table-header-left i {
    width: 20px;
    height: 20px;
    color: var(--primary);
}

.table-header h3 {
    font-size: 1.1rem;
    font-weight: 600;
}

.table-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.search-box {
    position: relative;
    display: flex;
    align-items: center;
}

.search-box i {
    position: absolute;
    left: 10px;
    width: 16px;
    height: 16px;
    color: var(--text-muted);
}

.search-box input {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-sm);
    color: var(--text-primary);
    padding: 0.4rem 0.75rem 0.4rem 2rem;
    font-size: 0.85rem;
    outline: none;
    transition: var(--transition-fast);
    width: 200px;
}

.search-box input:focus {
    border-color: var(--primary);
    width: 260px;
}

.table-container {
    overflow-x: auto;
    width: 100%;
}

.data-grid {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.data-grid th {
    color: var(--text-secondary);
    font-weight: 600;
    padding: 0.85rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.data-grid td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    color: var(--text-primary);
    font-size: 0.85rem;
    transition: var(--transition-fast);
}

.data-grid tr:last-child td {
    border-bottom: none;
}

.data-grid tbody tr:hover td {
    background: rgba(255, 255, 255, 0.02);
}

.text-right {
    text-align: right;
}

.text-sm {
    font-size: 0.8rem;
}

.loading-state {
    text-align: center;
    color: var(--text-muted);
    padding: 3rem !important;
    font-style: italic;
}

.no-records {
    text-align: center;
    color: var(--text-muted);
    padding: 2rem !important;
}

/* Detail view specific */
.full-table-section {
    min-height: calc(100vh - 12rem);
}

/* Status Pipeline Section */
.status-section {
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
}

.status-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-color);
}

.status-header h3 {
    font-size: 1.25rem;
}

.status-header i {
    width: 24px;
    height: 24px;
}

.status-body {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.02);
    padding: 1rem 1.5rem;
    border-radius: var(--border-radius-md);
    border: 1px solid var(--border-color);
}

.status-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.status-dot.online {
    background-color: var(--secondary);
    box-shadow: 0 0 12px var(--secondary);
}

.status-dot.busy {
    background-color: var(--amber);
    box-shadow: 0 0 12px var(--amber);
}

.status-info h4 {
    font-size: 0.95rem;
    margin-bottom: 0.15rem;
}

.status-info p {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.pipeline-actions h4 {
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.pipeline-actions .desc {
    color: var(--text-secondary);
    font-size: 0.85rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

.year-selector-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid var(--border-color);
    padding: 1.25rem;
    border-radius: var(--border-radius-md);
}

.year-selector-card h4 {
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}

.year-selector-card p {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.sync-controls {
    display: flex;
    gap: 1rem;
}

.sync-controls input {
    width: 100px;
}

.log-console-container h4 {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

#log-console {
    background: #05070c;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius-sm);
    color: #38bdf8;
    padding: 1rem;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.75rem;
    line-height: 1.4;
    white-space: pre-wrap;
    height: 180px;
    overflow-y: auto;
}

/* Scrollbar Customization */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.18);
}

/* Responsive Overrides */
@media (max-width: 768px) {
    .app-container {
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        height: auto;
        padding: 1rem 1.5rem;
        position: relative;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
    }
    
    .brand {
        margin-bottom: 1rem;
    }
    
    .nav-menu {
        flex-direction: row;
        gap: 0.25rem;
        overflow-x: auto;
        padding-bottom: 0.5rem;
    }
    
    .nav-item {
        padding: 0.5rem 0.75rem;
        font-size: 0.8rem;
    }
    
    .top-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .filter-panel {
        width: 100%;
        justify-content: space-between;
    }
    
    .main-content {
        padding: 1.5rem;
    }
}

/* Spinner Animation & Badge Styles */
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.spin {
    animation: spin 1.2s linear infinite;
    display: inline-block;
}

.badge-scheduled {
    background: rgba(59, 130, 246, 0.12) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(59, 130, 246, 0.25) !important;
}

.badge-nonscheduled {
    background: rgba(139, 92, 246, 0.12) !important;
    color: #a78bfa !important;
    border: 1px solid rgba(139, 92, 246, 0.25) !important;
}

