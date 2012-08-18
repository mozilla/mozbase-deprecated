# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from mozautolog import RESTfulAutologTestGroup

from base import Output, count, long_name


class AutologOutput(Output):

    def __init__(self, es_server='buildbot-es.metrics.scl3.mozilla.com:9200',
                 rest_server='http://brasstacks.mozilla.com/autologserver',
                 name='moztest',
                 harness='moztest'):
        self.es_server = es_server
        self.rest_server = rest_server
        self.name = name
        self.harness = harness

    def serialize(self, results_collection, file_obj):
        file_obj.write(self.make_testgroup(results_collection).serialize())

    def make_testgroups(self, results_collection):
        testgroups = []
        for context in results_collection.contexts:
            coll = results_collection.subset(lambda t: t.context == context)
            passed = coll.tests_with_result('PASS')
            failed = coll.tests_with_result('UNEXPECTED-FAIL')
            unexpected_passes = coll.tests_with_result('UNEXPECTED-PASS')
            errors = coll.tests_with_result('ERROR')
            skipped = coll.tests_with_result('SKIPPED')
            known_fails = coll.tests_with_result('KNOWN-FAIL')

            testgroup = RESTfulAutologTestGroup(
                 testgroup=self.name,
                 os=context.os,
                 platform=context.arch,
                 harness=self.harness,
                 server=self.es_server,
                 restserver=self.rest_server,
                 machine=context.hostname,
                )
            testgroup.add_test_suite(
                testsuite=results_collection.suite_name,
                elapsedtime=coll.time_taken,
                passed=count(passed),
                failed=count(failed) + count(errors) + count(unexpected_passes),
                todo=count(skipped) + count(known_fails),
                )
            testgroup.set_primary_product(
                tree=context.tree,
                revision=context.revision,
                productname=context.product
                )
            for f in failed:
                testgroup.add_test_failure(
                    test=long_name(f),
                    text='\n'.join(f.output),
                    status=f.result_actual
                    )
            testgroups.append(testgroup)
        return testgroups

    def post(self, *data):
        msg = "Must pass in data returned by make_testgroups."
        for d in data:
            assert isinstance(d, RESTfulAutologTestGroup), msg
            d.submit()
