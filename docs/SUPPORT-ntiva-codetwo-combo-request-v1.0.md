# Ntiva request — CodeTwo Combo mode, add-in audience, attribute access (v1.0, 2026-10-27)

Draft email from Michael to Ntiva (Global Administrator for aceseptictank.com). Status: drafted, not sent.
Register C3 (vendor operations). Context: ADR 0023 in the vault.

---

**Subject:** CodeTwo: switch to Combo mode, add-in audience, and attribute access

Hi Team,

The CodeTwo cloud signatures are working now, thank you for your help with that. Our next step is to show the signature in the email while people write it, not only after it's sent. CodeTwo does this in **Combo** mode, which uses the Outlook add-in for Outlook users and keeps the cloud signatures for everything else. My account can't make these changes, because they need a Global Administrator.

I'm testing with a small pilot first (my mailbox and one operator), so nothing changes for other users until we add them to the new rules.

**Group 1: Signature mode (highest priority, it blocks the pilot)**

1. Change the signature mode for the aceseptictank.com tenant from Cloud to Combo. In the CodeTwo Admin Panel, it's under **Tenants** > aceseptictank.com > **Signature mode**. The "Change signature mode" button is disabled for my account. The change runs a connector step; please keep the existing cloud connectors and rules in place. Tell us the date and time of the change.

**Group 2: Outlook add-in audience**

2. Open **Integrated apps** in the Microsoft 365 admin center. Select **CodeTwo Signatures Add-in for Outlook**, then **Edit users**. Send us the audience type and the group name. The add-in shows up in my Outlook, but in August Josh Irvine didn't have it, so I'm not sure it reached everyone.
3. If the audience isn't the entire organization, please change it to the entire organization, then tell us the date of the change. (If you'd prefer a group, let us know; it can't be a nested group.)

**Group 3: Access for the signature data**

4. Give mewell@purple-standard.com access to the CodeTwo **Attributes manager**. Right now it shows "You don't have appropriate permissions." I need it to check the job titles and phone numbers CodeTwo pulls from Entra, since missing titles and phones are the most common complaint.
5. Turn on **My user info** for all users, if it's a setting on your side. It shows the same permissions error for me. It lets staff correct their own title and phone, so we don't need a ticket for each person.

**Group 4: Open item from August**

6. Please confirm EWS is enabled for user mailboxes (EWSEnabled). Send us the result, or tell us if it's already done.

Let me know if you have any questions, or if you'd rather handle any of these differently than I've described.

Thanks,
