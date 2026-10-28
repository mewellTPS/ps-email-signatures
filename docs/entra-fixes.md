# Entra fixes owed (hardcoded signatures to revert)

Operators whose signature hardcodes person fields because Entra is missing or wrong.
When Ntiva fixes the Entra profile, switch the person back to the brand `default.html`
(dynamic fields) and check the live signature.

| Person | Brand | Field(s) hardcoded | Correct value | Signature file | Status |
|---|---|---|---|---|---|
| Victor Rodriguez | Brisa (BRS) | Title, Office phone (plus name and email, for exactness) | Co-Owner / Operator; (813) 461-5972 | `brisa/_mockup/victor/signature-*.html` | Entra fix pending (Ntiva) |
| Sean Myatt | WTR DR (WTR) | Title (plus name, phone and email, for exactness) | Owner/Founder (Michael confirmed); 813-429-8737 | `wtr-dr/_mockup/sean/signature-*.html` | Entra fix pending (Ntiva) |
| John Rodrigues | Tyrian Roofing (TYR) | Title, Office phone (plus name and email, for exactness) | Co-Owner/Founder; (813) 471-5201 | `tyrian/_mockup/john/signature-*.html` | Entra fix pending (Ntiva) |
| Danny Boyette | Boyette Pump & Well (BPW) | Title, Office phone, Reddick address (plus name and email, for exactness) | Owner/Founder; (813) 923-0008; 21516 Carson Dr + 15215 N Hwy 329, Reddick, FL 32686 | `boyette/_mockup/danny/signature-*.html` | Entra fix pending (Ntiva); Reddick stays hardcoded even after the fix |
| Kenny Morrow | Purple Current (PC) | First name (Entra shows "K."), Title (plus phone and email, for exactness) | Kenny Morrow; Owner/Founder; (813) 355-0865 | `purple-current/_mockup/kenny/signature-*.html` | Entra fix pending (Ntiva) |
