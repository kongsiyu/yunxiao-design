# Heartbeat Checklist

- Check GitHub Issues for new/updated items across all yunxiao projects (cli, design)
- Check for any completed or stuck background tasks → summarize results if any
- Check PRs with `needs-fix` label → Read PR comments with `[FIX NEEDED]` → Fix issues (P0)
- Check PRs with `changes-requested` → Address reviewer feedback (P1)
- Track fix progress in `memory/heartbeat-state.json` (record PR number, last commit SHA, status)
- If no PR needs attention, start next pending GitHub Issue using `claude` in background mode
- If idle for 8+ hours, send a brief check-in to Sue
- Cache GitHub Issue status in `memory/heartbeat-state.json` to avoid redundant checks
- Report work summary to Sue via DingTalk group (channel: cidWNYKHzGnfG0L5q0U6PaFkA==)

## GitHub Operations

### Check PRs with needs-fix label

```bash
gh pr list --state open --label "needs-fix" --json number,title
```

### Read PR comments (look for [FIX NEEDED])

```bash
gh pr view <N> --json comments
# Example: gh pr view 18 --json comments
```

### Reply to PR comment after fix

```bash
gh pr comment <N> --body "Fixed in commit <SHA>"
```

### User Workflow

1. **Review PR** → Find issue → Add `needs-fix` label
2. **Add PR comment** → Start with `[FIX NEEDED]` + describe the issue
   - Example: `[FIX NEEDED] Line 15: Add null check before accessing user.name`
3. **Agent fixes** → Pushes new commit → Replies "Fixed in commit abc123"
4. **You verify** → If fixed, **remove `needs-fix` label**
5. **New issue** → Add new `[FIX NEEDED]` comment

## Comment Format

- **Must start with**: `[FIX NEEDED]`
- **Include**: Line number (if applicable) + description
- **Agent reply**: `Fixed in commit <SHA>` or `Will fix in next commit`
