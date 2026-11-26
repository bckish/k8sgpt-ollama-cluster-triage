"""Read-only Kubernetes Event triage baseline; never executes remediation."""
import argparse
import json
from collections import Counter
from pathlib import Path

RULES = {
    "FailedScheduling": ("capacity", "Review pod requests, node capacity and scheduling constraints."),
    "FailedMount": ("storage", "Review volume bindings and storage controller status."),
    "Unhealthy": ("health", "Review readiness and liveness probe configuration and application diagnostics."),
    "BackOff": ("availability", "Review container termination reason and application logs."),
    "Failed": ("availability", "Review the affected workload status and recent deployment changes."),
}


def analyze(document):
    if not isinstance(document, dict) or not isinstance(document.get("items"), list):
        raise ValueError("expected a Kubernetes EventList JSON object")
    findings = []
    for event in document["items"]:
        if not isinstance(event, dict) or event.get("type") != "Warning":
            continue
        reason = event.get("reason", "Unknown")
        if not isinstance(reason, str):
            reason = "Unknown"
        category, recommendation = RULES.get(reason, ("unclassified", "Review workload events and escalate to an operator."))
        # Do not reproduce raw event messages, object names, hostnames or other possibly sensitive data.
        findings.append({"reason": reason if reason in RULES else "Unknown", "category": category, "recommendation": recommendation})
    return {"warnings": len(findings), "categories": dict(sorted(Counter(f["category"] for f in findings).items())), "findings": findings, "mode": "read-only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event_file", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.event_file.read_text(encoding="utf-8"))
        print(json.dumps(analyze(data), indent=2))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
