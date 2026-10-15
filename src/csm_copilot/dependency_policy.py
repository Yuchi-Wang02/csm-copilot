"""Opt-in morning-review call policy for the local host, not a prose validator."""

from copy import deepcopy


class DependencyPolicyError(ValueError):
    """A proposal or tool result cannot advance the requested workflow."""


def action(tool, **arguments):
    return {"tool": tool, "arguments": arguments}


class MorningReviewPolicy:
    """Discover scope from successful results; validate batches without executing them."""

    def __init__(self):
        self.stage = "awaiting_queue"
        self.account_id = None
        self.pending = [action("list_accounts", stale_days=3, as_of=None, include_live=False)]
        self.completed = []

    def snapshot(self):
        return deepcopy(
            {
                "version": "1-morning-dependencies",
                "stage": self.stage,
                "account_id": self.account_id,
                "pending_actions": self.pending,
                "completed_actions": self.completed,
                "final_allowed": not self.pending,
                "boundary": "Host call sequencing and requested-work coverage only; final prose still needs review.",
            }
        )

    def next_action_schema(self):
        """Decoder assistance: one pending action, or a final string after completion.

        Queue arguments are omitted to use the fixed defaults. Other arguments are
        exact strings discovered by this policy. The runtime checks still apply.
        """

        def closed_object(properties):
            return {
                "type": "object",
                "properties": properties,
                "required": list(properties),
                "additionalProperties": False,
            }

        if not self.pending:
            return closed_object({"final": {"type": "string", "minLength": 1}})
        choices = []
        for pending in self.pending:
            arguments = {} if pending["tool"] == "list_accounts" else pending["arguments"]
            choices.append(
                closed_object(
                    {
                        "tool": {"type": "string", "enum": [pending["tool"]]},
                        "arguments": closed_object(
                            {
                                key: {"type": "string", "enum": [value]}
                                for key, value in arguments.items()
                            }
                        ),
                    }
                )
            )
        return choices[0] if len(choices) == 1 else {"anyOf": choices}

    @staticmethod
    def _canonical(proposal):
        if not isinstance(proposal, dict) or set(proposal) != {"tool", "arguments"}:
            raise DependencyPolicyError("Expected a tool action with arguments")
        name, args = proposal["tool"], proposal["arguments"]
        if not isinstance(name, str) or not isinstance(args, dict):
            raise DependencyPolicyError("Invalid action shape")
        args = dict(args)
        if name == "list_accounts":
            args = {"stale_days": 3, "as_of": None, "include_live": False, **args}
            if (
                type(args["stale_days"]) not in (int, float)
                or args["stale_days"] != 3
                or args["as_of"] is not None
                or args["include_live"] is not False
            ):
                raise DependencyPolicyError("Use the fixed snapshot, three-day non-live queue")
        elif name == "draft_followup":
            args.setdefault("lang", "en")
        return action(name, **args)

    def validate_batch(self, actions):
        """Reject the entire proposal before any call, including a valid prefix."""
        if not isinstance(actions, list) or not 1 <= len(actions) <= 4:
            raise DependencyPolicyError("A batch must contain 1..4 actions")
        if len(actions) == 1 and isinstance(actions[0], dict) and set(actions[0]) == {"final"}:
            if self.pending:
                raise DependencyPolicyError("Requested work remains; final response is premature")
            return
        seen = []
        for proposal in actions:
            normalized = self._canonical(proposal)
            if normalized not in self.pending:
                raise DependencyPolicyError(
                    "Action is not pending in the current stage; use IDs from preceding results"
                )
            if normalized in seen:
                raise DependencyPolicyError("Duplicate actions in one batch are not allowed")
            seen.append(normalized)

    @staticmethod
    def _records(payload, key, id_key="id"):
        rows = payload.get(key)
        if not isinstance(rows, list):
            raise DependencyPolicyError(f"Tool result needs a {key} list")
        ids = []
        for row in rows:
            identifier = row.get(id_key) if isinstance(row, dict) else None
            if not isinstance(identifier, str) or not identifier.strip() or identifier in ids:
                raise DependencyPolicyError(f"Invalid or duplicate identifier in {key}")
            ids.append(identifier)
        return rows

    def observe(self, proposal, payload, *, tool_error=False):
        """Advance only after a successful, scoped result. Errors leave work pending."""
        self.validate_batch([proposal])
        normalized = self._canonical(proposal)
        if tool_error:
            return
        if not isinstance(payload, dict):
            raise DependencyPolicyError("A successful tool result must contain structured data")
        name, args = normalized["tool"], normalized["arguments"]
        new_pending = None
        selected_account = self.account_id
        if name == "list_accounts":
            rows = self._records(payload, "accounts", "account_id")
            if payload.get("time_basis") != "dataset_snapshot" or payload.get("stale_days") != 3:
                raise DependencyPolicyError("Queue result does not describe the requested snapshot")
            selected_account = rows[0]["account_id"] if rows else None
            new_pending = (
                [action("get_account_context", account_id=selected_account)] if rows else []
            )
        elif name == "get_account_context":
            account = payload.get("account")
            if not isinstance(account, dict) or account.get("id") != self.account_id:
                raise DependencyPolicyError("Context result belongs to a different account")
            integrations = self._records(payload, "integrations")
            issues = self._records(payload, "issues")
            integration_ids = {item["id"] for item in integrations}
            if any(item.get("account_id") != self.account_id for item in integrations) or any(
                item.get("integration_id") not in integration_ids for item in issues
            ):
                raise DependencyPolicyError("Context contains records outside the selected account")
            new_pending = [
                call
                for item in integrations
                for call in (
                    action("check_readiness", integration_id=item["id"]),
                    action("draft_followup", integration_id=item["id"], lang="en"),
                )
            ] + [action("draft_ticket", issue_id=item["id"]) for item in issues]
        elif name == "check_readiness":
            if (
                payload.get("integration_id") != args["integration_id"]
                or payload.get("decision")
                not in ("blocked", "needs_evidence", "checklist_complete")
                or not isinstance(payload.get("checks"), list)
            ):
                raise DependencyPolicyError("Readiness result lacks the requested scope or checks")
        elif name in ("draft_followup", "draft_ticket"):
            if payload.get("state") != "draft" or payload.get("sent") is not False:
                raise DependencyPolicyError("Expected an unsent draft result")
            if name == "draft_followup":
                if (
                    payload.get("lang") != "en"
                    or not isinstance(payload.get("body"), str)
                    or not payload["body"].strip()
                ):
                    raise DependencyPolicyError("Expected a nonempty English follow-up")
            elif (
                payload.get("draft_id") != "ticket-" + args["issue_id"]
                or not isinstance(payload.get("fields"), dict)
                or not isinstance(payload.get("missing_fields"), list)
            ):
                raise DependencyPolicyError("Handoff result lacks the requested issue or fields")

        # All checks above finish before any state mutation.
        if new_pending is None:
            new_pending = [item for item in self.pending if item != normalized]
        self.pending = new_pending
        self.account_id = selected_account
        self.completed.append(normalized)
        self.stage = (
            "complete"
            if not self.pending
            else "awaiting_context"
            if name == "list_accounts"
            else "reviewing"
        )
