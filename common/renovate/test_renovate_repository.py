"""Repository-independent policy assertions for mixed PRs."""
import base64
import json
import unittest

from renovate_policy import UPDATES, reconcile
from test_renovate_controller import Fake


class RepositoryPolicyTests(unittest.TestCase):
    def test_manual_go_identity_blocks_mixed_pr_merge_retry_and_close(self):
        identities = [('github-releases', 'actions/go-versions'),
                      ('github-tags', 'actions/go-versions'), ('docker', 'golang'),
                      ('docker', 'library/golang'), ('docker', 'docker.io/library/golang'),
                      ('golang-version', 'go'), ('golang-version', 'golang/go')]
        for datasource, name in identities:
            for conclusion, attempt in [('success', 1), ('failure', 1), ('failure', 2)]:
                with self.subTest(datasource=datasource, name=name,
                                  conclusion=conclusion, attempt=attempt):
                    api = Fake()
                    items = [{'depName': 'normal', 'datasource': 'npm', 'newValue': '2'},
                             {'depName': 'go', 'packageName': name,
                              'datasource': datasource, 'newValue': '1.27.3'}]
                    api.message = UPDATES + base64.b64encode(json.dumps(items).encode()).decode() + ' -->'
                    api.run.update(conclusion=conclusion, run_attempt=attempt)
                    api.jobs[0]['conclusion'] = conclusion
                    if attempt == 2:
                        api.receipts = {'1:abc': {'state': {'sha': 'abc', 'runs': {
                            'ci.yml': {'run_id': 1, 'attempt': 1, 'retried': True}}}}}
                    reconcile(api, api.config)
                    self.assertEqual(api.actions, [])
                    self.assertEqual(api.pr['state'], 'open')
                    self.assertEqual(api.comments, [])
