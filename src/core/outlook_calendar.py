import win32com.client as win32
from datetime import datetime, timedelta


def get_upcoming_events(days_ahead=7, max_events=10):
outlook = win32.Dispatch("Outlook.Application").GetNamespace("MAPI")
calendar = outlook.GetDefaultFolder(9) # 9 = olFolderCalendar
start = datetime.now()
end = start + timedelta(days=days_ahead)
items = calendar.Items
items.IncludeRecurrences = True
items.Sort("[Start]")
restriction = f"[Start] >= '{start.strftime('%m/%d/%Y %H:%M %p')}' AND [Start] <= '{end.strftime('%m/%d/%Y %H:%M %p')}'"
restricted = items.Restrict(restriction)
events = []
for item in restricted:
try:
events.append({
"subject": item.Subject,
"start": item.Start.Format("%Y-%m-%d %H:%M"),
"end": item.End.Format("%Y-%m-%d %H:%M"),
"location": item.Location or ""
})
except Exception:
continue
if len(events) >= max_events:
break
return events


def format_events_brief(events):
if not events:
return "Sem compromissos nos próximos dias."
out = []
for e in events:
out.append(f"{e['start']} — {e['subject']} ({e['location']})")
return "\n".join(out)
