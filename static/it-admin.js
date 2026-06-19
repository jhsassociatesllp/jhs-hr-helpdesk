

const API_URL = '/api/it/tickets';
const API_ADMIN = '/api/it';

const ITENGINEERS = {
    'Irfan IT': 'mohammad.siddiqui@jhsassociates.in',
    'Shahnawaz IT': 'mohammad.siddiqui@jhsassociates.in',
    'Pankaj IT': 'mohammad.siddiqui@jhsassociates.in',
    'Other': ''
};

let hrChart = null;
let statusPieChart = null;
let issueChart = null;
let trendChart = null;
let partnerChart = null;
let tatChart = null;

let initialized = false;
let currentTicket = null;
let pendingAction = null;
let pendingTicketId = null;
let allTicketsCache = []; // cache for Excel export

// Pagination variables
let currentPage = 1;
let itemsPerPage = 10;
let filteredTickets = [];

// Session timeout variables
let sessionCheckInterval = null;
let sessionWarningTimeout = null;

// ---------- SESSION MANAGEMENT ----------
function getAuthHeaders() {
    const token = localStorage.getItem('jwtToken');
    if (!token) return {};
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

function checkSession() {
    const token = localStorage.getItem('jwtToken');
    if (!token) { handleSessionExpired(); return false; }
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const expirationTime = payload.exp * 1000;
        const currentTime = Date.now();
        const timeRemaining = expirationTime - currentTime;
        if (timeRemaining < 5 * 60 * 1000 && timeRemaining > 0) showSessionWarning(Math.floor(timeRemaining / 1000 / 60));
        if (timeRemaining <= 0) { handleSessionExpired(); return false; }
        return true;
    } catch (error) {
        handleSessionExpired();
        return false;
    }
}

function showSessionWarning(minutesRemaining) {
    if (sessionWarningTimeout) return;
    const warningDiv = document.createElement('div');
    warningDiv.id = 'sessionWarning';
    warningDiv.style.cssText = `position:fixed;top:20px;right:20px;background:#f59e0b;color:white;padding:1rem 1.5rem;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:10000;font-weight:500;`;
    warningDiv.innerHTML = ` Your session will expire in ${minutesRemaining} minute(s)`;
    document.body.appendChild(warningDiv);
    sessionWarningTimeout = setTimeout(() => { warningDiv.remove(); sessionWarningTimeout = null; }, 10000);
}

function handleSessionExpired() {
    clearInterval(sessionCheckInterval);
    localStorage.removeItem('adminLoggedIn');
    localStorage.removeItem('adminEmpCode');
    localStorage.removeItem('jwtToken');
    alert(' Your session has expired. Please login again.');
    window.location.href = '/adminlogin';
}

function startSessionMonitoring() {
    sessionCheckInterval = setInterval(checkSession, 30000);
    checkSession();
}

// ---------- API WRAPPER ----------
async function apiRequest(url, options = {}) {
    const headers = getAuthHeaders();
    const response = await fetch(url, { ...options, headers: { ...headers, ...options.headers } });
    if (response.status === 401) { handleSessionExpired(); throw new Error('Session expired'); }
    return response;
}

// ---------- UTILITY ----------
function escapeHtml(text) {
    if (!text) return '';
    return String(text).replace(/[&<>"']/g, m =>
        ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m]);
}

function fmtDateIsoToIST(d) {
    if (!d) return '-';
    try {
        const iso = typeof d === 'string' && !d.endsWith('Z') ? d + 'Z' : d;
        return new Date(iso).toLocaleString('en-IN', {
            timeZone: 'Asia/Kolkata', year: 'numeric', month: 'short',
            day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true
        });
    } catch { return d; }
}

function calculateTAT(assignedAt, closedAt) {
    if (!assignedAt) return '-';
    try {
        const assigned = new Date(assignedAt.endsWith('Z') ? assignedAt : assignedAt + 'Z');
        const closed = closedAt ? new Date(closedAt.endsWith('Z') ? closedAt : closedAt + 'Z') : new Date();
        const diffMs = closed - assigned;
        const totalMinutes = Math.floor(diffMs / (1000 * 60));
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        const days = Math.floor(hours / 24);
        const remainingHours = hours % 24;
        if (days > 0) return `${days}d ${remainingHours}h`;
        if (hours > 0) return `${hours}h ${minutes}m`;
        return `${minutes}m`;
    } catch { return '-'; }
}

function tatToHours(assignedAt, closedAt) {
    if (!assignedAt) return null;
    try {
        const assigned = new Date(assignedAt.endsWith('Z') ? assignedAt : assignedAt + 'Z');
        const closed = closedAt ? new Date(closedAt.endsWith('Z') ? closedAt : closedAt + 'Z') : new Date();
        return parseFloat(((closed - assigned) / (1000 * 60 * 60)).toFixed(2));
    } catch { return null; }
}

// ---------- INIT ----------
document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('adminLoggedIn') || !localStorage.getItem('jwtToken')) {
        window.location.href = '/adminlogin';
        return;
    }
    if (initialized) return;
    initialized = true;

    startSessionMonitoring();

    document.getElementById('btnAnalysis')?.addEventListener('click', () => showSection('analysis'));
    document.getElementById('btnTickets')?.addEventListener('click', () => showSection('tickets'));
    document.getElementById('btnClose')?.addEventListener('click', () => showSection('closed'));
    document.getElementById('btnAssign')?.addEventListener('click', () => showSection('assign'));
    document.getElementById('btnLogout')?.addEventListener('click', showLogoutPopup);

    document.getElementById('btnRefresh')?.addEventListener('click', loadTickets);
    document.getElementById('searchInput')?.addEventListener('input', debounce(loadTickets, 300));
    document.getElementById('fromDate')?.addEventListener('change', loadTickets);
    document.getElementById('toDate')?.addEventListener('change', loadTickets);
    document.getElementById('statusFilter')?.addEventListener('change', loadTickets);

    document.getElementById('btnPrevPage')?.addEventListener('click', () => {
        if (currentPage > 1) { currentPage--; renderTickets(); }
    });
    document.getElementById('btnNextPage')?.addEventListener('click', () => {
        const totalPages = Math.ceil(filteredTickets.length / itemsPerPage);
        if (currentPage < totalPages) { currentPage++; renderTickets(); }
    });

    document.getElementById('btnFetch')?.addEventListener('click', fetchTicketDetails);
    document.getElementById('ticketIdInput')?.addEventListener('keypress', (e) => { if (e.key === 'Enter') fetchTicketDetails(); });
    document.getElementById('btnMarkClosed')?.addEventListener('click', validateAndCloseTicket);
    document.getElementById('btnCancelClose')?.addEventListener('click', resetCloseForm);
    document.getElementById('remarkText')?.addEventListener('input', (e) => updateCharCount(e.target.value.length));

    document.getElementById('btnDownloadExcel')?.addEventListener('click', downloadExcel);

    setupAssignSection();
    document.getElementById('popupNo')?.addEventListener('click', () => handleConfirm(false));
    document.getElementById('popupYes')?.addEventListener('click', () => handleConfirm(true));
    document.getElementById('confirmPopup')?.addEventListener('click', (e) => { if (e.target.id === 'confirmPopup') hideConfirm(); });

    document.getElementById('logoutCancel')?.addEventListener('click', hideLogoutPopup);
    document.getElementById('logoutConfirm')?.addEventListener('click', confirmLogout);
    document.getElementById('logoutPopup')?.addEventListener('click', (e) => { if (e.target.id === 'logoutPopup') hideLogoutPopup(); });

    showSection('tickets');
    loadTickets();
    loadStats();
});

function showSection(id) {
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    const el = document.getElementById(id);
    if (el) el.classList.remove('hidden');
    if (id === 'analysis') loadStats();
    if (id === 'tickets') loadTickets();
}

// ---------- LOGOUT ----------
function showLogoutPopup() { document.getElementById('logoutPopup')?.classList.add('show'); }
function hideLogoutPopup() { document.getElementById('logoutPopup')?.classList.remove('show'); }
function confirmLogout() { hideLogoutPopup(); logoutAdmin(); }
function logoutAdmin() {
    clearInterval(sessionCheckInterval);
    localStorage.removeItem('adminLoggedIn');
    localStorage.removeItem('adminEmpCode');
    localStorage.removeItem('jwtToken');
    window.location.href = '/adminlogin';
}

// ---------- LOAD TICKETS ----------
async function loadTickets() {
    const tbody = document.getElementById('ticketBody');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="17" style="text-align:center;padding:3rem">Loading tickets...</td></tr>';
    try {
        const res = await apiRequest(API_URL);
        if (!res.ok) throw new Error('Failed to fetch');
        let tickets = await res.json();

        allTicketsCache = tickets; // cache for Excel

        const fromDate = document.getElementById('fromDate')?.value;
        const toDate = document.getElementById('toDate')?.value;
        if (fromDate || toDate) {
            const from = fromDate ? new Date(fromDate) : new Date(0);
            const to = toDate ? new Date(toDate) : new Date();
            to.setHours(23, 59, 59, 999);
            tickets = tickets.filter(t => { const c = new Date(t.createdAt); return c >= from && c <= to; });
        }

        const statusFilter = document.getElementById('statusFilter')?.value;
        if (statusFilter && statusFilter !== 'All status')
            tickets = tickets.filter(t => t.status?.toLowerCase() === statusFilter.toLowerCase());

        const q = document.getElementById('searchInput')?.value?.toLowerCase();
        if (q) tickets = tickets.filter(t =>
            t.id?.toLowerCase().includes(q) || t.name?.toLowerCase().includes(q) ||
            t.email?.toLowerCase().includes(q) || t.assetCode?.toLowerCase().includes(q) ||
            t.issueDescription?.toLowerCase().includes(q));

        filteredTickets = tickets;
        currentPage = 1;
        renderTickets();
    } catch (e) {
        console.error(e);
        tbody.innerHTML = '<tr><td colspan="17" style="text-align:center;padding:3rem;color:#ef4444">Error loading tickets</td></tr>';
    }
}

function renderTickets() {
    const tbody = document.getElementById('ticketBody');
    if (!tbody) return;
    if (!filteredTickets.length) {
        tbody.innerHTML = '<tr><td colspan="17" style="text-align:center;padding:3rem;color:#64748b">No tickets found</td></tr>';
        updatePaginationControls(); return;
    }
    const start = (currentPage - 1) * itemsPerPage;
    const paged = filteredTickets.slice(start, start + itemsPerPage);
    tbody.innerHTML = paged.map(t => {
        const statusBadge = t.status?.toLowerCase() === 'open'
            ? '<span class="status-open">Open</span>' : '<span class="status-closed">Closed</span>';
        const issuesText = Array.isArray(t.issues) ? t.issues.join(', ') : t.issues || '-';
        const tat = calculateTAT(t.assignedAt, t.closedAt);
        return `<tr>
            <td><strong>${escapeHtml(t.id)}</strong></td>
            <td>${escapeHtml(t.name)}</td>
            <td>${escapeHtml(t.email)}</td>
            <td>${escapeHtml(t.phone) || '-'}</td>
            <td>${escapeHtml(t.assetCode) || '-'}</td>
            <td>${escapeHtml(issuesText)}</td>
            <td>${escapeHtml((t.issueDescription || '').slice(0, 80))}...</td>
            <td>${escapeHtml(t.reportingPartner) || '-'}</td>
            <td>${statusBadge}</td>
            <td>${fmtDateIsoToIST(t.createdAt)}</td>
            <td>${escapeHtml(t.assigned) || 'Unassigned'}</td>
            <td>${escapeHtml(t.itEmail) || '-'}</td>
            <td>${fmtDateIsoToIST(t.assignedAt)}</td>
            <td>${fmtDateIsoToIST(t.closedAt)}</td>
            <td title="${t.remark ? escapeHtml(t.remark) : ''}">${escapeHtml((t.remark || '').slice(0, 50))}${t.remark && t.remark.length > 50 ? '...' : ''}</td>
            <td><strong>${escapeHtml(tat)}</strong></td>
            <td><button class="small" onclick="deleteTicket('${escapeHtml(t.id)}')">Delete</button></td>
        </tr>`;
    }).join('');
    updatePaginationControls();
}

function updatePaginationControls() {
    const totalPages = Math.ceil(filteredTickets.length / itemsPerPage);
    const pageInfo = document.getElementById('pageInfo');
    const prevBtn = document.getElementById('btnPrevPage');
    const nextBtn = document.getElementById('btnNextPage');
    if (pageInfo) pageInfo.textContent = `Page ${currentPage} of ${totalPages || 1}`;
    if (prevBtn) prevBtn.disabled = currentPage <= 1;
    if (nextBtn) nextBtn.disabled = currentPage >= totalPages;
}

async function deleteTicket(id) {
    showConfirm('Delete Ticket', `Do you really want to DELETE ticket <strong>${escapeHtml(id)}</strong>?`, 'delete', id);
}

// ---------- CLOSE TICKET ----------
async function fetchTicketDetails() {
    const ticketId = document.getElementById('ticketIdInput')?.value.trim().toUpperCase();
    const card = document.getElementById('ticketDetailsCard');
    const msg = document.getElementById('closedMsg');
    if (!ticketId) { showCloseMessage('Enter a valid Ticket ID', 'error'); return; }
    try {
        const res = await apiRequest(`${API_URL}/${ticketId}`);
        if (!res.ok) throw new Error('Ticket not found');
        currentTicket = await res.json();
        displayCloseTicketDetails();
        card.classList.add('active');
        msg.classList.remove('active');
    } catch (error) {
        showCloseMessage('❌ Ticket not found', 'error');
        card.classList.remove('active');
    }
}

function displayCloseTicketDetails() {
    const ticket = currentTicket;
    document.getElementById('ticketIdDisplay').textContent = ticket.id;
    document.getElementById('ticketSubject').textContent = `${ticket.assetCode} • ${ticket.reportingPartner}`;
    const statusBadge = document.getElementById('closingStatusBadge');
    statusBadge.textContent = ticket.status || 'Open';
    statusBadge.className = `close-status-badge ${ticket.status?.toLowerCase() === 'closed' ? 'close-status-closed' : 'close-status-open'}`;
    document.getElementById('ticketName').textContent = ticket.name || '-';
    document.getElementById('ticketEmail').textContent = ticket.email || '-';
    document.getElementById('ticketPhone').textContent = ticket.phone || '-';
    document.getElementById('ticketAsset').textContent = ticket.assetCode || '-';
    const issuesText = Array.isArray(ticket.issues) ? ticket.issues.join(', ') : ticket.issues || '-';
    document.getElementById('ticketIssue').textContent = issuesText;
    document.getElementById('ticketPartner').textContent = ticket.reportingPartner || '-';
    document.getElementById('ticketCreatedAt').textContent = fmtDateIsoToIST(ticket.createdAt);
    document.getElementById('ticketAssigned').textContent = ticket.assigned || 'Unassigned';
    document.getElementById('ticketAssignedAt').textContent = fmtDateIsoToIST(ticket.assignedAt);
    document.getElementById('ticketDescription').textContent = ticket.issueDescription || '-';
    calculateAndDisplayTAT(ticket);
    document.getElementById('remarkText').value = '';
    updateCharCount(0);
}

function calculateAndDisplayTAT(ticket) {
    const tatElement = document.getElementById('ticketTAT');
    const tatInfo = document.getElementById('tatInfo');
    if (!ticket.assignedAt) { tatElement.textContent = 'Not Assigned'; tatInfo.textContent = 'Ticket has not been assigned yet'; return; }
    try {
        const assignedDate = new Date(ticket.assignedAt.endsWith('Z') ? ticket.assignedAt : ticket.assignedAt + 'Z');
        const closedDate = ticket.closedAt ? new Date(ticket.closedAt.endsWith('Z') ? ticket.closedAt : ticket.closedAt + 'Z') : new Date();
        const diffMs = closedDate - assignedDate;
        const totalMinutes = Math.floor(diffMs / (1000 * 60));
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        const days = Math.floor(hours / 24);
        const remainingHours = hours % 24;
        let tatDisplay = days > 0 ? `${days}d ${remainingHours}h ${minutes}m` : hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
        tatElement.textContent = tatDisplay;
        tatInfo.textContent = `From ${fmtDateIsoToIST(ticket.assignedAt)}`;
    } catch (error) {
        tatElement.textContent = 'Error';
        tatInfo.textContent = 'Unable to calculate TAT';
    }
}

function updateCharCount(count) {
    const charCountEl = document.getElementById('charCount');
    charCountEl.textContent = count;
    const parent = charCountEl.parentElement;
    if (count > 500) parent.classList.add('error');
    else if (count > 400) parent.classList.add('warning');
    else parent.classList.remove('error', 'warning');
}

function validateAndCloseTicket() {
    const remark = document.getElementById('remarkText')?.value.trim();
    if (!remark) { showCloseMessage(' Please add a resolution remark before closing', 'error'); return; }
    if (remark.length > 500) { showCloseMessage(' Remark exceeds 500 characters', 'error'); return; }
    if (!currentTicket?.id) { showCloseMessage(' No ticket selected', 'error'); return; }
    showConfirm('Close Ticket', `Close ticket <strong>${escapeHtml(currentTicket.id)}</strong> with remark: "${remark.substring(0, 50)}${remark.length > 50 ? '...' : ''}"?`, 'close');
}

function resetCloseForm() {
    document.getElementById('ticketIdInput').value = '';
    document.getElementById('remarkText').value = '';
    document.getElementById('ticketDetailsCard').classList.remove('active');
    document.getElementById('closedMsg').classList.remove('active');
    updateCharCount(0);
    currentTicket = null;
}

function showCloseMessage(text, type = 'success') {
    const msgEl = document.getElementById('closedMsg');
    msgEl.textContent = text;
    msgEl.className = `close-message active ${type}`;
}

// ---------- CONFIRM POPUP ----------
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
    if (!confirmed || !pendingAction) { hideConfirm(); return; }
    if (pendingAction === 'close') markTicketClosed();
    else if (pendingAction === 'assign') saveAssignment();
    else if (pendingAction === 'delete') confirmDelete();
    hideConfirm();
}

async function markTicketClosed() {
    if (!currentTicket?.id) return;
    const remark = document.getElementById('remarkText')?.value.trim();
    const btn = document.getElementById('btnMarkClosed');
    btn.disabled = true; btn.textContent = ' Closing...';
    try {
        const res = await apiRequest(`${API_URL}/${currentTicket.id}`, { method: 'PUT', body: JSON.stringify({ status: 'Closed', remark }) });
        if (!res.ok) throw new Error('Close failed');
        showCloseMessage(` Ticket ${currentTicket.id} closed successfully! User notified.`, 'success');
        setTimeout(() => { resetCloseForm(); loadTickets(); loadStats(); }, 2000);
    } catch (e) {
        showCloseMessage(` Error: ${e.message}`, 'error');
    } finally {
        btn.disabled = false; btn.textContent = '✓ Mark as Closed & Notify';
    }
}

async function confirmDelete() {
    if (!pendingTicketId) return;
    try {
        const res = await apiRequest(`${API_URL}/${pendingTicketId}`, { method: 'DELETE' });
        if (!res.ok) throw new Error('Delete failed');
        loadTickets(); loadStats();
    } catch (e) { alert('Delete failed: ' + e.message); }
}

// ---------- ASSIGN SECTION ----------
function setupAssignSection() {
    const nameSelect = document.getElementById('assignHrName');
    const emailSelect = document.getElementById('assignHrEmail');
    if (!nameSelect || !emailSelect) return;

    nameSelect.innerHTML = '<option value="">Select IT Engineer Name</option>' +
        Object.keys(ITENGINEERS).map(name => `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join('');

    emailSelect.innerHTML = '<option value="">Select Email</option>' +
        Object.entries(ITENGINEERS).filter(([, email]) => email)
            .map(([name, email]) => `<option value="${escapeHtml(email)}" data-name="${escapeHtml(name)}">${escapeHtml(email)}</option>`).join('');

    nameSelect.addEventListener('change', () => {
        const name = nameSelect.value;
        const email = ITENGINEERS[name];
        emailSelect.value = email || '';
        emailSelect.disabled = !email || name === 'Other' || name === 'Unassigned';
    });

    emailSelect.addEventListener('change', () => {
        const selectedEmail = emailSelect.value;
        const matchingName = Object.keys(ITENGINEERS).find(name => ITENGINEERS[name] === selectedEmail);
        if (matchingName && nameSelect.value !== matchingName) nameSelect.value = matchingName;
    });

    document.getElementById('assignSaveBtn')?.addEventListener('click', () => {
        const ticketId = document.getElementById('assignTicketId')?.value.trim();
        const hrName = document.getElementById('assignHrName')?.value;
        const hrEmail = document.getElementById('assignHrEmail')?.value;
        const msg = document.getElementById('assignMsg');

        if (!ticketId || !hrName) { msg.textContent = 'Ticket ID & IT Engineer are required'; msg.className = 'msg-error'; return; }
        if (hrName !== 'Unassigned' && hrName !== 'Other' && ITENGINEERS[hrName] !== hrEmail) { msg.textContent = 'Email must match selected IT Engineer name'; msg.className = 'msg-error'; return; }

        showConfirm('Assign Ticket', `Assign ticket <strong>${escapeHtml(ticketId)}</strong> to <strong>${escapeHtml(hrName)}</strong>?`, 'assign', ticketId);
    });
}

async function saveAssignment() {
    const ticketId = pendingTicketId;
    const hrName = document.getElementById('assignHrName')?.value;
    const hrEmail = document.getElementById('assignHrEmail')?.value;
    const msg = document.getElementById('assignMsg');
    try {
        const res = await apiRequest(`${API_URL}/${ticketId}`, { method: 'PUT', body: JSON.stringify({ assigned: hrName, status: 'Open', itEmail: hrEmail || null }) });
        if (!res.ok) throw new Error('Assignment failed');
        msg.textContent = 'Assigned & emails sent!'; msg.className = 'msg-success';
        document.getElementById('assignTicketId').value = '';
        document.getElementById('assignHrName').value = '';
        document.getElementById('assignHrEmail').value = '';
        loadTickets(); loadStats();
    } catch (e) { msg.textContent = `Error: ${e.message}`; msg.className = 'msg-error'; }
}

// ---------- STATS & CHARTS ----------
async function loadStats() {
    try {
        const res = await apiRequest(`${API_URL}`);
        if (!res.ok) throw new Error('failed');
        const tickets = await res.json();
        allTicketsCache = tickets;
        buildAllCharts(tickets);
    } catch (e) {
        console.error('Stats load failed:', e);
    }
}

function buildAllCharts(tickets) {
    // --- Summary stats ---
    const total = tickets.length;
    const open = tickets.filter(t => t.status?.toLowerCase() === 'open').length;
    const closed = tickets.filter(t => t.status?.toLowerCase() === 'closed').length;

    document.getElementById('totalTickets').textContent = total;
    document.getElementById('openTickets').textContent = open;
    document.getElementById('closedTickets').textContent = closed;

    // Avg TAT in hours (only closed with assignedAt)
    const tatValues = tickets
        .filter(t => t.assignedAt && t.closedAt)
        .map(t => tatToHours(t.assignedAt, t.closedAt))
        .filter(v => v !== null);
    const avgTat = tatValues.length ? (tatValues.reduce((a, b) => a + b, 0) / tatValues.length).toFixed(1) : '-';
    document.getElementById('avgTatStat').textContent = avgTat;

    // --- Chart 1: Engineer Open vs Closed (bar) ---
    const byIT = {};
    tickets.forEach(t => {
        const eng = t.assigned || 'Unassigned';
        if (!byIT[eng]) byIT[eng] = { Open: 0, Closed: 0 };
        const status = t.status?.toLowerCase() === 'closed' ? 'Closed' : 'Open';
        byIT[eng][status]++;
    });
    drawHRChart(byIT);

    // --- Chart 2: Status Pie ---
    drawStatusPie(open, closed);

    // --- Chart 3: Issues Breakdown ---
    const issueCounts = {};
    tickets.forEach(t => {
        const issues = Array.isArray(t.issues) ? t.issues : [t.issues].filter(Boolean);
        issues.forEach(issue => {
            if (issue) issueCounts[issue] = (issueCounts[issue] || 0) + 1;
        });
    });
    drawIssueChart(issueCounts);

    // --- Chart 4: Trend (last 30 days) ---
    const trendData = {};
    const now = new Date();
    for (let i = 29; i >= 0; i--) {
        const d = new Date(now);
        d.setDate(d.getDate() - i);
        const key = d.toISOString().split('T')[0];
        trendData[key] = 0;
    }
    tickets.forEach(t => {
        if (t.createdAt) {
            const key = new Date(t.createdAt).toISOString().split('T')[0];
            if (trendData[key] !== undefined) trendData[key]++;
        }
    });
    drawTrendChart(trendData);

    // --- Chart 5: Partner Doughnut ---
    const partnerCounts = {};
    tickets.forEach(t => {
        const p = t.reportingPartner || 'Unknown';
        partnerCounts[p] = (partnerCounts[p] || 0) + 1;
    });
    drawPartnerChart(partnerCounts);

    // --- Chart 6: Avg TAT per Engineer ---
    const tatByEng = {};
    tickets.forEach(t => {
        if (!t.assignedAt || !t.closedAt) return;
        const eng = t.assigned || 'Unassigned';
        if (!tatByEng[eng]) tatByEng[eng] = [];
        const hours = tatToHours(t.assignedAt, t.closedAt);
        if (hours !== null) tatByEng[eng].push(hours);
    });
    const tatAvgByEng = {};
    Object.entries(tatByEng).forEach(([eng, vals]) => {
        tatAvgByEng[eng] = parseFloat((vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(1));
    });
    drawTatChart(tatAvgByEng);
}

function destroyChart(ref) {
    if (ref) { try { ref.destroy(); } catch (e) {} }
}

function drawHRChart(byit) {
    const canvas = document.getElementById('hrChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart(hrChart);
    const labels = Object.keys(byit);
    hrChart = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels,
            datasets: [
                { label: 'Open', data: labels.map(l => byit[l].Open || 0), backgroundColor: '#f87171', borderRadius: 8, borderSkipped: false },
                { label: 'Closed', data: labels.map(l => byit[l].Closed || 0), backgroundColor: '#34d399', borderRadius: 8, borderSkipped: false }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } }, scales: { y: { beginAtZero: true } } }
    });
}

function drawStatusPie(open, closed) {
    const canvas = document.getElementById('statusPieChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart(statusPieChart);
    statusPieChart = new Chart(canvas.getContext('2d'), {
        type: 'pie',
        data: {
            labels: ['Open', 'Closed'],
            datasets: [{ data: [open, closed], backgroundColor: ['#fbbf24', '#34d399'], borderWidth: 3, borderColor: '#fff' }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.raw} (${((ctx.raw / (open + closed)) * 100).toFixed(1)}%)` } }
            }
        }
    });
}

function drawIssueChart(issueCounts) {
    const canvas = document.getElementById('issueChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart(issueChart);
    const sorted = Object.entries(issueCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);
    const colors = ['#6366f1','#f59e0b','#10b981','#3b82f6','#ef4444','#8b5cf6','#f97316','#14b8a6','#ec4899','#64748b'];
    issueChart = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: sorted.map(([k]) => k),
            datasets: [{ label: 'Count', data: sorted.map(([, v]) => v), backgroundColor: colors, borderRadius: 8, borderSkipped: false }]
        },
        options: {
            responsive: true, maintainAspectRatio: false, indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: { x: { beginAtZero: true } }
        }
    });
}

function drawTrendChart(trendData) {
    const canvas = document.getElementById('trendChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart(trendChart);
    const labels = Object.keys(trendData).map(d => {
        const dt = new Date(d);
        return `${dt.getDate()}/${dt.getMonth() + 1}`;
    });
    trendChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: 'Tickets Raised',
                data: Object.values(trendData),
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99,102,241,0.12)',
                borderWidth: 2.5,
                pointRadius: 4,
                pointBackgroundColor: '#6366f1',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}

function drawPartnerChart(partnerCounts) {
    const canvas = document.getElementById('partnerChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart(partnerChart);
    const labels = Object.keys(partnerCounts);
    const colors = ['#6366f1','#f59e0b','#10b981','#3b82f6','#ef4444','#8b5cf6','#f97316','#14b8a6','#ec4899','#64748b'];
    partnerChart = new Chart(canvas.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{ data: labels.map(l => partnerCounts[l]), backgroundColor: colors.slice(0, labels.length), borderWidth: 3, borderColor: '#fff' }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { position: 'bottom' } },
            cutout: '60%'
        }
    });
}

function drawTatChart(tatAvgByEng) {
    const canvas = document.getElementById('tatChart');
    if (!canvas || typeof Chart === 'undefined') return;
    destroyChart(tatChart);
    const labels = Object.keys(tatAvgByEng);
    tatChart = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Avg TAT (hours)',
                data: labels.map(l => tatAvgByEng[l]),
                backgroundColor: '#f59e0b',
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, title: { display: true, text: 'Hours' } } }
        }
    });
}

// ---------- EXCEL DOWNLOAD ----------
function downloadExcel() {
    const tickets = allTicketsCache;
    if (!tickets || !tickets.length) { alert('No ticket data to export.'); return; }

    const wb = XLSX.utils.book_new();

    // Sheet 1: All Tickets
    const rows = tickets.map(t => ({
        'Ticket ID': t.id || '',
        'Name': t.name || '',
        'Email': t.email || '',
        'Phone': t.phone || '',
        'IT Asset Code': t.assetCode || '',
        'Issues': Array.isArray(t.issues) ? t.issues.join(', ') : t.issues || '',
        'Description': t.issueDescription || '',
        'Reporting Partner': t.reportingPartner || '',
        'Status': t.status || '',
        'Created At': fmtDateIsoToIST(t.createdAt),
        'Assigned Engineer': t.assigned || 'Unassigned',
        'Engineer Email': t.itEmail || '',
        'Assigned At': fmtDateIsoToIST(t.assignedAt),
        'Closed At': fmtDateIsoToIST(t.closedAt),
        'Remark': t.remark || '',
        'TAT': calculateTAT(t.assignedAt, t.closedAt)
    }));
    const ws1 = XLSX.utils.json_to_sheet(rows);
    ws1['!cols'] = [
        { wch: 18 }, { wch: 20 }, { wch: 28 }, { wch: 15 }, { wch: 18 },
        { wch: 30 }, { wch: 40 }, { wch: 22 }, { wch: 10 }, { wch: 22 },
        { wch: 20 }, { wch: 28 }, { wch: 22 }, { wch: 22 }, { wch: 40 }, { wch: 12 }
    ];
    XLSX.utils.book_append_sheet(wb, ws1, 'All Tickets');

    // Sheet 2: Summary
    const open = tickets.filter(t => t.status?.toLowerCase() === 'open').length;
    const closed = tickets.filter(t => t.status?.toLowerCase() === 'closed').length;
    const tatValues = tickets.filter(t => t.assignedAt && t.closedAt).map(t => tatToHours(t.assignedAt, t.closedAt)).filter(v => v !== null);
    const avgTat = tatValues.length ? (tatValues.reduce((a, b) => a + b, 0) / tatValues.length).toFixed(1) : 'N/A';

    const summaryRows = [
        { 'Metric': 'Total Tickets', 'Value': tickets.length },
        { 'Metric': 'Open Tickets', 'Value': open },
        { 'Metric': 'Closed Tickets', 'Value': closed },
        { 'Metric': 'Avg TAT (hours)', 'Value': avgTat },
        { 'Metric': 'Report Generated', 'Value': new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }) }
    ];
    const ws2 = XLSX.utils.json_to_sheet(summaryRows);
    ws2['!cols'] = [{ wch: 25 }, { wch: 30 }];
    XLSX.utils.book_append_sheet(wb, ws2, 'Summary');

    // Sheet 3: Engineer Stats
    const byIT = {};
    tickets.forEach(t => {
        const eng = t.assigned || 'Unassigned';
        if (!byIT[eng]) byIT[eng] = { Open: 0, Closed: 0, TatHours: [] };
        const status = t.status?.toLowerCase() === 'closed' ? 'Closed' : 'Open';
        byIT[eng][status]++;
        const h = tatToHours(t.assignedAt, t.closedAt);
        if (h !== null) byIT[eng].TatHours.push(h);
    });
    const engRows = Object.entries(byIT).map(([eng, data]) => ({
        'Engineer': eng,
        'Open': data.Open,
        'Closed': data.Closed,
        'Total': data.Open + data.Closed,
        'Avg TAT (hrs)': data.TatHours.length ? (data.TatHours.reduce((a, b) => a + b, 0) / data.TatHours.length).toFixed(1) : 'N/A'
    }));
    const ws3 = XLSX.utils.json_to_sheet(engRows);
    ws3['!cols'] = [{ wch: 22 }, { wch: 10 }, { wch: 10 }, { wch: 10 }, { wch: 18 }];
    XLSX.utils.book_append_sheet(wb, ws3, 'Engineer Stats');

    // Download
    const dateStr = new Date().toISOString().split('T')[0];
    XLSX.writeFile(wb, `JHS_IT_Helpdesk_Report_${dateStr}.xlsx`);
}

// ---------- HELPERS ----------
function debounce(fn, delay) {
    let timeout;
    return (...args) => { clearTimeout(timeout); timeout = setTimeout(() => fn(...args), delay); };
}