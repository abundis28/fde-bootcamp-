# Real vs Mocked Trade-Off

## Real
Real tests are useful to make sure the server responds and the requests go through but these are expensive and may take time.
Different responses are hard to get on-demand since external factors impact the outcome.

## Mocked
Useful and fast to detect logic issues (e.g. response handling issue).
May not test the same external factors that are a "con" in the real tests.

# Raised issues

## First review
1. Every successful call prints a fake "API Error."
The else binds to the second if, so any status that isn't ≥500 — including 200 — falls into it and prints an error on a perfectly good response. Your tests didn't catch it because none assert on stdout. Same lesson as the cart: a test only protects what it asserts.
2. Your error-handling try/except is dead code.
You catch httpx.HTTPStatusError, but that exception is only raised by response.raise_for_status() — which you never call. I grepped to confirm: raise_for_status() appears nowhere. So that except block can never execute. It looks like robust error handling and does nothing — which is exactly the kind of thing you'll be hunting in AI output in Week 4. Either call response.raise_for_status() and handle the exception it throws, or keep your manual status checks and delete the dead try/except. Don't keep both — pick one model.
3. You return the raw Response, but the spec asked for data.
get_user should return the user dict, get_repos the list of repos. Right now both return the httpx.Response object and the caller still has to call .json(). That means your "client" isn't actually wrapping anything — it leaks the transport layer to every caller. Return response.json() (the dict/list) so the client is a real abstraction. This is the whole point of a client module.
4. Your own 404-vs-500 decision isn't realized in the code
You told me, correctly: "404 is the user's fault, 500 is the server's fault — different errors for each." Good instinct. But both paths raise the same type, ValidationFailed, differing only by a message string. User would have to catch the one generic type and inspect .partial_data["status"] with an if. Your stated design ("different errors") and your implementation ("same type, different string") disagree — the signature/behavior mismatch theme again. Make the distinction real: two exception types (optionally sharing a base). Then the 404/500 split you correctly reasoned about becomes something a caller can actually act on — which is the entire reason the distinction matters.
5. Naming lies a little.
ValidationFailed — nothing is being validated; a 404 is "not found," a 500 is "server error." And your 404 message is literally "Key error" (a leftover). Names and messages are documentation; make them true: UserNotFoundError, GitHubServerError.
6. Your repos "found" mock returns a dict, not a list
test_gh_user_repos_found mocks {"login": "octocat"}, but the real /repos endpoint returns a JSON array. A mock that lies about the response shape can pass while your real parsing is wrong — the classic mocked-test risk you described well in NOTES.md. Mock a small list of repo dicts and assert you get a list back.
7. De-duplicate.
Your two functions are near-identical copy-paste (same error block). Factor the request-and-handle into one helper (_get(url)), then get_user/get_repos just build the URL and parse. You learned this move on Day 3 — apply it here.