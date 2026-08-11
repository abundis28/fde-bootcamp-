# Real vs Mocked Trade-Off

## Real
Real tests are useful to make sure the server responds and the requests go through but these are expensive and may take time.
Different responses are hard to get on-demand since external factors impact the outcome.

## Mocked
Useful and fast to detect logic issues (e.g. response handling issue).
May not test the same external factors that are a "con" in the real tests.