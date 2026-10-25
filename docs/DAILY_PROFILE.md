# Daily inspiration, curiosity and contribution snake

The profile refreshes daily, scheduled for **08:23 China time (00:23 UTC)**. GitHub may delay scheduled workflows. It can also be refreshed manually from the [Refresh daily profile workflow](https://github.com/Khalil-Work/khalil-work/actions/workflows/snake.yml).

## What changes

- **Daily inspiration:** general life and reflection quotes from [ZenQuotes](https://zenquotes.io/). The author is displayed. If the provider's daily selection is too long for a readable card, a short attributed quote is selected from its feed instead. Inspirational quotes provided by ZenQuotes API.
- **Daily curiosity:** one general-knowledge question with four choices and a collapsible answer. The question and choices come from [Open Trivia DB](https://opentdb.com/), under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The adapted trivia text and cards retain that license. No computer-science category filter is used.
- **When I push:** a sample of up to 300 recent public GitHub events within 30 days. Only this account's `PushEvent` events are counted, once per event ID. Events are grouped by their actual event timestamp in UTC+8: night 00–05, morning 06–11, afternoon 12–17, evening 18–23. This is **push timing**, not a count of individual commits, a complete activity history, or hours worked. Private activity is excluded. Author dates and reconstructed calendar records are not used to calculate this panel.
- **Contribution snake:** [Platane/snk](https://github.com/Platane/snk) reads the existing GitHub calendar and generates a purple animated SVG, with light and dark variants. It is an animation, not an interactive game. The existing calendar includes [disclosed reconstructed date records](CALENDAR_HISTORY_2024_2026.md).

## Reliability and accessibility

The quote and trivia are cached for the local calendar day. A manual rerun keeps the same daily content. When a source fails, the previous successful item and its original date remain visible. The workflow does not replace it with an invented quotation or answer. Network requests have timeouts, bounded responses and limited retries. Source text is escaped before SVG rendering.

Light and dark cards follow the viewer's color-scheme preference. [Read all current content as ordinary text](https://github.com/Khalil-Work/khalil-work/blob/output/daily/README.md), including the sample counts and refresh time. The four featured project GIFs retain their existing still alternatives.

## Publication

The daily assets live on the separate **output** branch. The automation uses GitHub's repository-scoped token, attributed to `github-actions[bot]`, with no personal token or extra login. It preserves output-branch history and unrelated files and rejects non-fast-forward updates. It does not rewrite source commits, alter contribution dates, change profile privacy, or change the native heatmap. The daily refresh does not commit to the default branch.

Dependencies are pinned to exact commits. The generator and publisher use Python's standard library. Five offline tests cover timezone boundaries, duplicate/foreign/old-event filtering, provider failures, daily caching, text escaping and answer consistency. The workflow stops before publication if a test or generation step fails.

## Native GitHub profile sections

GitHub controls the **Popular repositories** section and the **Contribution activity** timeline outside this README. It currently documents replacing Popular repositories with pinned repositories, but no independent hide switch. Making a profile private also hides the contribution graph. Those settings were left unchanged to preserve the public heatmap.

Sources: [profile contributions](https://docs.github.com/en/account-and-profile/concepts/contributions-on-your-profile), [private/public profile differences](https://docs.github.com/en/account-and-profile/concepts/personal-profile#differences-between-private-and-public-profiles), [public events and retention](https://docs.github.com/en/rest/activity/events#about-github-events), [scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), [ZenQuotes API](https://docs.zenquotes.io/zenquotes-documentation/), [Open Trivia DB API](https://opentdb.com/api_config.php), [pinned snake action](https://github.com/Platane/snk/blob/d8f6715049803e982ee5ff501b6b9b7d5deeb09b/svg-only/action.yml).
