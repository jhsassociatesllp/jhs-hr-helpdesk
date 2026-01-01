// // const API_URL = 'http://localhost:8000/api/tickets';
// // const API_ADMIN = 'http://localhost:8000/api/admin';

// const API_URL = '/api/tickets';
// const API_ADMIN = '/api/admin';

// // ✅ FIXED: Matches backend EXACTLY
// const HR_MAPPING = {
//     'Unassigned': '', 
//     'Janhavi Gamare': 'janhavi.gamare@jhsassociatesllp.in', 
//     'Darshan Shah': 'darshan.shah@jhsassociates.in', 
//     'Krutika Shivshivkar': 'krutika.shivshivkar@jhsassociates.in', 
//     'Fiza Kudalkar': 'fiza.kudalkar@jhsassociates.in'
// };

// let hrChart = null; 
// let initialized = false; 
// let currentTicket = null;
// let pendingAction = null; 
// let pendingTicketId = null;
// let currentPage = 1;
// const itemsPerPage = 10;
// let filteredTickets = [];

// function escapeHtml(text) {
//     if (!text) return ''; 
//     return String(text).replace(/[&<>"']/g, m => ({ 
//         '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' 
//     })[m]);
// }

// function fmtDateIsoToIST(d) {
//     if (!d) return '-';
//     try {
//         const date = new Date(d + 'Z'); 
//         return date.toLocaleString('en-IN', { 
//             timeZone: 'Asia/Kolkata',
//             year: 'numeric',
//             month: 'short',
//             day: 'numeric',
//             hour: '2-digit',
//             minute: '2-digit',
//             hour12: true
//         });
//     } catch {
//         return d;
//     }
// }

// document.addEventListener('DOMContentLoaded', () => {
//     if (!localStorage.getItem('adminLoggedIn')) { 
//         window.location.href = '/static/adminlogin.html'; 
//         return; 
//     }
//     if (initialized) return; 
//     initialized = true;

//     document.getElementById('btnAnalysis')?.addEventListener('click', () => showSection('analysis'));
//     document.getElementById('btnTickets')?.addEventListener('click', () => showSection('tickets'));
//     document.getElementById('btnClose')?.addEventListener('click', () => showSection('closed'));
//     document.getElementById('btnAssign')?.addEventListener('click', () => showSection('assign'));
//     document.getElementById('btnLogout')?.addEventListener('click', logoutAdmin);

//     document.getElementById('btnRefresh')?.addEventListener('click', loadTickets);
//     document.getElementById('searchInput')?.addEventListener('input', debounce(loadTickets, 300));
//     document.getElementById('fromDate')?.addEventListener('change', loadTickets);
//     document.getElementById('toDate')?.addEventListener('change', loadTickets);
//     document.getElementById('statusFilter')?.addEventListener('change', loadTickets);

//     document.getElementById('btnFetch')?.addEventListener('click', fetchTicketDetails);

//     // ✅ ADD-UP: Remark mandatory before closing
//     document.getElementById('btnMarkClosed')?.addEventListener('click', () => {
//         if (!currentTicket?.id) return;
//         const remark = document.getElementById('closeRemark')?.value.trim();
//         if (!remark) {
//             alert('Remark is mandatory to close the ticket');
//             return;
//         }
//         showConfirm('Close Ticket', `Do you really want to CLOSE ticket ${currentTicket.id}?`, 'close');
//     });

//     setupAssignSection();
//     document.getElementById('popupNo')?.addEventListener('click', () => handleConfirm(false));
//     document.getElementById('popupYes')?.addEventListener('click', () => handleConfirm(true));
//     document.getElementById('confirmPopup')?.addEventListener('click', (e) => {
//         if (e.target.id === 'confirmPopup') hideConfirm();
//     });

//     showSection('tickets'); 
//     loadTickets(); 
//     loadStats();
// });

// function showSection(id) {
//     document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
//     const el = document.getElementById(id); 
//     if (el) el.classList.remove('hidden');
//     if (id === 'analysis') loadStats(); 
//     if (id === 'tickets') loadTickets(); 
// }

// function logoutAdmin() {
//     localStorage.removeItem('adminLoggedIn'); 
//     localStorage.removeItem('adminEmpCode');
//     window.location.href = '/static/adminlogin.html';
// }

// async function loadTickets() {
//     const tbody = document.getElementById('ticketBody'); 

//     function renderPaginatedTable() {
//         const start = (currentPage - 1) * itemsPerPage;
//         const pageItems = filteredTickets.slice(start, start + itemsPerPage);

//         tbody.innerHTML = pageItems
//             .map(t => {
//                 const statusBadge = t.status?.toLowerCase() === "open"
//                     ? '<span class="status-open">Open</span>'
//                     : '<span class="status-closed">Closed</span>';

//                 return `
//                     <tr>
//                         <td><strong>${escapeHtml(t.id)}</strong></td>
//                         <td>${escapeHtml(t.name)}</td>
//                         <td>${escapeHtml(t.email)}</td>
//                         <td>${escapeHtml(t.phone) || '-'}</td>
//                         <td>${escapeHtml(t.empCode) || '-'}</td>
//                         <td>${escapeHtml(t.category)}</td>
//                         <td>${escapeHtml(t.issue?.slice(0,80))}...</td>
//                         <td>${statusBadge}</td>
//                         <td>${escapeHtml(t.assigned || "Unassigned")}</td>
//                         <td>${fmtDateIsoToIST(t.createdAt)}</td>
//                         <td>${fmtDateIsoToIST(t.assignedAt)}</td>
//                         <td>${fmtDateIsoToIST(t.closedAt)}</td>
                        
//                         <!-- ✅ ADD-UP: remark column -->
//                         <td title="${escapeHtml(t.remark || '')}">
//                             ${escapeHtml(t.remark?.slice(0,40) || '-')}
//                         </td>

//                         <td><button class="small delete-btn" onclick="deleteTicket('${escapeHtml(t.id)}')">🗑️</button></td>
//                     </tr>
//                 `;
//             }).join("");

//         renderPaginationButtons();
//     }

//     function renderPaginationButtons() {
//         const pagination = document.getElementById("pagination");
//         const totalPages = Math.ceil(filteredTickets.length / itemsPerPage);

//         let html = `<button ${currentPage === 1 ? "disabled" : ""} onclick="changePage(${currentPage - 1})">Prev</button>`;

//         for (let i = 1; i <= totalPages; i++) {
//             html += `<button class="${currentPage === i ? "active" : ""}" onclick="changePage(${i})">${i}</button>`;
//         }

//         html += `<button ${currentPage === totalPages ? "disabled" : ""} onclick="changePage(${currentPage + 1})">Next</button>`;
//         pagination.innerHTML = html;
//     }

//     function changePage(page) {
//         currentPage = page;
//         renderPaginatedTable();
//     }

//     if (!tbody) return;
//     tbody.innerHTML = '<tr><td colspan="13" style="text-align:center;padding:3rem">🔄 Loading tickets...</td></tr>';

//     try {
//         const res = await fetch(API_URL); 
//         if (!res.ok) throw new Error('Failed to fetch');
//         let tickets = await res.json();

//         const q = document.getElementById('searchInput')?.value.toLowerCase() || '';
//         const statusFilter = document.getElementById('statusFilter')?.value;
//         const fromDate = document.getElementById('fromDate')?.value; 
//         const toDate = document.getElementById('toDate')?.value;

//         const map = new Map(); 
//         tickets.forEach(t => map.set(t.id, t)); 
//         tickets = Array.from(map.values());

//         if (fromDate || toDate) {
//             const from = fromDate ? new Date(fromDate) : new Date(0); 
//             const to = toDate ? new Date(toDate) : new Date();
//             to.setHours(23, 59, 59, 999); 
//             tickets = tickets.filter(t => { 
//                 const created = new Date(t.createdAt); 
//                 return created >= from && created <= to; 
//             });
//         }

//         if (statusFilter && statusFilter !== 'All status') { 
//             tickets = tickets.filter(t => t.status?.toLowerCase() === statusFilter.toLowerCase()); 
//         }
//         if (q) { 
//             tickets = tickets.filter(t => 
//                 t.id.toLowerCase().includes(q) || 
//                 t.name.toLowerCase().includes(q) || 
//                 t.email.toLowerCase().includes(q) || 
//                 t.category.toLowerCase().includes(q) || 
//                 t.issue?.toLowerCase().includes(q)
//             ); 
//         }

//         if (!tickets.length) { 
//             tbody.innerHTML = '<tr><td colspan="13" style="text-align:center;padding:3rem;color:#64748b">📭 No tickets found</td></tr>'; 
//             return; 
//         }

//         filteredTickets = tickets;
//         renderPaginatedTable();

//     } catch (e) {
//         tbody.innerHTML = '<tr><td colspan="13" style="text-align:center;padding:3rem;color:#ef4444">❌ Error loading tickets</td></tr>'; 
//         console.error(e);
//     }
// }

// async function deleteTicket(id) {
//     try {
//         const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' }); 
//         if (!res.ok) throw new Error('Delete failed');
//         loadTickets(); 
//         loadStats();
//     } catch (e) { 
//         alert(`Delete failed: ${e.message}`); 
//     }
// }

// async function fetchTicketDetails() {
//     const ticketId = document.getElementById('ticketIdInput')?.value.trim();
//     const details = document.getElementById('ticketDetails'); 
//     const msg = document.getElementById('closedMsg');
    
//     if (!ticketId) { 
//         msg.textContent = 'Enter ticket ID'; 
//         msg.className = 'msg-error'; 
//         return; 
//     }

//     try {
//         const res = await fetch(`${API_URL}/${ticketId}`); 
//         if (!res.ok) throw new Error('Ticket not found');
//         currentTicket = await res.json();
//         document.getElementById('ticketName').textContent = currentTicket.name;
//         document.getElementById('ticketEmail').textContent = currentTicket.email;
//         document.getElementById('ticketIssue').textContent = currentTicket.issue;
//         document.getElementById('ticketCreatedAt').textContent = fmtDateIsoToIST(currentTicket.createdAt);
//         document.getElementById('ticketAssigned').textContent = currentTicket.assigned || 'Unassigned';
//         document.getElementById('ticketAssignedAt').textContent = fmtDateIsoToIST(currentTicket.assignedAt); 
//         document.getElementById('ticketClosedAt').textContent = fmtDateIsoToIST(currentTicket.closedAt);
//         details.classList.remove('hidden'); 
//         msg.textContent = '';
//     } catch (e) { 
//         msg.textContent = 'Ticket not found'; 
//         msg.className = 'msg-error'; 
//         details.classList.add('hidden'); 
//     }
// }

// // ========== CONFIRMATION FUNCTIONS ==========
// function showConfirm(title, message, action, ticketId = null) {
//     pendingAction = action; 
//     pendingTicketId = ticketId;
//     document.getElementById('popupTitle').textContent = title;
//     document.getElementById('popupText').innerHTML = message;
//     document.getElementById('confirmPopup').classList.add('show');
// }

// function hideConfirm() {
//     document.getElementById('confirmPopup').classList.remove('show');
//     pendingAction = null; 
//     pendingTicketId = null;
// }

// function handleConfirm(confirmed) {
//     if (!confirmed || !pendingAction) { 
//         hideConfirm(); 
//         return; 
//     }
//     if (pendingAction === 'close') { 
//         markTicketClosed(); 
//     }
//     else if (pendingAction === 'assign') { 
//         saveAssignment(); 
//     }
//     hideConfirm();
// }

// // ✅ ADD-UP: markTicketClosed now sends remark
// async function markTicketClosed() {
//     if (!currentTicket?.id) return;
//     const remark = document.getElementById('closeRemark')?.value.trim();
//     try {
//         const res = await fetch(`${API_URL}/${currentTicket.id}`, {
//             method: 'PUT', 
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ status: 'Closed', remark })
//         });
//         if (!res.ok) throw new Error('Close failed');

//         document.getElementById('closedMsg').textContent = `✅ ${currentTicket.id} closed & notified`;
//         document.getElementById('closedMsg').className = 'msg-success';

//         document.getElementById('closeRemark').value = '';
//         await fetchTicketDetails();
//         document.getElementById('ticketIdInput').value = ''; 
//         currentTicket = null;
//         loadTickets(); 
//         loadStats();
//     } catch (e) {
//         document.getElementById('closedMsg').textContent = `Error: ${e.message}`;
//         document.getElementById('closedMsg').className = 'msg-error';
//     }
// }

// // ========== ASSIGN SECTION ==========
// function setupAssignSection() {
//     const nameSelect = document.getElementById('assignHrName'); 
//     const emailSelect = document.getElementById('assignHrEmail');
//     if (!nameSelect || !emailSelect) return;

//     nameSelect.innerHTML = '<option value="">Select HR Name</option>' + 
//         Object.keys(HR_MAPPING).map(name => 
//             `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`
//         ).join('');

//     emailSelect.innerHTML = '<option value="">Select Email</option>';
//     Object.entries(HR_MAPPING).forEach(([name, email]) => {
//         if (email) {  
//             emailSelect.innerHTML += `<option value="${escapeHtml(email)}" data-name="${escapeHtml(name)}">${escapeHtml(email)}</option>`;
//         }
//     });

//     nameSelect.addEventListener('change', () => {
//         const name = nameSelect.value; 
//         const email = HR_MAPPING[name] || '';
//         emailSelect.value = email; 
//         emailSelect.disabled = !email || name === 'Unassigned' || name === 'Other';
//     });

//     emailSelect.addEventListener('change', () => {
//         const selectedEmail = emailSelect.value;
//         const matchingName = Object.keys(HR_MAPPING).find(name => HR_MAPPING[name] === selectedEmail);
//         if (matchingName && !nameSelect.value) {
//             nameSelect.value = matchingName;
//         }
//     });

//     document.getElementById('assignSaveBtn')?.addEventListener('click', () => {
//         const ticketId = document.getElementById('assignTicketId')?.value.trim();
//         const hrName = document.getElementById('assignHrName')?.value;
//         const hrEmail = document.getElementById('assignHrEmail')?.value;
//         if (!ticketId || !hrName) {
//             document.getElementById('assignMsg').textContent = 'Ticket ID & HR Name required';
//             document.getElementById('assignMsg').className = 'msg-error'; 
//             return;
//         }
//         if (hrName !== 'Unassigned' && hrName !== 'Other' && HR_MAPPING[hrName] !== hrEmail) {
//             document.getElementById('assignMsg').textContent = 'Email must match selected HR name';
//             document.getElementById('assignMsg').className = 'msg-error'; 
//             return;
//         }
//         showConfirm('Assign Ticket', 
//             `Assign ticket <strong>${escapeHtml(ticketId)}</strong> to <strong>${escapeHtml(hrName)}</strong> (${escapeHtml(hrEmail || 'No email')})?`, 
//             'assign', ticketId
//         );
//     });
// }

// async function saveAssignment() {
//     const ticketId = pendingTicketId; 
//     const hrName = document.getElementById('assignHrName')?.value;
//     const hrEmail = document.getElementById('assignHrEmail')?.value; 
//     const msg = document.getElementById('assignMsg');
//     try {
//         const res = await fetch(`${API_URL}/${ticketId}`, {
//             method: 'PUT', 
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ assigned: hrName, status: 'Open', hrEmail })
//         });
//         if (!res.ok) throw new Error('Assignment failed');
//         msg.textContent = '✅ Assigned & emails sent!'; 
//         msg.className = 'msg-success';
//         document.getElementById('assignTicketId').value = ''; 
//         document.getElementById('assignHrName').value = '';
//         document.getElementById('assignHrEmail').value = ''; 
//         loadTickets(); 
//         loadStats();
//     } catch (e) { 
//         msg.textContent = `Error: ${e.message}`; 
//         msg.className = 'msg-error'; 
//     }
// }

// async function loadStats() {
//     try {
//         const res = await fetch(`${API_URL}/stats`); 
//         if (res.ok) { 
//             const data = await res.json(); 
//             updateStats(data); 
//             return; 
//         }
//     } catch { }
//     buildStatsFallback();
// }

// function updateStats(data) {
//     document.getElementById('totalTickets').textContent = data.total || 0;
//     document.getElementById('openTickets').textContent = data.bystatus?.Open || 0;
//     document.getElementById('closedTickets').textContent = data.bystatus?.Closed || 0;
//     drawHRChart(data.byhr || {});
// }

// function drawHRChart(byhr) {
//     const canvas = document.getElementById('hrChart'); 
//     if (!canvas || !byhr || typeof Chart === 'undefined') return;
//     const ctx = canvas.getContext('2d'); 
//     const labels = Object.keys(byhr);
//     const openData = labels.map(l => byhr[l].Open || 0); 
//     const closedData = labels.map(l => byhr[l].Closed || 0);
//     if (hrChart) hrChart.destroy();
//     hrChart = new Chart(ctx, {
//         type: 'bar', 
//         data: { 
//             labels, 
//             datasets: [
//                 { label: 'Open', data: openData, backgroundColor: '#e81313ff', borderRadius: 8, borderSkipped: false }, 
//                 { label: 'Closed', data: closedData, backgroundColor: '#17ac78ff', borderRadius: 8, borderSkipped: false }
//             ] 
//         },
//         options: { 
//             responsive: true, 
//             maintainAspectRatio: false, 
//             plugins: { legend: { position: 'top' } }, 
//             scales: { y: { beginAtZero: true } } 
//         }
//     });
// }

// function debounce(fn, delay) {
//     let timeout; 
//     return (...args) => { 
//         clearTimeout(timeout); 
//         timeout = setTimeout(() => fn(...args), delay); 
//     };
// }

























































































// ---------------------working code


// // API Configuration
// // const API_URL = 'http://localhost:8000/api/tickets';
// // const API_ADMIN = 'http://localhost:8000/api/admin';

// const API_URL = '/api/tickets';
// const API_ADMIN = '/api/admin';

// // HR Mapping - matches backend exactly
// const HR_MAPPING = {
//     'Unassigned': '', 
//     'Janhavi Gamare': 'janhavi.gamare@jhsassociatesllp.in', 
//     'Darshan Shah': 'darshan.shah@jhsassociates.in', 
//     'Krutika Shivshivkar': 'krutika.shivshivkar@jhsassociates.in', 
//     'Fiza Kudalkar': 'fiza.kudalkar@jhsassociates.in'
// };

// // Global variables
// let hrChart = null; 
// let initialized = false; 
// let currentTicket = null;
// let pendingAction = null; 
// let pendingTicketId = null;
// let currentPage = 1;
// const itemsPerPage = 10;
// let filteredTickets = [];

// // Utility Functions
// function escapeHtml(text) {
//     if (!text) return ''; 
//     return String(text).replace(/[&<>"']/g, m => ({ 
//         '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' 
//     })[m]);
// }

// function fmtDateIsoToIST(d) {
//     if (!d) return '-';
//     try {
//         const date = new Date(d + 'Z'); 
//         return date.toLocaleString('en-IN', { 
//             timeZone: 'Asia/Kolkata',
//             year: 'numeric',
//             month: 'short',
//             day: 'numeric',
//             hour: '2-digit',
//             minute: '2-digit',
//             hour12: true
//         });
//     } catch {
//         return d;
//     }
// }

// function debounce(fn, delay) {
//     let timeout; 
//     return (...args) => { 
//         clearTimeout(timeout); 
//         timeout = setTimeout(() => fn(...args), delay); 
//     };
// }

// // Initialize
// document.addEventListener('DOMContentLoaded', () => {
//     // Check admin authentication
//     if (!localStorage.getItem('adminLoggedIn')) { 
//         window.location.href = '/static/adminlogin.html'; 
//         return; 
//     }
    
//     if (initialized) return; 
//     initialized = true;

//     // Navigation buttons
//     document.getElementById('btnAnalysis')?.addEventListener('click', () => showSection('analysis'));
//     document.getElementById('btnTickets')?.addEventListener('click', () => showSection('tickets'));
//     document.getElementById('btnClose')?.addEventListener('click', () => showSection('closed'));
//     document.getElementById('btnAssign')?.addEventListener('click', () => showSection('assign'));
//     document.getElementById('btnLogout')?.addEventListener('click', logoutAdmin);

//     // Ticket filters
//     document.getElementById('btnRefresh')?.addEventListener('click', loadTickets);
//     document.getElementById('searchInput')?.addEventListener('input', debounce(loadTickets, 300));
//     document.getElementById('fromDate')?.addEventListener('change', loadTickets);
//     document.getElementById('toDate')?.addEventListener('change', loadTickets);
//     document.getElementById('statusFilter')?.addEventListener('change', loadTickets);

//     // Close section
//     document.getElementById('btnFetch')?.addEventListener('click', fetchTicketDetails);
//     document.getElementById('btnMarkClosed')?.addEventListener('click', () => {
//         if (!currentTicket?.id) return;
//         const remark = document.getElementById('closeRemark')?.value.trim();
//         if (!remark) {
//             alert('⚠️ Remark is mandatory to close the ticket');
//             return;
//         }
//         showConfirm('Close Ticket', `Do you really want to CLOSE ticket <strong>${currentTicket.id}</strong>?`, 'close');
//     });

//     // Assign section
//     setupAssignSection();

//     // Popup
//     document.getElementById('popupNo')?.addEventListener('click', () => handleConfirm(false));
//     document.getElementById('popupYes')?.addEventListener('click', () => handleConfirm(true));
//     document.getElementById('confirmPopup')?.addEventListener('click', (e) => {
//         if (e.target.id === 'confirmPopup') hideConfirm();
//     });

//     // Initial load
//     showSection('tickets'); 
//     loadTickets(); 
//     loadStats();
// });

// // Section Management
// function showSection(id) {
//     document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
//     const el = document.getElementById(id); 
//     if (el) el.classList.remove('hidden');
    
//     if (id === 'analysis') loadStats(); 
//     if (id === 'tickets') loadTickets(); 
// }

// function logoutAdmin() {
//     localStorage.removeItem('adminLoggedIn'); 
//     localStorage.removeItem('adminEmpCode');
//     window.location.href = '/static/adminlogin.html';
// }

// // Tickets Management
// async function loadTickets() {
//     const tbody = document.getElementById('ticketBody'); 
//     if (!tbody) return;

//     tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:3rem">🔄 Loading tickets...</td></tr>';

//     try {
//         const res = await fetch(API_URL); 
//         if (!res.ok) throw new Error('Failed to fetch');
//         let tickets = await res.json();

//         // Get filters
//         const q = document.getElementById('searchInput')?.value.toLowerCase() || '';
//         const statusFilter = document.getElementById('statusFilter')?.value;
//         const fromDate = document.getElementById('fromDate')?.value; 
//         const toDate = document.getElementById('toDate')?.value;

//         // Remove duplicates
//         const map = new Map(); 
//         tickets.forEach(t => map.set(t.id, t)); 
//         tickets = Array.from(map.values());

//         // Apply date filter
//         if (fromDate || toDate) {
//             const from = fromDate ? new Date(fromDate) : new Date(0); 
//             const to = toDate ? new Date(toDate) : new Date();
//             to.setHours(23, 59, 59, 999); 
//             tickets = tickets.filter(t => { 
//                 const created = new Date(t.createdAt); 
//                 return created >= from && created <= to; 
//             });
//         }

//         // Apply status filter
//         if (statusFilter && statusFilter !== 'All status') { 
//             tickets = tickets.filter(t => t.status?.toLowerCase() === statusFilter.toLowerCase()); 
//         }

//         // Apply search filter
//         if (q) { 
//             tickets = tickets.filter(t => 
//                 t.id.toLowerCase().includes(q) || 
//                 t.name.toLowerCase().includes(q) || 
//                 t.email.toLowerCase().includes(q) || 
//                 t.category.toLowerCase().includes(q) || 
//                 t.issue?.toLowerCase().includes(q)
//             ); 
//         }

//         if (!tickets.length) { 
//             tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:3rem;color:#64748b">📭 No tickets found</td></tr>'; 
//             return; 
//         }

//         filteredTickets = tickets;
//         renderPaginatedTable();

//     } catch (e) {
//         tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:3rem;color:#ef4444">❌ Error loading tickets</td></tr>'; 
//         console.error(e);
//     }
// }

// function renderPaginatedTable() {
//     const tbody = document.getElementById('ticketBody');
//     const start = (currentPage - 1) * itemsPerPage;
//     const pageItems = filteredTickets.slice(start, start + itemsPerPage);

//     tbody.innerHTML = pageItems
//         .map(t => {
//             const statusBadge = t.status?.toLowerCase() === "open"
//                 ? '<span class="status-open">Open</span>'
//                 : '<span class="status-closed">Closed</span>';

//             return `
//                 <tr>
//                     <td><strong>${escapeHtml(t.id)}</strong></td>
//                     <td>${escapeHtml(t.name)}</td>
//                     <td>${escapeHtml(t.email)}</td>
//                     <td>${escapeHtml(t.phone) || '-'}</td>
//                     <td>${escapeHtml(t.empCode) || '-'}</td>
//                     <td>${escapeHtml(t.category)}</td>
//                     <td title="${escapeHtml(t.issue)}">${escapeHtml(t.issue?.slice(0,60))}...</td>
//                     <td>${statusBadge}</td>
//                     <td>${escapeHtml(t.assigned || "Unassigned")}</td>
//                     <td>${fmtDateIsoToIST(t.createdAt)}</td>
//                     <td>${fmtDateIsoToIST(t.assignedAt)}</td>
//                     <td>${fmtDateIsoToIST(t.closedAt)}</td>
//                     <td title="${escapeHtml(t.remark || '')}">${escapeHtml(t.remark?.slice(0,30) || '-')}</td>
//                     <td><button class="delete-btn" onclick="deleteTicket('${escapeHtml(t.id)}')">DELETE</button></td>
//                 </tr>
//             `;
//         }).join("");

//     renderPaginationButtons();
// }

// function renderPaginationButtons() {
//     const pagination = document.getElementById("pagination");
//     const totalPages = Math.ceil(filteredTickets.length / itemsPerPage);

//     let html = `<button ${currentPage === 1 ? "disabled" : ""} onclick="changePage(${currentPage - 1})">← Prev</button>`;

//     // Show page numbers
//     for (let i = 1; i <= totalPages; i++) {
//         html += `<button class="${currentPage === i ? "active" : ""}" onclick="changePage(${i})">${i}</button>`;
//     }

//     html += `<button ${currentPage === totalPages ? "disabled" : ""} onclick="changePage(${currentPage + 1})">Next →</button>`;
//     pagination.innerHTML = html;
// }

// function changePage(page) {
//     const totalPages = Math.ceil(filteredTickets.length / itemsPerPage);
//     if (page < 1 || page > totalPages) return;
    
//     currentPage = page;
//     renderPaginatedTable();
// }

// async function deleteTicket(id) {
//     if (!confirm(`⚠️ Are you sure you want to delete ticket ${id}?`)) return;
    
//     try {
//         const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' }); 
//         if (!res.ok) throw new Error('Delete failed');
//         loadTickets(); 
//         loadStats();
//     } catch (e) { 
//         alert(`❌ Delete failed: ${e.message}`); 
//     }
// }

// // Close Ticket Functions
// async function fetchTicketDetails() {
//     const ticketId = document.getElementById('ticketIdInput')?.value.trim();
//     const details = document.getElementById('ticketDetails'); 
//     const msg = document.getElementById('closedMsg');
    
//     if (!ticketId) { 
//         msg.textContent = '⚠️ Please enter a ticket ID'; 
//         msg.className = 'msg-error'; 
//         return; 
//     }

//     msg.textContent = '';

//     try {
//         const res = await fetch(`${API_URL}/${ticketId}`); 
//         if (!res.ok) throw new Error('Ticket not found');
        
//         currentTicket = await res.json();
        
//         document.getElementById('ticketName').textContent = currentTicket.name;
//         document.getElementById('ticketEmail').textContent = currentTicket.email;
//         document.getElementById('ticketIssue').textContent = currentTicket.issue;
//         document.getElementById('ticketCreatedAt').textContent = fmtDateIsoToIST(currentTicket.createdAt);
//         document.getElementById('ticketAssigned').textContent = currentTicket.assigned || 'Unassigned';
//         document.getElementById('ticketAssignedAt').textContent = fmtDateIsoToIST(currentTicket.assignedAt); 
//         document.getElementById('ticketClosedAt').textContent = fmtDateIsoToIST(currentTicket.closedAt);
        
//         // Clear previous remark
//         document.getElementById('closeRemark').value = '';
        
//         details.classList.remove('hidden'); 
        
//     } catch (e) { 
//         msg.textContent = '❌ Ticket not found'; 
//         msg.className = 'msg-error'; 
//         details.classList.add('hidden'); 
//     }
// }

// async function markTicketClosed() {
//     if (!currentTicket?.id) return;
    
//     const remark = document.getElementById('closeRemark')?.value.trim();
    
//     try {
//         const res = await fetch(`${API_URL}/${currentTicket.id}`, {
//             method: 'PUT', 
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ status: 'Closed', remark })
//         });
        
//         if (!res.ok) throw new Error('Close failed');

//         const msg = document.getElementById('closedMsg');
//         msg.textContent = `✅ Ticket ${currentTicket.id} closed successfully & user notified!`;
//         msg.className = 'msg-success';

//         // Reset form
//         document.getElementById('closeRemark').value = '';
//         document.getElementById('ticketIdInput').value = ''; 
//         document.getElementById('ticketDetails').classList.add('hidden');
//         currentTicket = null;
        
//         // Reload data
//         loadTickets(); 
//         loadStats();
        
//     } catch (e) {
//         const msg = document.getElementById('closedMsg');
//         msg.textContent = `❌ Error: ${e.message}`;
//         msg.className = 'msg-error';
//     }
// }

// // Assign Section
// function setupAssignSection() {
//     const nameSelect = document.getElementById('assignHrName'); 
//     const emailSelect = document.getElementById('assignHrEmail');
//     if (!nameSelect || !emailSelect) return;

//     // Populate name dropdown
//     nameSelect.innerHTML = '<option value="">Select HR Name</option>' + 
//         Object.keys(HR_MAPPING).map(name => 
//             `<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`
//         ).join('');

//     // Populate email dropdown
//     emailSelect.innerHTML = '<option value="">Select Email</option>';
//     Object.entries(HR_MAPPING).forEach(([name, email]) => {
//         if (email) {  
//             emailSelect.innerHTML += `<option value="${escapeHtml(email)}" data-name="${escapeHtml(name)}">${escapeHtml(email)}</option>`;
//         }
//     });

//     // Sync name and email
//     nameSelect.addEventListener('change', () => {
//         const name = nameSelect.value; 
//         const email = HR_MAPPING[name] || '';
//         emailSelect.value = email; 
//         emailSelect.disabled = !email || name === 'Unassigned';
//     });

//     emailSelect.addEventListener('change', () => {
//         const selectedEmail = emailSelect.value;
//         const matchingName = Object.keys(HR_MAPPING).find(name => HR_MAPPING[name] === selectedEmail);
//         if (matchingName && !nameSelect.value) {
//             nameSelect.value = matchingName;
//         }
//     });

//     // Assign button
//     document.getElementById('assignSaveBtn')?.addEventListener('click', () => {
//         const ticketId = document.getElementById('assignTicketId')?.value.trim();
//         const hrName = document.getElementById('assignHrName')?.value;
//         const hrEmail = document.getElementById('assignHrEmail')?.value;
//         const msg = document.getElementById('assignMsg');
        
//         if (!ticketId || !hrName) {
//             msg.textContent = '⚠️ Ticket ID & HR Name are required';
//             msg.className = 'msg-error'; 
//             return;
//         }
        
//         if (hrName !== 'Unassigned' && HR_MAPPING[hrName] !== hrEmail) {
//             msg.textContent = '⚠️ Email must match selected HR name';
//             msg.className = 'msg-error'; 
//             return;
//         }
        
//         showConfirm(
//             'Assign Ticket', 
//             `Assign ticket <strong>${escapeHtml(ticketId)}</strong> to <strong>${escapeHtml(hrName)}</strong>?`, 
//             'assign', 
//             ticketId
//         );
//     });
// }

// async function saveAssignment() {
//     const ticketId = pendingTicketId; 
//     const hrName = document.getElementById('assignHrName')?.value;
//     const hrEmail = document.getElementById('assignHrEmail')?.value; 
//     const msg = document.getElementById('assignMsg');
    
//     try {
//         const res = await fetch(`${API_URL}/${ticketId}`, {
//             method: 'PUT', 
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ assigned: hrName, status: 'Open', hrEmail })
//         });
        
//         if (!res.ok) throw new Error('Assignment failed');
        
//         msg.textContent = '✅ Ticket assigned successfully & emails sent!'; 
//         msg.className = 'msg-success';
        
//         // Reset form
//         document.getElementById('assignTicketId').value = ''; 
//         document.getElementById('assignHrName').value = '';
//         document.getElementById('assignHrEmail').value = ''; 
        
//         // Reload data
//         loadTickets(); 
//         loadStats();
        
//     } catch (e) { 
//         msg.textContent = `❌ Error: ${e.message}`; 
//         msg.className = 'msg-error'; 
//     }
// }

// // Stats & Analytics
// async function loadStats() {
//     try {
//         const res = await fetch(`${API_URL}/stats`); 
//         if (res.ok) { 
//             const data = await res.json(); 
//             updateStats(data); 
//             return; 
//         }
//     } catch { }
    
//     // Fallback: calculate stats from tickets
//     buildStatsFallback();
// }

// async function buildStatsFallback() {
//     try {
//         const res = await fetch(API_URL);
//         if (!res.ok) return;
        
//         const tickets = await res.json();
//         const stats = {
//             total: tickets.length,
//             bystatus: {},
//             byhr: {}
//         };
        
//         tickets.forEach(t => {
//             const status = t.status || 'Unknown';
//             const hr = t.assigned || 'Unassigned';
            
//             stats.bystatus[status] = (stats.bystatus[status] || 0) + 1;
            
//             if (!stats.byhr[hr]) stats.byhr[hr] = { Open: 0, Closed: 0 };
//             stats.byhr[hr][status] = (stats.byhr[hr][status] || 0) + 1;
//         });
        
//         updateStats(stats);
//     } catch (e) {
//         console.error('Failed to build stats:', e);
//     }
// }

// function updateStats(data) {
//     document.getElementById('totalTickets').textContent = data.total || 0;
//     document.getElementById('openTickets').textContent = data.bystatus?.Open || 0;
//     document.getElementById('closedTickets').textContent = data.bystatus?.Closed || 0;
//     drawHRChart(data.byhr || {});
// }

// function drawHRChart(byhr) {
//     const canvas = document.getElementById('hrChart'); 
//     if (!canvas || !byhr || typeof Chart === 'undefined') return;
    
//     const ctx = canvas.getContext('2d'); 
//     const labels = Object.keys(byhr);
//     const openData = labels.map(l => byhr[l].Open || 0); 
//     const closedData = labels.map(l => byhr[l].Closed || 0);
    
//     if (hrChart) hrChart.destroy();
    
//     hrChart = new Chart(ctx, {
//         type: 'bar', 
//         data: { 
//             labels, 
//             datasets: [
//                 { 
//                     label: 'Open', 
//                     data: openData, 
//                     backgroundColor: '#ef4444', 
//                     borderRadius: 8, 
//                     borderSkipped: false 
//                 }, 
//                 { 
//                     label: 'Closed', 
//                     data: closedData, 
//                     backgroundColor: '#10b981', 
//                     borderRadius: 8, 
//                     borderSkipped: false 
//                 }
//             ] 
//         },
//         options: { 
//             responsive: true, 
//             maintainAspectRatio: false, 
//             plugins: { 
//                 legend: { position: 'top' },
//                 title: {
//                     display: true,
//                     text: 'Tickets by HR Representative'
//                 }
//             }, 
//             scales: { 
//                 y: { beginAtZero: true } 
//             } 
//         }
//     });
// }

// // Confirmation Popup
// function showConfirm(title, message, action, ticketId = null) {
//     pendingAction = action; 
//     pendingTicketId = ticketId;
//     document.getElementById('popupTitle').textContent = title;
//     document.getElementById('popupText').innerHTML = message;
//     document.getElementById('confirmPopup').classList.add('show');
// }

// function hideConfirm() {
//     document.getElementById('confirmPopup').classList.remove('show');
//     pendingAction = null; 
//     pendingTicketId = null;
// }

// function handleConfirm(confirmed) {
//     if (!confirmed || !pendingAction) { 
//         hideConfirm(); 
//         return; 
//     }
    
//     if (pendingAction === 'close') { 
//         markTicketClosed(); 
//     } else if (pendingAction === 'assign') { 
//         saveAssignment(); 
//     }
    
//     hideConfirm();
// }



































































































// API Configuration
const API_URL = '/api/tickets';
const API_ADMIN = '/api/admin';

// HR Mapping
const HR_MAPPING = {
    'Unassigned': '', 
    'Janhavi Gamare': 'janhavi.gamare@jhsassociatesllp.in', 
    'Darshan Shah': 'darshan.shah@jhsassociates.in', 
    'Krutika Shivshivkar': 'krutika.shivshivkar@jhsassociates.in', 
    'Fiza Kudalkar': 'fiza.kudalkar@jhsassociates.in'
};

// Global variables
let hrChart = null; 
let initialized = false; 
let currentTicket = null;
let pendingAction = null; 
let pendingTicketId = null;
let currentPage = 1;
const itemsPerPage = 10;
let filteredTickets = [];

// Utility Functions
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

function debounce(fn, delay) {
    let timeout; 
    return (...args) => { 
        clearTimeout(timeout); 
        timeout = setTimeout(() => fn(...args), delay); 
    };
}

// NEW: Reset filters and reload
function resetFiltersAndReload() {
    document.getElementById('searchInput').value = '';
    document.getElementById('fromDate').value = '';
    document.getElementById('toDate').value = '';
    document.getElementById('statusFilter').value = 'All status';
    currentPage = 1;
    loadTickets();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('adminLoggedIn')) { 
        window.location.href = '/static/adminlogin.html'; 
        return; 
    }
    
    if (initialized) return; 
    initialized = true;

    // Navigation buttons
    document.getElementById('btnAnalysis')?.addEventListener('click', () => showSection('analysis'));
    document.getElementById('btnTickets')?.addEventListener('click', () => showSection('tickets'));
    document.getElementById('btnClose')?.addEventListener('click', () => showSection('closed'));
    document.getElementById('btnAssign')?.addEventListener('click', () => showSection('assign'));
    document.getElementById('btnLogout')?.addEventListener('click', logoutAdmin);

    // Ticket filters - FIXED: Use resetFiltersAndReload for refresh button
    document.getElementById('btnRefresh')?.addEventListener('click', resetFiltersAndReload);
    document.getElementById('searchInput')?.addEventListener('input', debounce(loadTickets, 300));
    document.getElementById('fromDate')?.addEventListener('change', loadTickets);
    document.getElementById('toDate')?.addEventListener('change', loadTickets);
    document.getElementById('statusFilter')?.addEventListener('change', loadTickets);

    // Close section
    document.getElementById('btnFetch')?.addEventListener('click', fetchTicketDetails);
    document.getElementById('btnMarkClosed')?.addEventListener('click', () => {
        if (!currentTicket?.id) return;
        const remark = document.getElementById('closeRemark')?.value.trim();
        if (!remark) {
            alert('⚠️ Remark is mandatory to close the ticket');
            return;
        }
        showConfirm('Close Ticket', `Do you really want to CLOSE ticket <strong>${currentTicket.id}</strong>?`, 'close');
    });

    // Assign section
    setupAssignSection();

    // Popup
    document.getElementById('popupNo')?.addEventListener('click', () => handleConfirm(false));
    document.getElementById('popupYes')?.addEventListener('click', () => handleConfirm(true));
    document.getElementById('confirmPopup')?.addEventListener('click', (e) => {
        if (e.target.id === 'confirmPopup') hideConfirm();
    });

    // Initial load
    showSection('tickets'); 
    loadTickets(); 
    loadStats();
});

// Section Management
function showSection(id) {
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    const el = document.getElementById(id); 
    if (el) el.classList.remove('hidden');
    
    if (id === 'analysis') loadStats(); 
    if (id === 'tickets') loadTickets(); 
}

function logoutAdmin() {
    localStorage.removeItem('adminLoggedIn'); 
    localStorage.removeItem('adminEmpCode');
    window.location.href = '/static/adminlogin.html';
}

// Tickets Management
async function loadTickets() {
    const tbody = document.getElementById('ticketBody'); 
    if (!tbody) return;

    // FIXED: Changed colspan to 14
    tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:3rem">🔄 Loading tickets...</td></tr>';

    try {
        const res = await fetch(API_URL); 
        if (!res.ok) throw new Error('Failed to fetch');
        let tickets = await res.json();

        // Get filters
        const q = document.getElementById('searchInput')?.value.toLowerCase() || '';
        const statusFilter = document.getElementById('statusFilter')?.value;
        const fromDate = document.getElementById('fromDate')?.value; 
        const toDate = document.getElementById('toDate')?.value;

        // Remove duplicates
        const map = new Map(); 
        tickets.forEach(t => map.set(t.id, t)); 
        tickets = Array.from(map.values());

        // Apply date filter
        if (fromDate || toDate) {
            const from = fromDate ? new Date(fromDate) : new Date(0); 
            const to = toDate ? new Date(toDate) : new Date();
            to.setHours(23, 59, 59, 999); 
            tickets = tickets.filter(t => { 
                const created = new Date(t.createdAt); 
                return created >= from && created <= to; 
            });
        }

        // Apply status filter
        if (statusFilter && statusFilter !== 'All status') { 
            tickets = tickets.filter(t => t.status?.toLowerCase() === statusFilter.toLowerCase()); 
        }

        // Apply search filter
        if (q) { 
            tickets = tickets.filter(t => 
                t.id.toLowerCase().includes(q) || 
                t.name.toLowerCase().includes(q) || 
                t.email.toLowerCase().includes(q) || 
                t.category.toLowerCase().includes(q) || 
                t.issue?.toLowerCase().includes(q)
            ); 
        }

        // FIXED: Changed colspan to 14
        if (!tickets.length) { 
            tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:3rem;color:#64748b">📭 No tickets found</td></tr>'; 
            return; 
        }

        filteredTickets = tickets;
        renderPaginatedTable();

    } catch (e) {
        // FIXED: Changed colspan to 14
        tbody.innerHTML = '<tr><td colspan="14" style="text-align:center;padding:3rem;color:#ef4444">❌ Error loading tickets</td></tr>'; 
        console.error(e);
    }
}

function renderPaginatedTable() {
    const tbody = document.getElementById('ticketBody');
    const start = (currentPage - 1) * itemsPerPage;
    const pageItems = filteredTickets.slice(start, start + itemsPerPage);

    tbody.innerHTML = pageItems
        .map(t => {
            const statusBadge = t.status?.toLowerCase() === "open"
                ? '<span class="status-open">Open</span>'
                : '<span class="status-closed">Closed</span>';

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
    if (!confirm(`⚠️ Are you sure you want to delete ticket ${id}?`)) return;
    
    try {
        const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' }); 
        if (!res.ok) throw new Error('Delete failed');
        loadTickets(); 
        loadStats();
    } catch (e) { 
        alert(`❌ Delete failed: ${e.message}`); 
    }
}

// Close Ticket Functions
async function fetchTicketDetails() {
    const ticketId = document.getElementById('ticketIdInput')?.value.trim();
    const details = document.getElementById('ticketDetails'); 
    const msg = document.getElementById('closedMsg');
    
    if (!ticketId) { 
        msg.textContent = '⚠️ Please enter a ticket ID'; 
        msg.className = 'msg-error'; 
        return; 
    }

    msg.textContent = '';

    try {
        const res = await fetch(`${API_URL}/${ticketId}`); 
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
        msg.textContent = '❌ Ticket not found'; 
        msg.className = 'msg-error'; 
        details.classList.add('hidden'); 
    }
}

async function markTicketClosed() {
    if (!currentTicket?.id) return;
    
    const remark = document.getElementById('closeRemark')?.value.trim();
    
    try {
        const res = await fetch(`${API_URL}/${currentTicket.id}`, {
            method: 'PUT', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: 'Closed', remark })
        });
        
        if (!res.ok) throw new Error('Close failed');

        const msg = document.getElementById('closedMsg');
        msg.textContent = `✅ Ticket ${currentTicket.id} closed successfully & user notified!`;
        msg.className = 'msg-success';

        document.getElementById('closeRemark').value = '';
        document.getElementById('ticketIdInput').value = ''; 
        document.getElementById('ticketDetails').classList.add('hidden');
        currentTicket = null;
        
        loadTickets(); 
        loadStats();
        
    } catch (e) {
        const msg = document.getElementById('closedMsg');
        msg.textContent = `❌ Error: ${e.message}`;
        msg.className = 'msg-error';
    }
}

// Assign Section
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
        if (email) {  
            emailSelect.innerHTML += `<option value="${escapeHtml(email)}" data-name="${escapeHtml(name)}">${escapeHtml(email)}</option>`;
        }
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
            msg.textContent = '⚠️ Ticket ID & HR Name are required';
            msg.className = 'msg-error'; 
            return;
        }
        
        if (hrName !== 'Unassigned' && HR_MAPPING[hrName] !== hrEmail) {
            msg.textContent = '⚠️ Email must match selected HR name';
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
        const res = await fetch(`${API_URL}/${ticketId}`, {
            method: 'PUT', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ assigned: hrName, status: 'Open', hrEmail })
        });
        
        if (!res.ok) throw new Error('Assignment failed');
        
        msg.textContent = '✅ Ticket assigned successfully & emails sent!'; 
        msg.className = 'msg-success';
        
        document.getElementById('assignTicketId').value = ''; 
        document.getElementById('assignHrName').value = '';
        document.getElementById('assignHrEmail').value = ''; 
        
        loadTickets(); 
        loadStats();
        
    } catch (e) { 
        msg.textContent = `❌ Error: ${e.message}`; 
        msg.className = 'msg-error'; 
    }
}

// Stats & Analytics
async function loadStats() {
    try {
        const res = await fetch(`${API_URL}/stats`); 
        if (res.ok) { 
            const data = await res.json(); 
            updateStats(data); 
            return; 
        }
    } catch { }
    
    buildStatsFallback();
}

async function buildStatsFallback() {
    try {
        const res = await fetch(API_URL);
        if (!res.ok) return;
        
        const tickets = await res.json();
        const stats = {
            total: tickets.length,
            bystatus: {},
            byhr: {}
        };
        
        tickets.forEach(t => {
            const status = t.status || 'Unknown';
            const hr = t.assigned || 'Unassigned';
            
            stats.bystatus[status] = (stats.bystatus[status] || 0) + 1;
            
            if (!stats.byhr[hr]) stats.byhr[hr] = { Open: 0, Closed: 0 };
            stats.byhr[hr][status] = (stats.byhr[hr][status] || 0) + 1;
        });
        
        updateStats(stats);
    } catch (e) {
        console.error('Failed to build stats:', e);
    }
}

function updateStats(data) {
    document.getElementById('totalTickets').textContent = data.total || 0;
    document.getElementById('openTickets').textContent = data.bystatus?.Open || 0;
    document.getElementById('closedTickets').textContent = data.bystatus?.Closed || 0;
    drawHRChart(data.byhr || {});
}

function drawHRChart(byhr) {
    const canvas = document.getElementById('hrChart'); 
    if (!canvas || !byhr || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d'); 
    const labels = Object.keys(byhr);
    const openData = labels.map(l => byhr[l].Open || 0); 
    const closedData = labels.map(l => byhr[l].Closed || 0);
    
    if (hrChart) hrChart.destroy();
    
    hrChart = new Chart(ctx, {
        type: 'bar', 
        data: { 
            labels, 
            datasets: [
                { 
                    label: 'Open', 
                    data: openData, 
                    backgroundColor: '#ef4444', 
                    borderRadius: 8, 
                    borderSkipped: false 
                }, 
                { 
                    label: 'Closed', 
                    data: closedData, 
                    backgroundColor: '#10b981', 
                    borderRadius: 8, 
                    borderSkipped: false 
                }
            ] 
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { 
                legend: { position: 'top' },
                title: {
                    display: true,
                    text: 'Tickets by HR Representative'
                }
            }, 
            scales: { 
                y: { beginAtZero: true } 
            } 
        }
    });
}

// Confirmation Popup
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















