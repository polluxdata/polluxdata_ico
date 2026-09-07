# Follow-up Email — structure and rules

Output: **plain text (.txt)**. Short follow-up after sending an offer/proforma or after a meeting.

Generated with `make_email.py` from a JSON with: contact first name, subject, body, CTA, sender.

## Structure

```
Asunto: {curious/direct, references the doc ref}
Hola {nombre}:
{body}     — 2-4 sentences: the numbers that matter, validity date, zero pressure
{cta}      — ONE concrete question with two options (dates/choices)
Si prefieres, te llamo hoy mismo — dime una hora y te marco.
Un saludo,
{sender}
PolluxData · polluxdata.com · email
```

## Tone (informal-ganadora)

- Direct and warm, "tú", short sentences
- Lead with the concrete value (numbers, weeks, outcomes)
- CTA is always a closed question with two options — never "déjame saber"
- One email = one ask. Never stack three asks
- No corporate filler ("quedamos atentos a sus comentarios" is banned)

## Verification

- [ ] References the document ref and validity date
- [ ] CTA has two concrete options
- [ ] Under 120 words
