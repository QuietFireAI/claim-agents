# INTEGRATIONS - Claim Swarm (Insurance) (v0.1, ratified 2026-07-11 - owner sign-off)

The deployable boundary of this identity: every external system it touches,
the contract an adapter must satisfy, and the conformance bar. This file is
the build spec for implementers; no adapter code ships here.

## Adapter contract (applies to every seam below)

Every external system connects through an adapter that presents to the hub as
a registered endpoint. The contract is the same everywhere:

1. **Inbound**: adapter events enter as envelopes on the seam's declared
   intent(s), with provenance `{source, captured_at, verbatim_available}` -
   an event without provenance is rejected at the hub, not cleaned up.
2. **Outbound**: the adapter consumes the seam's outbound intent(s) and MUST
   return the named acceptance artifact. No artifact = not done; the sending
   agent treats it as failed and escalates at lead-time.
3. **Custody**: seams flagged SEALED transport content by reference only -
   the adapter never exposes sealed content to swarm agents.
4. **Idempotency**: adapters de-duplicate on the upstream reference key named
   per seam; a replayed event re-acks, never re-processes.
5. **Conformance**: an adapter is deployable when it passes the checklist at
   the end of this file against a sandbox of the target system. Passing the
   checklist is the definition of done - a demo is not conformance.

No adapter code ships in this repo. This file is the contract an implementer
builds against; credentials, sandboxes, and vendor agreements are
deployment-site property.

## Seams

| Seam | Direction | Serves | Required artifact | Sealed | Idempotency key |
|---|---|---|---|---|---|
| FNOL channels (phone/web/portal) | IN | claim.fnol intake | n/a (inbound) | no | FNOL reference |
| Policy admin system | IN | policy verification facts | n/a (lookup facts + timestamp) | no | policy number + as-of |
| Estimating platform | OUT+IN | estimate order + package intents | estimate package artifact | no | estimate ID |
| Payments/reserves core | OUT | payment.authority execution lane (signed) | payment confirmation artifact | no | transaction ID |
| Inspection/adjuster vendors | OUT+IN | inspection scheduling + reports | report artifact in record | no | assignment ID |
| Document intake (email/upload) | IN | document collection intents | n/a (inventoried with source) | YES | document hash |

## Adapter conformance checklist (per seam)

- [ ] Inbound events carry full provenance; hub accepts; missing provenance rejected
- [ ] Outbound intent produces the named acceptance artifact in the record
- [ ] Duplicate upstream event re-acks without re-processing (idempotency key proven)
- [ ] SEALED seams: content never readable by any swarm agent (reference-only verified)
- [ ] Failure mode: adapter outage surfaces as unknown/exception, never as stale success
- [ ] Every adapter interaction lands in interaction.log via the owning agent

