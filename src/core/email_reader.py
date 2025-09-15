from imapclient import IMAPClient
import pyzmail, re
from typing import List, Dict


def _normalize(text, n=200):
text = re.sub(r"\s+", " ", text).strip()
return (text[:n] + "…") if len(text) > n else text


def fetch_emails(host, port, user, password, folder="INBOX", max_fetch=20) -> List[Dict]:
with IMAPClient(host, port=port, ssl=True) as server:
server.login(user, password)
server.select_folder(folder, readonly=True)
msgs = server.search(["NOT", "DELETED"]) # últimos N
msgs = msgs[-max_fetch:]
resp = server.fetch(msgs, ["ENVELOPE", "RFC822.SIZE", "BODY[]"])
emails = []
for uid in msgs:
body = resp[uid][b"BODY[]"]
mail = pyzmail.PyzMessage.factory(body)
subject = mail.get_subject() or ""
from_ = mail.get_addresses("from")
from_name = from_[0][0] or from_[0][1] if from_ else ""
from_email = from_[0][1] if from_ else ""
if mail.text_part:
txt = mail.text_part.get_payload().decode(mail.text_part.charset or "utf-8", errors="ignore")
else:
txt = ""
emails.append({
"uid": int(uid),
"from_name": from_name,
"from_email": from_email,
"subject": subject,
"snippet": _normalize(txt, 300),
"size": resp[uid][b"RFC822.SIZE"]
})
for e in emails:
score = 0
subj = (e["subject"] or "").lower()
if any(k in subj for k in ["reunião","meeting","urgente","prazo","invoice","fatura","parabéns","aprovação"]):
score += 2
if any(k in subj for k in ["dell","genpower","henry","projeto","apresentação"]):
score += 1
e["importance"] = score
emails.sort(key=lambda x: (x["importance"], x["uid"]), reverse=True)
return emails
