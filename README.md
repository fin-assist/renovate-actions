# FinAssist Renovate Actions

This repository supplies the shared Renovate policy controller and regression suite for public consumers.

- `renovate-policy-tests` runs the policy and locked-runtime suites against consumer configuration on a read-only runner.
- `renovate-policy` runs the controller on the consumer's default branch with its existing protected environment and credentials.

Pin both Actions, the test inputs and the consumer source manifest to the same full commit SHA. The consumer owns its required checks, activation flag, policy data and runtime lock. Test jobs must run without a mutation credential.

For local checks, run the policy and runtime modes of `common/renovate/test.py` against a consumer checkout pinned to this source revision. The runtime mode expects the consumer's locked Renovate installation.
