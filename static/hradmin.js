// ============================================================
// admin.js - JHS HR Help Desk Admin Panel
// ============================================================

// API Configuration
const API_URL = '/api/tickets';
const API_ADMIN = '/api/admin';

// HR Mapping
// const HR_MAPPING = {
//     'Unassigned': '', 
//     'Janhavi Gamare': 'janhavi.gamare@jhsassociatesllp.in', 
//     'Darshan Shah': 'darshan.shah@jhsassociates.in', 
//     'Krutika Shivshivkar': 'krutika.shivshivkar@jhsassociates.in', 
//     'Fiza Kudalkar': 'fiza.kudalkar@jhsassociates.in'
// };

// Global variables
let hrChart = null;
let initialized = false;
let currentTicket = null;
let pendingAction = null;
let pendingTicketId = null;
let currentPage = 1;
const itemsPerPage = 10;
let filteredTickets = [];

// ==========================
// Prevent Back Button After Logout
// ==========================
(function() {
    if (!localStorage.getItem('adminToken')) {
        window.location.replace('/adminlogin');
    }
    window.history.replaceState(null, '', window.location.href);
    window.addEventListener('pageshow', (event) => {
        if (event.persisted || window.performance && performance.getEntriesByType("navigation")[0].type === "back_forward") {
            if (!localStorage.getItem('adminToken')) {
                window.location.replace('/adminlogin');
            }
        }
    });
})();

// ==========================
// Utility Functions
// ==========================
function escapeHtml(text) {
    if (!text) return '';
    return String(text).replace(/[&<>"']/g, m => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[m]);
}

function fmtDateIsoToIST(d) {
    if (!d) return '-';
    try {
        const date = new Date(d + 'Z');
        return date.toLocaleString('en-IN', { 
            timeZone: 'Asia/Kolkata',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    } catch {
        return d;
    }
}

function parseDate(d) {
    if (!d) return null;
    // If already has timezone info (Z, +, or offset), parse directly
    if (/Z|[+-]\d{2}:\d{2}$/.test(d)) return new Date(d);
    // If has a space instead of T (e.g. "2026-01-15 09:40:00"), normalize it
    const normalized = d.replace(' ', 'T');
    // Try appending Z only if no timezone present
    const dt = new Date(normalized + 'Z');
    if (!isNaN(dt)) return dt;
    // Fallback: parse as-is
    return new Date(d);
}

function calcResolutionTime(assignedAt, closedAt) {
    if (!assignedAt || !closedAt) return '-';
    try {
        const start = parseDate(assignedAt);
        const end = parseDate(closedAt);
        if (!start || !end || isNaN(start) || isNaN(end)) return '-';
        const diffMs = end - start;
        if (diffMs < 0) return '-';

        const totalMins = Math.floor(diffMs / 60000);
        const days = Math.floor(totalMins / 1440);
        const hours = Math.floor((totalMins % 1440) / 60);
        const mins = totalMins % 60;

        let parts = [];
        if (days > 0) parts.push(`${days}d`);
        if (hours > 0) parts.push(`${hours}h`);
        if (mins > 0 || parts.length === 0) parts.push(`${mins}m`);
        return parts.join(' ');
    } catch {
        return '-';
    }
}

function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}

function authFetch(url, options = {}) {
    const token = localStorage.getItem('adminToken');
    if (!token) {
        logoutAdmin();
        return;
    }
    return fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...(options.headers || {})
        }
    });
}

// ==========================
// Logout
// ==========================
function logoutAdmin() {
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminLoggedIn');
    window.location.replace('/adminlogin');
}

// ==========================
// DOMContentLoaded
// ==========================
document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('adminToken')) {
        window.location.replace('/adminlogin');
        return;
    }

    if (initialized) return;
    initialized = true;

    // Section Buttons
    document.getElementById('btnAnalysis')?.addEventListener('click', () => showSection('analysis'));
    document.getElementById('btnTickets')?.addEventListener('click', () => showSection('tickets'));
    document.getElementById('btnClose')?.addEventListener('click', () => showSection('closed'));
    document.getElementById('btnAssign')?.addEventListener('click', () => showSection('assign'));

    // Filters
    document.getElementById('btnRefresh')?.addEventListener('click', resetFiltersAndReload);
    document.getElementById('btnDownloadExcel')?.addEventListener('click', downloadExcel);
    document.getElementById('searchInput')?.addEventListener('input', debounce(loadTickets, 300));
    document.getElementById('fromDate')?.addEventListener('change', loadTickets);
    document.getElementById('toDate')?.addEventListener('change', loadTickets);
    document.getElementById('statusFilter')?.addEventListener('change', loadTickets);

    // Close Section
    document.getElementById('btnFetch')?.addEventListener('click', fetchTicketDetails);
    document.getElementById('btnMarkClosed')?.addEventListener('click', () => {
        if (!currentTicket?.id) return;
        const remark = document.getElementById('closeRemark')?.value.trim();
        if (!remark) {
            alert(' Remark is mandatory to close the ticket');
            return;
        }
        showConfirm('Close Ticket', `Do you really want to CLOSE ticket <strong>${currentTicket.id}</strong>?`, 'close');
    });

    // Assign Section
    setupAssignSection();

    // Confirmation popup
    document.getElementById('popupNo')?.addEventListener('click', () => handleConfirm(false));
    document.getElementById('popupYes')?.addEventListener('click', () => handleConfirm(true));
    document.getElementById('confirmPopup')?.addEventListener('click', (e) => {
        if (e.target.id === 'confirmPopup') hideConfirm();
    });

    // Logout Popup
    setupLogoutPopup();

    // Initial load
    showSection('tickets');
    loadTickets();
    loadStats();
});

// ==========================
// Section Management
// ==========================
function showSection(id) {
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    const el = document.getElementById(id);
    if (el) el.classList.remove('hidden');
    if (id === 'analysis') loadStats();
    if (id === 'tickets') loadTickets();
}

// ==========================
// Reset Filters
// ==========================
function resetFiltersAndReload() {
    document.getElementById('searchInput').value = '';
    document.getElementById('fromDate').value = '';
    document.getElementById('toDate').value = '';
    document.getElementById('statusFilter').value = 'All status';
    currentPage = 1;
    loadTickets();
}

// ==========================
// Tickets Management
// ==========================
async function loadTickets() {
    const tbody = document.getElementById('ticketBody');
    if (!tbody) return;

    tbody.innerHTML = '<tr><td colspan="15" style="text-align:center;padding:3rem">🔄 Loading tickets...</td></tr>';

    try {
        const res = await authFetch(API_URL);
        if (!res.ok) throw new Error('Failed to fetch');
        let tickets = await res.json();

        const q = document.getElementById('searchInput')?.value.toLowerCase() || '';
        const statusFilter = document.getElementById('statusFilter')?.value;
        const fromDate = document.getElementById('fromDate')?.value;
        const toDate = document.getElementById('toDate')?.value;

        const map = new Map();
        tickets.forEach(t => map.set(t.id, t));
        tickets = Array.from(map.values());

        if (fromDate || toDate) {
            const from = fromDate ? new Date(fromDate) : new Date(0);
            const to = toDate ? new Date(toDate) : new Date();
            to.setHours(23, 59, 59, 999);
            tickets = tickets.filter(t => {
                const created = new Date(t.createdAt);
                return created >= from && created <= to;
            });
        }

        if (statusFilter && statusFilter !== 'All status') {
            tickets = tickets.filter(t => t.status?.toLowerCase() === statusFilter.toLowerCase());
        }

        if (q) {
            tickets = tickets.filter(t =>
                t.id.toLowerCase().includes(q) ||
                t.name.toLowerCase().includes(q) ||
                t.email.toLowerCase().includes(q) ||
                t.category.toLowerCase().includes(q) ||
                t.issue?.toLowerCase().includes(q)
            );
        }

        if (!tickets.length) {
            tbody.innerHTML = '<tr><td colspan="15" style="text-align:center;padding:3rem;color:#64748b">📭 No tickets found</td></tr>';
            return;
        }

        filteredTickets = tickets;
        // Debug: log first ticket's date fields to console so you can verify format
        if (tickets.length > 0) {
            console.log('[DEBUG] Sample ticket dates:', {
                assignedAt: tickets[0].assignedAt,
                closedAt: tickets[0].closedAt,
                createdAt: tickets[0].createdAt
            });
        }
        renderPaginatedTable();
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="15" style="text-align:center;padding:3rem;color:#ef4444">❌ Error loading tickets</td></tr>';
        console.error(e);
    }
}

// ==========================
// Render Table & Pagination
// ==========================
function renderPaginatedTable() {
    const tbody = document.getElementById('ticketBody');
    const start = (currentPage - 1) * itemsPerPage;
    const pageItems = filteredTickets.slice(start, start + itemsPerPage);

    tbody.innerHTML = pageItems
        .map(t => {
            const statusBadge = t.status?.toLowerCase() === "open"
                ? '<span class="status-open">Open</span>'
                : '<span class="status-closed">Closed</span>';

            const resolutionTime = calcResolutionTime(t.assignedAt, t.closedAt);
            const resolutionClass = resolutionTime !== '-' ? 'resolution-time' : 'resolution-na';

            return `
                <tr>
                    <td><strong>${escapeHtml(t.id)}</strong></td>
                    <td>${escapeHtml(t.name)}</td>
                    <td>${escapeHtml(t.email)}</td>
                    <td>${escapeHtml(t.phone) || '-'}</td>
                    <td>${escapeHtml(t.empCode) || '-'}</td>
                    <td>${escapeHtml(t.category)}</td>
                    <td title="${escapeHtml(t.issue)}">${escapeHtml(t.issue?.slice(0,60))}...</td>
                    <td>${statusBadge}</td>
                    <td>${escapeHtml(t.assigned || "Unassigned")}</td>
                    <td>${fmtDateIsoToIST(t.createdAt)}</td>
                    <td>${fmtDateIsoToIST(t.assignedAt)}</td>
                    <td>${fmtDateIsoToIST(t.closedAt)}</td>
                    <td><span class="${resolutionClass}">${resolutionTime}</span></td>
                    <td title="${escapeHtml(t.remark || '')}">${escapeHtml(t.remark?.slice(0,30) || '-')}</td>
                    <td><button class="delete-btn" onclick="deleteTicket('${escapeHtml(t.id)}')">DELETE</button></td>
                </tr>
            `;
        }).join("");

    renderPaginationButtons();
}

function renderPaginationButtons() {
    const pagination = document.getElementById("pagination");
    const totalPages = Math.ceil(filteredTickets.length / itemsPerPage);

    let html = `<button ${currentPage === 1 ? "disabled" : ""} onclick="changePage(${currentPage - 1})">← Prev</button>`;
    for (let i = 1; i <= totalPages; i++) {
        html += `<button class="${currentPage === i ? "active" : ""}" onclick="changePage(${i})">${i}</button>`;
    }
    html += `<button ${currentPage === totalPages ? "disabled" : ""} onclick="changePage(${currentPage + 1})">Next →</button>`;
    pagination.innerHTML = html;
}

function changePage(page) {
    const totalPages = Math.ceil(filteredTickets.length / itemsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderPaginatedTable();
}

async function deleteTicket(id) {
    if (!confirm(` Are you sure you want to delete ticket ${id}?`)) return;
    try {
        const res = await authFetch(`${API_URL}/${id}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('Delete failed');
        loadTickets();
        loadStats();
    } catch (e) {
        alert(` Delete failed: ${e.message}`);
    }
}

// ==========================
// Close Ticket Functions
// ==========================
async function fetchTicketDetails() {
    const ticketId = document.getElementById('ticketIdInput')?.value.trim();
    const details = document.getElementById('ticketDetails');
    const msg = document.getElementById('closedMsg');

    if (!ticketId) {
        msg.textContent = ' Please enter a ticket ID';
        msg.className = 'msg-error';
        return;
    }

    msg.textContent = '';

    try {
        const res = await authFetch(`${API_URL}/${ticketId}`);
        if (!res.ok) throw new Error('Ticket not found');

        currentTicket = await res.json();

        document.getElementById('ticketName').textContent = currentTicket.name;
        document.getElementById('ticketEmail').textContent = currentTicket.email;
        document.getElementById('ticketIssue').textContent = currentTicket.issue;
        document.getElementById('ticketCreatedAt').textContent = fmtDateIsoToIST(currentTicket.createdAt);
        document.getElementById('ticketAssigned').textContent = currentTicket.assigned || 'Unassigned';
        document.getElementById('ticketAssignedAt').textContent = fmtDateIsoToIST(currentTicket.assignedAt);
        document.getElementById('ticketClosedAt').textContent = fmtDateIsoToIST(currentTicket.closedAt);

        document.getElementById('closeRemark').value = '';
        details.classList.remove('hidden');

    } catch (e) {
        msg.textContent = ' Ticket not found';
        msg.className = 'msg-error';
        details.classList.add('hidden');
    }
}

async function markTicketClosed() {
    if (!currentTicket?.id) return;
    const remark = document.getElementById('closeRemark')?.value.trim();

    try {
        const res = await authFetch(`${API_URL}/${currentTicket.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'Closed', remark })
        });

        if (!res.ok) throw new Error('Close failed');

        const msg = document.getElementById('closedMsg');
        msg.textContent = ` Ticket ${currentTicket.id} closed successfully & user notified!`;
        msg.className = 'msg-success';

        document.getElementById('closeRemark').value = '';
        document.getElementById('ticketIdInput').value = '';
        document.getElementById('ticketDetails').classList.add('hidden');
        currentTicket = null;

        loadTickets();
        loadStats();

    } catch (e) {
        const msg = document.getElementById('closedMsg');
        msg.textContent = ` Error: ${e.message}`;
        msg.className = 'msg-error';
    }
}

// ==========================
// Assign Section
// ==========================
function setupAssignSection() {
    const nameSelect = document.getElementById('assignHrName');
    const emailSelect = document.getElementById('assignHrEmail');
    if (!nameSelect || !emailSelect) return;

    nameSelect.innerHTML = '<option value="">Select HR Name</option>' +
        Object.keys(HR_MAPPING).map(name =>
            `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`
        ).join('');

    emailSelect.innerHTML = '<option value="">Select Email</option>';
    Object.entries(HR_MAPPING).forEach(([name, email]) => {
        if (email) emailSelect.innerHTML += `<option value="${escapeHtml(email)}" data-name="${escapeHtml(name)}">${escapeHtml(email)}</option>`;
    });

    nameSelect.addEventListener('change', () => {
        const name = nameSelect.value;
        const email = HR_MAPPING[name] || '';
        emailSelect.value = email;
        emailSelect.disabled = !email || name === 'Unassigned';
    });

    emailSelect.addEventListener('change', () => {
        const selectedEmail = emailSelect.value;
        const matchingName = Object.keys(HR_MAPPING).find(name => HR_MAPPING[name] === selectedEmail);
        if (matchingName && !nameSelect.value) {
            nameSelect.value = matchingName;
        }
    });

    document.getElementById('assignSaveBtn')?.addEventListener('click', () => {
        const ticketId = document.getElementById('assignTicketId')?.value.trim();
        const hrName = document.getElementById('assignHrName')?.value;
        const hrEmail = document.getElementById('assignHrEmail')?.value;
        const msg = document.getElementById('assignMsg');

        if (!ticketId || !hrName) {
            msg.textContent = ' Ticket ID & HR Name are required';
            msg.className = 'msg-error';
            return;
        }

        if (hrName !== 'Unassigned' && HR_MAPPING[hrName] !== hrEmail) {
            msg.textContent = 'Email must match selected HR name';
            msg.className = 'msg-error';
            return;
        }

        showConfirm(
            'Assign Ticket',
            `Assign ticket <strong>${escapeHtml(ticketId)}</strong> to <strong>${escapeHtml(hrName)}</strong>?`,
            'assign',
            ticketId
        );
    });
}

async function saveAssignment() {
    const ticketId = pendingTicketId;
    const hrName = document.getElementById('assignHrName')?.value;
    const hrEmail = document.getElementById('assignHrEmail')?.value;
    const msg = document.getElementById('assignMsg');

    try {
        const res = await authFetch(`${API_URL}/${ticketId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ assigned: hrName, status: 'Open', hrEmail })
        });

        if (!res.ok) throw new Error('Assignment failed');

        msg.textContent = ' Ticket assigned successfully & emails sent!';
        msg.className = 'msg-success';

        document.getElementById('assignTicketId').value = '';
        document.getElementById('assignHrName').value = '';
        document.getElementById('assignHrEmail').value = '';

        loadTickets();
        loadStats();

    } catch (e) {
        msg.textContent = ` Error: ${e.message}`;
        msg.className = 'msg-error';
    }
}


// ==========================
// Chart instance registry
// ==========================
const chartRegistry = {};

function destroyChart(id) {
    if (chartRegistry[id]) {
        chartRegistry[id].destroy();
        delete chartRegistry[id];
    }
}

// ==========================
// Stats & Analytics
// ==========================
async function loadStats() {
    try {
        const res = await authFetch(`${API_ADMIN}/stats`);
        if (res.ok) {
            const data = await res.json();
            const res2 = await authFetch(API_URL);
            const tickets = res2.ok ? await res2.json() : [];
            updateStats(data, tickets);
            return;
        }
    } catch { }
    buildStatsFallback();
}

async function buildStatsFallback() {
    try {
        const res = await authFetch(API_URL);
        if (!res.ok) return;
        const tickets = await res.json();
        const stats = { total: tickets.length, bystatus: {}, byhr: {} };
        tickets.forEach(t => {
            const status = t.status || 'Unknown';
            const hr = t.assigned || 'Unassigned';
            stats.bystatus[status] = (stats.bystatus[status] || 0) + 1;
            if (!stats.byhr[hr]) stats.byhr[hr] = { Open: 0, Closed: 0 };
            stats.byhr[hr][status] = (stats.byhr[hr][status] || 0) + 1;
        });
        updateStats(stats, tickets);
    } catch (e) {
        console.error('Failed to build stats:', e);
    }
}

function updateStats(data, tickets = []) {
    const total = data.total || 0;
    const open  = data.bystatus?.Open || 0;
    const closed = data.bystatus?.Closed || 0;

    document.getElementById('totalTickets').textContent = total;
    document.getElementById('openTickets').textContent  = open;
    document.getElementById('closedTickets').textContent = closed;

    // Avg resolution time KPI
    const resolvedTickets = tickets.filter(t => t.assignedAt && t.closedAt);
    let avgMins = 0;
    if (resolvedTickets.length > 0) {
        const totalMins = resolvedTickets.reduce((sum, t) => {
            const start = parseDate(t.assignedAt);
            const end   = parseDate(t.closedAt);
            if (!start || !end || isNaN(start) || isNaN(end)) return sum;
            return sum + Math.max(0, Math.floor((end - start) / 60000));
        }, 0);
        avgMins = Math.round(totalMins / resolvedTickets.length);
    }
    const avgEl = document.getElementById('avgResolutionTime');
    if (avgEl) {
        if (avgMins === 0) {
            avgEl.textContent = '-';
        } else {
            const d = Math.floor(avgMins / 1440);
            const h = Math.floor((avgMins % 1440) / 60);
            const m = avgMins % 60;
            avgEl.textContent = d > 0 ? `${d}d ${h}h` : h > 0 ? `${h}h ${m}m` : `${m}m`;
        }
    }

    // Resolution rate KPI
    const rateEl = document.getElementById('resolutionRate');
    if (rateEl) rateEl.textContent = total > 0 ? `${Math.round((closed / total) * 100)}%` : '0%';

    // Draw all 6 charts
    drawHRChart(data.byhr || {});
    drawStatusDonut(open, closed);
    drawMonthlyVolumeChart(tickets);
    drawResolutionTimeChart(tickets);
    drawCategoryChart(tickets);
    drawHRResolutionAvgChart(tickets);
}

// ---- Chart 1: HR Open vs Closed (grouped bar) ----
function drawHRChart(byhr) {
    const canvas = document.getElementById('hrChart');
    if (!canvas || !byhr || typeof Chart === 'undefined') return;
    destroyChart('hrChart');
    const labels = Object.keys(byhr);
    chartRegistry['hrChart'] = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels,
            datasets: [
                { label: 'Open',   data: labels.map(l => byhr[l].Open   || 0), backgroundColor: 'rgba(239,68,68,0.85)',  borderRadius: 8, borderSkipped: false },
                { label: 'Closed', data: labels.map(l => byhr[l].Closed || 0), backgroundColor: 'rgba(16,185,129,0.85)', borderRadius: 8, borderSkipped: false }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                title:  { display: true, text: 'Tickets by HR — Open vs Closed', font: { size: 15, weight: 'bold' } }
            },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
}

// ---- Chart 2: Status Doughnut ----
function drawStatusDonut(open, closed) {
    const canvas = document.getElementById('statusDonut');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart('statusDonut');
    chartRegistry['statusDonut'] = new Chart(canvas.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Open', 'Closed'],
            datasets: [{
                data: [open, closed],
                backgroundColor: ['rgba(239,68,68,0.85)', 'rgba(16,185,129,0.85)'],
                borderWidth: 3, borderColor: '#fff', hoverOffset: 8
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            cutout: '68%',
            plugins: {
                legend: { position: 'bottom' },
                title:  { display: true, text: 'Ticket Status Distribution', font: { size: 15, weight: 'bold' } }
            }
        }
    });
}

// ---- Chart 3: Monthly Ticket Volume (grouped bar) ----
function drawMonthlyVolumeChart(tickets) {
    const canvas = document.getElementById('monthlyVolumeChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart('monthlyVolumeChart');

    const monthMap = {};
    tickets.forEach(t => {
        if (!t.createdAt) return;
        const d = parseDate(t.createdAt);
        if (!d || isNaN(d)) return;
        const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
        if (!monthMap[key]) monthMap[key] = { Open: 0, Closed: 0 };
        const s = t.status || 'Open';
        monthMap[key][s] = (monthMap[key][s] || 0) + 1;
    });

    const sortedKeys = Object.keys(monthMap).sort();
    const labels = sortedKeys.map(k => {
        const [y, m] = k.split('-');
        return new Date(+y, +m - 1).toLocaleString('en-IN', { month: 'short', year: '2-digit' });
    });

    chartRegistry['monthlyVolumeChart'] = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels,
            datasets: [
                { label: 'Open',   data: sortedKeys.map(k => monthMap[k].Open   || 0), backgroundColor: 'rgba(239,68,68,0.75)',  borderRadius: 6, borderSkipped: false },
                { label: 'Closed', data: sortedKeys.map(k => monthMap[k].Closed || 0), backgroundColor: 'rgba(16,185,129,0.75)', borderRadius: 6, borderSkipped: false }
            ]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                title:  { display: true, text: 'Monthly Ticket Volume', font: { size: 15, weight: 'bold' } }
            },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
}

// ---- Chart 4: Avg Resolution Time per Month (line) ----
function drawResolutionTimeChart(tickets) {
    const canvas = document.getElementById('resolutionTimeChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart('resolutionTimeChart');

    const monthMap = {};
    tickets.forEach(t => {
        if (!t.assignedAt || !t.closedAt) return;
        const start = parseDate(t.assignedAt);
        const end   = parseDate(t.closedAt);
        if (!start || !end || isNaN(start) || isNaN(end)) return;
        const diffMins = Math.floor((end - start) / 60000);
        if (diffMins < 0) return;
        const key = `${end.getFullYear()}-${String(end.getMonth() + 1).padStart(2, '0')}`;
        if (!monthMap[key]) monthMap[key] = { total: 0, count: 0 };
        monthMap[key].total += diffMins;
        monthMap[key].count++;
    });

    const sortedKeys = Object.keys(monthMap).sort();
    const labels = sortedKeys.map(k => {
        const [y, m] = k.split('-');
        return new Date(+y, +m - 1).toLocaleString('en-IN', { month: 'short', year: '2-digit' });
    });
    const avgHours = sortedKeys.map(k => +(monthMap[k].total / monthMap[k].count / 60).toFixed(2));

    chartRegistry['resolutionTimeChart'] = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Avg Resolution Time (hrs)',
                data: avgHours,
                borderColor: '#7c3aed',
                backgroundColor: 'rgba(124,58,237,0.12)',
                borderWidth: 3,
                pointBackgroundColor: '#7c3aed',
                pointRadius: 6, pointHoverRadius: 9,
                fill: true, tension: 0.4
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                title:  { display: true, text: 'Avg Resolution Time per Month (hours)', font: { size: 15, weight: 'bold' } }
            },
            scales: { y: { beginAtZero: true, title: { display: true, text: 'Hours' } } }
        }
    });
}

// ---- Chart 5: Tickets by Category (horizontal bar) ----
function drawCategoryChart(tickets) {
    const canvas = document.getElementById('categoryChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart('categoryChart');

    const catMap = {};
    tickets.forEach(t => {
        const cat = t.category || 'Unknown';
        catMap[cat] = (catMap[cat] || 0) + 1;
    });

    const sorted = Object.entries(catMap).sort((a, b) => b[1] - a[1]);
    const palette = ['#6366f1','#f59e0b','#10b981','#ef4444','#3b82f6','#ec4899','#14b8a6','#f97316','#8b5cf6','#84cc16'];

    chartRegistry['categoryChart'] = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: sorted.map(([k]) => k),
            datasets: [{
                label: 'Tickets',
                data: sorted.map(([, v]) => v),
                backgroundColor: sorted.map((_, i) => palette[i % palette.length]),
                borderRadius: 8, borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title:  { display: true, text: 'Tickets by Category', font: { size: 15, weight: 'bold' } }
            },
            scales: { x: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
}

// ---- Chart 6: Avg Resolution Time per HR (horizontal bar) ----
function drawHRResolutionAvgChart(tickets) {
    const canvas = document.getElementById('hrResolutionChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart('hrResolutionChart');

    const hrMap = {};
    tickets.forEach(t => {
        if (!t.assignedAt || !t.closedAt || !t.assigned) return;
        const start = parseDate(t.assignedAt);
        const end   = parseDate(t.closedAt);
        if (!start || !end || isNaN(start) || isNaN(end)) return;
        const diffMins = Math.floor((end - start) / 60000);
        if (diffMins < 0) return;
        const hr = t.assigned;
        if (!hrMap[hr]) hrMap[hr] = { total: 0, count: 0 };
        hrMap[hr].total  += diffMins;
        hrMap[hr].count++;
    });

    const entries = Object.entries(hrMap)
        .map(([name, v]) => ({ name, avg: +(v.total / v.count / 60).toFixed(2) }))
        .sort((a, b) => a.avg - b.avg);

    chartRegistry['hrResolutionChart'] = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: entries.map(e => e.name),
            datasets: [{
                label: 'Avg Resolution Time (hrs)',
                data: entries.map(e => e.avg),
                backgroundColor: 'rgba(102,126,234,0.82)',
                borderRadius: 8, borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title:  { display: true, text: 'Avg Resolution Time per HR (hours)', font: { size: 15, weight: 'bold' } }
            },
            scales: { x: { beginAtZero: true, title: { display: true, text: 'Hours' } } }
        }
    });
}


// ==========================
// Confirmation Popup
// ==========================
function showConfirm(title, message, action, ticketId = null) {
    pendingAction = action; 
    pendingTicketId = ticketId;
    document.getElementById('popupTitle').textContent = title;
    document.getElementById('popupText').innerHTML = message;
    document.getElementById('confirmPopup').classList.add('show');
}

function hideConfirm() {
    document.getElementById('confirmPopup').classList.remove('show');
    pendingAction = null; 
    pendingTicketId = null;
}

function handleConfirm(confirmed) {
    if (!confirmed || !pendingAction) { 
        hideConfirm(); 
        return; 
    }
    
    if (pendingAction === 'close') { 
        markTicketClosed(); 
    } else if (pendingAction === 'assign') { 
        saveAssignment(); 
    }
    
    hideConfirm();
}

// ==========================
// Logout Popup
// ==========================
function setupLogoutPopup() {
    const logoutBtn = document.getElementById('btnLogout');
    const popup = document.getElementById('logoutPopup');
    const yesBtn = document.getElementById('logoutYes');
    const noBtn = document.getElementById('logoutNo');

    if (!logoutBtn || !popup || !yesBtn || !noBtn) return;

    logoutBtn.addEventListener('click', () => popup.classList.remove('hidden'));
    noBtn.addEventListener('click', () => popup.classList.add('hidden'));
    yesBtn.addEventListener('click', () => {
        popup.classList.add('hidden');
        logoutAdmin();
    });
}

// ==========================
// Warn user before leaving page (refresh / close tab / back)
// ==========================
let allowExit = false;

function confirmExit() {
    return confirm("Do you really want to exit the application?");
}

history.pushState(null, null, location.href);
window.addEventListener('popstate', function (event) {
    if (!allowExit) {
        const leave = confirmExit();
        if (!leave) {
            history.pushState(null, null, location.href);
        } else {
            allowExit = true;
            history.back();
        }
    }
});

window.addEventListener("beforeunload", function (e) {
    if (!allowExit) {
        e.preventDefault();
        e.returnValue = '';
        return '';
    }
});

// ==========================
// Download Excel (SheetJS)
// ==========================
function downloadExcel() {
    if (!filteredTickets || filteredTickets.length === 0) {
        alert(' No ticket data to export. Please load tickets first.');
        return;
    }

    // Build rows with all columns including Resolution Time
    const rows = filteredTickets.map(t => ({
        'Ticket ID':        t.id || '',
        'Name':             t.name || '',
        'Email':            t.email || '',
        'Phone':            t.phone || '',
        'Emp Code':         t.empCode || '',
        'Category':         t.category || '',
        'Description':      t.issue || '',
        'Status':           t.status || '',
        'Assigned To':      t.assigned || 'Unassigned',
        'Created Time':     fmtDateIsoToIST(t.createdAt),
        'Assigned Time':    fmtDateIsoToIST(t.assignedAt),
        'Closed Time':      fmtDateIsoToIST(t.closedAt),
        'Resolution Time':  calcResolutionTime(t.assignedAt, t.closedAt),
        'Remark':           t.remark || ''
    }));

    const ws = XLSX.utils.json_to_sheet(rows);

    // Column widths
    ws['!cols'] = [
        { wch: 16 }, // Ticket ID
        { wch: 20 }, // Name
        { wch: 28 }, // Email
        { wch: 14 }, // Phone
        { wch: 12 }, // Emp Code
        { wch: 18 }, // Category
        { wch: 40 }, // Description
        { wch: 10 }, // Status
        { wch: 22 }, // Assigned To
        { wch: 22 }, // Created Time
        { wch: 22 }, // Assigned Time
        { wch: 22 }, // Closed Time
        { wch: 16 }, // Resolution Time
        { wch: 30 }, // Remark
    ];

    // Style header row (bold + background) — requires xlsx-style or manual approach
    const headerRange = XLSX.utils.decode_range(ws['!ref']);
    for (let C = headerRange.s.c; C <= headerRange.e.c; C++) {
        const cellAddr = XLSX.utils.encode_cell({ r: 0, c: C });
        if (!ws[cellAddr]) continue;
        ws[cellAddr].s = {
            font:      { bold: true, color: { rgb: 'FFFFFF' } },
            fill:      { fgColor: { rgb: '667EEA' } },
            alignment: { horizontal: 'center', vertical: 'center', wrapText: true }
        };
    }

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'HR Tickets');

    // Build filename with date range if filters applied
    const from = document.getElementById('fromDate')?.value;
    const to   = document.getElementById('toDate')?.value;
    const status = document.getElementById('statusFilter')?.value;
    const today = new Date().toISOString().slice(0, 10);

    let filename = `JHS_HR_Tickets_${today}`;
    if (from) filename += `_from${from}`;
    if (to)   filename += `_to${to}`;
    if (status && status !== 'All status') filename += `_${status}`;
    filename += '.xlsx';

    XLSX.writeFile(wb, filename);
}