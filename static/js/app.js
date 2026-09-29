// Meeting Prep Agent Frontend Application
let currentBrief = null;
let savedMeetings = [];

// Initialize on DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadHistoryList();
    setupDropdowns();
    setupKeyboardShortcuts();
    checkBannerState();
});

// --- Theme Management ---
function initTheme() {
    const savedTheme = localStorage.getItem('meeting_prep_theme') || 'light';
    const isDark = savedTheme === 'dark';
    document.documentElement.classList.toggle('dark', isDark);
    updateThemeIcon(isDark);

    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) {
        themeBtn.addEventListener('click', toggleTheme);
    }
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('meeting_prep_theme', isDark ? 'dark' : 'light');
    updateThemeIcon(isDark);
}

function updateThemeIcon(isDark) {
    const icon = document.getElementById('themeIcon');
    if (icon) {
        icon.className = isDark ? 'fa-solid fa-sun text-amber-400' : 'fa-solid fa-moon text-slate-600';
    }
}

// --- Setup Dropdowns & Modals ---
function setupDropdowns() {
    const sampleBtn = document.getElementById('sampleDropdownBtn');
    const sampleMenu = document.getElementById('sampleDropdownMenu');

    if (sampleBtn && sampleMenu) {
        sampleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            sampleMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', () => {
            sampleMenu.classList.add('hidden');
        });
    }

    // History Drawer
    const historyBtn = document.getElementById('historyDrawerBtn');
    if (historyBtn) {
        historyBtn.addEventListener('click', openHistoryDrawer);
    }

    const drawerBackdrop = document.getElementById('historyDrawerBackdrop');
    if (drawerBackdrop) {
        drawerBackdrop.addEventListener('click', closeHistoryDrawer);
    }

    // Settings Modal
    const settingsBtn = document.getElementById('settingsModalBtn');
    if (settingsBtn) {
        settingsBtn.addEventListener('click', openSettingsModal);
    }
}

function setupKeyboardShortcuts() {
    document.getElementById('meetingForm').addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('prepareMeetingBtn').click();
        }
    });
}

function checkBannerState() {
    if (localStorage.getItem('meeting_prep_dismiss_banner') === 'true') {
        const banner = document.getElementById('welcomeBanner');
        if (banner) banner.style.display = 'none';
    }
}

function dismissBanner() {
    localStorage.setItem('meeting_prep_dismiss_banner', 'true');
    const banner = document.getElementById('welcomeBanner');
    if (banner) {
        banner.style.opacity = '0';
        setTimeout(() => banner.style.display = 'none', 200);
    }
}

// --- Sample Presets ---
async function loadSamplePreset(sampleId) {
    const sampleMenu = document.getElementById('sampleDropdownMenu');
    if (sampleMenu) sampleMenu.classList.add('hidden');

    try {
        const resp = await fetch(`/api/samples/${sampleId}`);
        const data = await resp.json();

        if (data.success && data.sample) {
            const s = data.sample;
            document.getElementById('meetingTitle').value = s.title || '';
            document.getElementById('personCompany').value = s.person_company || '';
            document.getElementById('meetingDateTime').value = s.date_time || '';
            document.getElementById('meetingPurpose').value = s.purpose || '';
            document.getElementById('previousNotes').value = s.previous_notes || '';
            document.getElementById('additionalInfo').value = s.additional_info || '';

            hideFormError();
            showToast(`Loaded sample scenario: "${s.title}"`);

            // Highlight form fields briefly
            highlightFormInputs();
        }
    } catch (err) {
        console.error('Failed to load sample preset:', err);
        showToast('Failed to load sample', true);
    }
}

function highlightFormInputs() {
    const inputs = document.querySelectorAll('#meetingForm input, #meetingForm textarea');
    inputs.forEach(el => {
        el.classList.add('ring-2', 'ring-indigo-400');
        setTimeout(() => el.classList.remove('ring-2', 'ring-indigo-400'), 600);
    });
}

function resetForm() {
    document.getElementById('meetingForm').reset();
    hideFormError();
    showToast('Form cleared');
}

function showFormError(msg) {
    const errBox = document.getElementById('formError');
    const errMsg = document.getElementById('formErrorMessage');
    if (errBox && errMsg) {
        errMsg.textContent = msg;
        errBox.classList.remove('hidden');
    }
}

function hideFormError() {
    const errBox = document.getElementById('formError');
    if (errBox) errBox.classList.add('hidden');
}

// --- Main Prepare Meeting Action ---
async function handlePrepareMeeting(event) {
    event.preventDefault();
    hideFormError();

    const title = document.getElementById('meetingTitle').value.trim();
    const personCompany = document.getElementById('personCompany').value.trim();
    const dateTime = document.getElementById('meetingDateTime').value.trim();
    const purpose = document.getElementById('meetingPurpose').value.trim();
    const previousNotes = document.getElementById('previousNotes').value.trim();
    const additionalInfo = document.getElementById('additionalInfo').value.trim();
    const apiKey = localStorage.getItem('meeting_prep_gemini_key') || '';

    if (!title || !personCompany) {
        showFormError('Meeting Title and Person/Company Name are required.');
        return;
    }

    // Set UI to loading state
    setLoadingState(true);

    try {
        const response = await fetch('/api/prepare-meeting', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title,
                person_company: personCompany,
                date_time: dateTime,
                purpose,
                previous_notes: previousNotes,
                additional_info: additionalInfo,
                api_key: apiKey,
                save_history: true
            })
        });

        const result = await response.json();

        if (result.success && result.brief) {
            currentBrief = result.brief;
            renderBrief(result.brief);
            loadHistoryList();
            showToast('Meeting Preparation Brief generated!');
        } else {
            showFormError(result.error || 'Failed to generate meeting brief.');
            setLoadingState(false);
        }
    } catch (error) {
        console.error('Error preparing meeting:', error);
        showFormError('A network error occurred while preparing your meeting brief.');
        setLoadingState(false);
    }
}

// --- Loading Progress Simulator ---
let loadingInterval = null;
function setLoadingState(isLoading) {
    const emptyState = document.getElementById('emptyBriefState');
    const loadingState = document.getElementById('loadingBriefState');
    const activeState = document.getElementById('activeBriefContainer');
    const prepareBtn = document.getElementById('prepareMeetingBtn');
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon');
    const statusText = document.getElementById('loadingStatusText');
    const progressBar = document.getElementById('loadingProgressBar');

    if (isLoading) {
        emptyState.classList.add('hidden');
        activeState.classList.add('hidden');
        loadingState.classList.remove('hidden');

        prepareBtn.disabled = true;
        prepareBtn.classList.add('opacity-75', 'cursor-not-allowed');
        btnText.textContent = 'Generating Brief...';
        btnIcon.className = 'fa-solid fa-spinner animate-spin text-amber-300';

        // Step simulation for encouraging user feedback
        const steps = [
            { text: "Analyzing meeting purpose & company context...", progress: "25%" },
            { text: "Synthesizing prioritized agenda discussion points...", progress: "55%" },
            { text: "Formulating high-impact questions & objection mitigations...", progress: "80%" },
            { text: "Finalizing executive briefing dossier...", progress: "95%" }
        ];
        let stepIdx = 0;
        progressBar.style.width = steps[0].progress;
        statusText.textContent = steps[0].text;

        loadingInterval = setInterval(() => {
            stepIdx++;
            if (stepIdx < steps.length) {
                statusText.textContent = steps[stepIdx].text;
                progressBar.style.width = steps[stepIdx].progress;
            }
        }, 350);

    } else {
        clearInterval(loadingInterval);
        loadingState.classList.add('hidden');
        prepareBtn.disabled = false;
        prepareBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        btnText.textContent = 'Prepare Meeting';
        btnIcon.className = 'fa-solid fa-bolt-lightning text-amber-300';
    }
}

// --- Render Generated Brief ---
function renderBrief(brief) {
    setLoadingState(false);

    const activeContainer = document.getElementById('activeBriefContainer');
    activeContainer.classList.remove('hidden');
    activeContainer.classList.add('animate-fade-in');

    const meta = brief.metadata || {};
    
    // Header
    document.getElementById('briefTitleDisplay').textContent = meta.title || 'Meeting Preparation Brief';
    document.getElementById('briefTargetName').textContent = meta.person_company || 'Stakeholder';
    document.getElementById('briefTargetTime').textContent = meta.date_time || 'Scheduled';
    document.getElementById('briefTypeBadge').textContent = (meta.meeting_type || 'General') + ' Brief';
    document.getElementById('briefEngineBadge').textContent = meta.generated_by || 'Meeting Prep Agent';

    // 1. Meeting Objective
    const obj = brief.meeting_objective || {};
    document.getElementById('briefPrimaryObjective').textContent = obj.primary || 'Align with stakeholder on key priorities.';
    
    const criteriaList = document.getElementById('briefSuccessCriteria');
    criteriaList.innerHTML = '';
    const criteria = obj.success_criteria || [];
    criteria.forEach(item => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2';
        li.innerHTML = `<i class="fa-solid fa-check text-emerald-500 mt-0.5 text-xs"></i><span>${escapeHtml(item)}</span>`;
        criteriaList.appendChild(li);
    });

    // 2. Person / Company Summary
    document.getElementById('briefCompanySummary').textContent = brief.person_company_summary || 'No background summary provided.';

    // 3. Key Discussion Points
    const discussionContainer = document.getElementById('briefDiscussionPoints');
    discussionContainer.innerHTML = '';
    const points = brief.key_discussion_points || [];
    points.forEach((pt, idx) => {
        const card = document.createElement('div');
        card.className = 'p-3 rounded-lg bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 text-xs';
        card.innerHTML = `
            <div class="font-semibold text-slate-800 dark:text-slate-100 flex items-center justify-between gap-2 mb-1">
                <span><span class="text-indigo-600 dark:text-indigo-400 font-bold mr-1.5">${idx + 1}.</span>${escapeHtml(pt.topic || 'Discussion Item')}</span>
            </div>
            <p class="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">${escapeHtml(pt.details || '')}</p>
        `;
        discussionContainer.appendChild(card);
    });

    // 4. Important Questions to Ask
    const questionsList = document.getElementById('briefQuestionsList');
    questionsList.innerHTML = '';
    const questions = brief.important_questions || [];
    questions.forEach((q, idx) => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2.5 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300';
        li.innerHTML = `
            <span class="w-5 h-5 rounded-full bg-indigo-100 dark:bg-indigo-950/80 text-indigo-600 dark:text-indigo-400 font-bold text-[10px] flex items-center justify-center shrink-0">Q${idx + 1}</span>
            <span class="leading-relaxed">${escapeHtml(q)}</span>
        `;
        questionsList.appendChild(li);
    });

    // 5. Suggested Talking Points
    const talkingList = document.getElementById('briefTalkingPoints');
    talkingList.innerHTML = '';
    const talking = brief.suggested_talking_points || [];
    talking.forEach(tp => {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2 p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300';
        li.innerHTML = `
            <i class="fa-solid fa-quote-left text-indigo-400 mt-1 shrink-0 text-[10px]"></i>
            <span class="leading-relaxed">${escapeHtml(tp)}</span>
        `;
        talkingList.appendChild(li);
    });

    // 6. Possible Concerns or Objections
    const objectionsContainer = document.getElementById('briefObjectionsList');
    objectionsContainer.innerHTML = '';
    const objections = brief.possible_concerns_objections || [];
    objections.forEach(objItem => {
        const box = document.createElement('div');
        box.className = 'p-3 rounded-lg bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 text-xs space-y-1.5';
        box.innerHTML = `
            <div class="flex items-center gap-1.5 text-rose-600 dark:text-rose-400 font-semibold">
                <i class="fa-solid fa-triangle-exclamation text-xs"></i>
                <span>Potential Concern: ${escapeHtml(objItem.concern || '')}</span>
            </div>
            <div class="flex items-start gap-1.5 text-slate-600 dark:text-slate-400 pl-4 border-l-2 border-indigo-400">
                <span class="font-semibold text-indigo-600 dark:text-indigo-400 shrink-0">Mitigation:</span>
                <span>${escapeHtml(objItem.mitigation || '')}</span>
            </div>
        `;
        objectionsContainer.appendChild(box);
    });

    // 7. Recommended Next Steps
    const nextStepsList = document.getElementById('briefNextStepsList');
    nextStepsList.innerHTML = '';
    const steps = brief.recommended_next_steps || [];
    steps.forEach((step, idx) => {
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between p-2.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 text-xs';
        item.innerHTML = `
            <div class="flex items-center gap-2">
                <span class="w-5 h-5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 text-[10px] font-bold flex items-center justify-center shrink-0">${idx + 1}</span>
                <span class="text-slate-800 dark:text-slate-200 font-medium">${escapeHtml(step.action || '')}</span>
            </div>
            <div class="flex items-center gap-2 shrink-0">
                <span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 font-semibold">${escapeHtml(step.owner || 'You')}</span>
                <span class="text-[10px] text-indigo-600 dark:text-indigo-400 font-medium">${escapeHtml(step.timing || '')}</span>
            </div>
        `;
        nextStepsList.appendChild(item);
    });

    // Bonus Checklist
    const checklistList = document.getElementById('briefChecklist');
    checklistList.innerHTML = '';
    const checklist = brief.pre_meeting_checklist || [];
    checklist.forEach(item => {
        const li = document.createElement('li');
        li.className = 'flex items-center gap-2';
        li.innerHTML = `
            <input type="checkbox" class="w-3.5 h-3.5 rounded text-indigo-600 focus:ring-indigo-500 border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800">
            <span>${escapeHtml(item)}</span>
        `;
        checklistList.appendChild(li);
    });

    // Email Template update
    const emailDraftTextarea = document.getElementById('emailDraftTextarea');
    if (emailDraftTextarea) {
        emailDraftTextarea.value = brief.follow_up_email_template || '';
    }

    // Scroll slightly if on mobile
    if (window.innerWidth < 1024) {
        activeContainer.scrollIntoView({ behavior: 'smooth' });
    }
}

// --- Markdown Generation & Downloads ---
function getMarkdownBriefText() {
    if (!currentBrief) return '';

    const b = currentBrief;
    const meta = b.metadata || {};
    let md = `# Meeting Preparation Brief: ${meta.title || ''}\n\n`;
    md += `**Stakeholder:** ${meta.person_company || ''}  \n`;
    md += `**Date/Time:** ${meta.date_time || ''}  \n`;
    md += `**Category:** ${meta.meeting_type || 'General'}  \n\n`;

    md += `## 1. Meeting Objective\n`;
    md += `${b.meeting_objective?.primary || ''}\n\n`;
    md += `**Success Criteria:**\n`;
    (b.meeting_objective?.success_criteria || []).forEach(c => {
        md += `- [ ] ${c}\n`;
    });
    md += `\n`;

    md += `## 2. Person / Company Summary\n`;
    md += `${b.person_company_summary || ''}\n\n`;

    md += `## 3. Key Discussion Points\n`;
    (b.key_discussion_points || []).forEach((pt, i) => {
        md += `${i + 1}. **${pt.topic}:** ${pt.details}\n`;
    });
    md += `\n`;

    md += `## 4. Important Questions to Ask\n`;
    (b.important_questions || []).forEach((q, i) => {
        md += `- **Q${i + 1}:** ${q}\n`;
    });
    md += `\n`;

    md += `## 5. Suggested Talking Points\n`;
    (b.suggested_talking_points || []).forEach(tp => {
        md += `> ${tp}\n\n`;
    });

    md += `## 6. Possible Concerns or Objections\n`;
    (b.possible_concerns_objections || []).forEach(item => {
        md += `- **Concern:** ${item.concern}\n  *Mitigation:* ${item.mitigation}\n`;
    });
    md += `\n`;

    md += `## 7. Recommended Next Steps\n`;
    (b.recommended_next_steps || []).forEach((step, i) => {
        md += `${i + 1}. ${step.action} *(Owner: ${step.owner}, Timing: ${step.timing})*\n`;
    });

    return md;
}

function copyBriefMarkdown() {
    if (!currentBrief) return;
    const md = getMarkdownBriefText();

    navigator.clipboard.writeText(md).then(() => {
        const copyIcon = document.getElementById('copyIcon');
        const copyText = document.getElementById('copyText');
        copyIcon.className = 'fa-solid fa-check text-emerald-500';
        copyText.textContent = 'Copied!';
        setTimeout(() => {
            copyIcon.className = 'fa-regular fa-copy';
            copyText.textContent = 'Copy';
        }, 2000);
        showToast('Brief copied to clipboard as Markdown');
    }).catch(err => {
        console.error('Failed to copy markdown:', err);
        showToast('Failed to copy to clipboard', true);
    });
}

function downloadMarkdownFile() {
    if (!currentBrief) return;
    const md = getMarkdownBriefText();
    const title = (currentBrief.metadata?.title || 'Meeting-Brief').replace(/[^a-zA-Z0-9_-]/g, '_');
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`Downloaded ${title}.md`);
}

function downloadCalendarEvent() {
    if (!currentBrief) return;
    const meta = currentBrief.metadata || {};
    const title = meta.title || 'Upcoming Meeting';
    const attendee = meta.person_company || 'Stakeholder';
    const obj = currentBrief.meeting_objective?.primary || '';
    
    // Build agenda overview
    const agendaLines = (currentBrief.key_discussion_points || [])
        .map((p, i) => `${i + 1}. ${p.topic}`)
        .join('\\n');

    const description = `Meeting with: ${attendee}\\n\\nObjective: ${obj}\\n\\nAgenda:\\n${agendaLines}\\n\\nGenerated by Meeting Prep Agent`;
    
    // ICS date stamp
    const now = new Date();
    const dtstamp = now.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    // Default to tomorrow 10am for calendar placeholder if no exact parse
    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    tomorrow.setHours(10, 0, 0, 0);
    const dtstart = tomorrow.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
    const dtend = new Date(tomorrow.getTime() + 45 * 60 * 1000).toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

    const icsContent = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Meeting Prep Agent//EN',
        'CALSCALE:GREGORIAN',
        'BEGIN:VEVENT',
        `UID:mpa-${Date.now()}@meetingprepagent.local`,
        `DTSTAMP:${dtstamp}`,
        `DTSTART:${dtstart}`,
        `DTEND:${dtend}`,
        `SUMMARY:${title} - ${attendee}`,
        `DESCRIPTION:${description}`,
        'STATUS:CONFIRMED',
        'END:VEVENT',
        'END:VCALENDAR'
    ].join('\r\n');

    const cleanFilename = (title || 'meeting').replace(/[^a-zA-Z0-9_-]/g, '_');
    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${cleanFilename}.ics`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`Downloaded calendar invite (${cleanFilename}.ics)`);
}

function printBrief() {
    window.print();
}

// --- Email Modal ---
function openEmailModal() {
    document.getElementById('emailModal').classList.remove('hidden');
}

function closeEmailModal() {
    document.getElementById('emailModal').classList.add('hidden');
}

function copyEmailDraft() {
    const text = document.getElementById('emailDraftTextarea').value;
    navigator.clipboard.writeText(text).then(() => {
        const btnText = document.getElementById('copyEmailBtnText');
        const icon = document.getElementById('copyEmailIcon');
        btnText.textContent = 'Copied!';
        icon.className = 'fa-solid fa-check text-emerald-300';
        setTimeout(() => {
            btnText.textContent = 'Copy Email';
            icon.className = 'fa-regular fa-copy';
        }, 2000);
        showToast('Email template copied to clipboard');
    });
}

// --- History Drawer & Persistence ---
async function loadHistoryList() {
    try {
        const resp = await fetch('/api/meetings');
        const data = await resp.json();
        if (data.success) {
            savedMeetings = data.meetings || [];
            updateHistoryUI(savedMeetings);
        }
    } catch (e) {
        console.error('Failed to load history:', e);
    }
}

function updateHistoryUI(meetings) {
    const badge = document.getElementById('historyBadge');
    if (badge) badge.textContent = meetings.length;

    const list = document.getElementById('historyListContainer');
    if (!list) return;

    if (meetings.length === 0) {
        list.innerHTML = `
            <div class="text-center py-12 text-slate-400">
                <i class="fa-regular fa-folder-open text-2xl mb-2"></i>
                <p class="text-xs">No saved briefs yet.</p>
            </div>
        `;
        return;
    }

    list.innerHTML = '';
    meetings.forEach(m => {
        const item = document.createElement('div');
        item.className = 'p-3 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900/90 hover:border-indigo-400 dark:hover:border-indigo-600 transition group cursor-pointer';
        item.onclick = () => loadPastMeeting(m.id);
        
        item.innerHTML = `
            <div class="flex items-start justify-between gap-2">
                <div class="flex-1 min-w-0">
                    <h4 class="font-semibold text-xs text-slate-900 dark:text-white truncate">${escapeHtml(m.title)}</h4>
                    <p class="text-[11px] text-indigo-600 dark:text-indigo-400 truncate mt-0.5">${escapeHtml(m.person_company)}</p>
                    <div class="flex items-center gap-2 text-[10px] text-slate-400 mt-1">
                        <span><i class="fa-regular fa-clock text-[9px]"></i> ${escapeHtml(m.date_time || 'No date')}</span>
                    </div>
                </div>
                <button onclick="deleteMeetingItem(${m.id}, event)" class="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-rose-500 rounded transition" title="Delete meeting">
                    <i class="fa-regular fa-trash-can text-xs"></i>
                </button>
            </div>
        `;
        list.appendChild(item);
    });
}

function filterHistoryList() {
    const q = (document.getElementById('historySearchInput').value || '').toLowerCase();
    const filtered = savedMeetings.filter(m => 
        (m.title || '').toLowerCase().includes(q) ||
        (m.person_company || '').toLowerCase().includes(q) ||
        (m.purpose || '').toLowerCase().includes(q)
    );
    updateHistoryUI(filtered);
}

async function loadPastMeeting(meetingId) {
    try {
        const resp = await fetch(`/api/meetings/${meetingId}`);
        const data = await resp.json();
        if (data.success && data.meeting) {
            const m = data.meeting;
            // populate form fields
            document.getElementById('meetingTitle').value = m.title || '';
            document.getElementById('personCompany').value = m.person_company || '';
            document.getElementById('meetingDateTime').value = m.date_time || '';
            document.getElementById('meetingPurpose').value = m.purpose || '';
            document.getElementById('previousNotes').value = m.previous_notes || '';
            document.getElementById('additionalInfo').value = m.additional_info || '';

            // render brief
            currentBrief = m.brief;
            renderBrief(m.brief);
            closeHistoryDrawer();
            showToast(`Loaded brief: "${m.title}"`);
        }
    } catch (err) {
        console.error('Failed to load past meeting:', err);
        showToast('Error loading past meeting', true);
    }
}

async function deleteMeetingItem(meetingId, event) {
    event.stopPropagation();
    if (!confirm('Are you sure you want to delete this meeting brief from history?')) return;

    try {
        const resp = await fetch(`/api/meetings/${meetingId}`, { method: 'DELETE' });
        const data = await resp.json();
        if (data.success) {
            showToast('Meeting brief deleted');
            loadHistoryList();
        }
    } catch (err) {
        console.error('Failed to delete meeting:', err);
        showToast('Failed to delete meeting', true);
    }
}

function openHistoryDrawer() {
    document.getElementById('historyDrawer').classList.remove('translate-x-full');
    document.getElementById('historyDrawerBackdrop').classList.remove('hidden');
    loadHistoryList();
}

function closeHistoryDrawer() {
    document.getElementById('historyDrawer').classList.add('translate-x-full');
    document.getElementById('historyDrawerBackdrop').classList.add('hidden');
}

// --- Settings Modal ---
function openSettingsModal() {
    const key = localStorage.getItem('meeting_prep_gemini_key') || '';
    document.getElementById('geminiApiKey').value = key;
    document.getElementById('settingsModal').classList.remove('hidden');
}

function closeSettingsModal() {
    document.getElementById('settingsModal').classList.add('hidden');
}

function saveSettings() {
    const key = document.getElementById('geminiApiKey').value.trim();
    if (key) {
        localStorage.setItem('meeting_prep_gemini_key', key);
    } else {
        localStorage.removeItem('meeting_prep_gemini_key');
    }
    closeSettingsModal();
    showToast('Preferences saved');
}

// --- Phone / Mobile Access Modal ---
let networkPhoneUrl = 'http://10.174.30.42:8080';

async function fetchNetworkInfo() {
    try {
        const resp = await fetch('/api/network-info');
        const data = await resp.json();
        if (data.success && data.network_url) {
            networkPhoneUrl = data.network_url;
        }
    } catch (e) {
        console.error('Failed to get network info:', e);
    }
}

async function openPhoneModal() {
    await fetchNetworkInfo();
    const input = document.getElementById('phoneNetworkUrlInput');
    const qrImg = document.getElementById('phoneQrImage');
    
    if (input) input.value = networkPhoneUrl;
    if (qrImg) {
        qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=${encodeURIComponent(networkPhoneUrl)}`;
    }
    document.getElementById('phoneModal').classList.remove('hidden');
}

function closePhoneModal() {
    document.getElementById('phoneModal').classList.add('hidden');
}

function copyPhoneUrl() {
    const input = document.getElementById('phoneNetworkUrlInput');
    if (!input) return;
    navigator.clipboard.writeText(input.value).then(() => {
        const icon = document.getElementById('copyPhoneIcon');
        const text = document.getElementById('copyPhoneText');
        icon.className = 'fa-solid fa-check text-emerald-300';
        text.textContent = 'Copied!';
        setTimeout(() => {
            icon.className = 'fa-regular fa-copy';
            text.textContent = 'Copy';
        }, 2000);
        showToast('Phone URL copied to clipboard');
    });
}

// --- Toast System ---
function showToast(message, isError = false) {
    const toast = document.getElementById('toastNotification');
    const toastMsg = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');

    toastMsg.textContent = message;
    if (isError) {
        toastIcon.className = 'fa-solid fa-circle-exclamation text-rose-400';
    } else {
        toastIcon.className = 'fa-solid fa-check text-emerald-400';
    }

    toast.classList.remove('translate-y-20', 'opacity-0');
    setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
    }, 2800);
}

// --- Helper Functions ---
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
