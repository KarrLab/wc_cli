""" Tests of wc command line interface (wc.__main__)

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2018-05-15
:Copyright: 2018, Karr Lab
:License: MIT
"""

from wc import __main__
import capturer
import mock
import os
import tempfile
import unittest
import wc


class TestCore(unittest.TestCase):
    def setUp(self):
        fid, self.filename = tempfile.mkstemp(suffix='.xlsx')
        os.close(fid)

    def tearDown(self):
        os.remove(self.filename)

    def test_cli(self):
        with mock.patch('sys.argv', ['wc', '--help']):
            with self.assertRaises(SystemExit) as context:
                __main__.main()
                self.assertRegexpMatches(context.Exception, 'usage: wc')

    def test_help(self):
        with self.assertRaises(SystemExit):
            with __main__.App(argv=['--help']) as app:
                app.run()
            self.assertRegexpMatches(context.Exception, 'usage: wc')

        with capturer.CaptureOutput(merged=False, relay=False) as captured:
            with __main__.App(argv=[]) as app:
                app.run()
            self.assertRegexpMatches(captured.stdout.get_text(), 'usage: wc')
            self.assertEqual(captured.stderr.get_text(), '')

    def test_version(self):
        with __main__.App(argv=['-v']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                with self.assertRaises(SystemExit):
                    app.run()
                self.assertEqual(captured.stdout.get_text(), wc.__version__)
                self.assertEqual(captured.stderr.get_text(), '')

        with __main__.App(argv=['--version']) as app:
            with capturer.CaptureOutput(merged=False, relay=False) as captured:
                with self.assertRaises(SystemExit):
                    app.run()
                self.assertEqual(captured.stdout.get_text(), wc.__version__)
                self.assertEqual(captured.stderr.get_text(), '')

    def test_model_help(self):
        with capturer.CaptureOutput(merged=False, relay=False) as captured:
            with __main__.App(argv=['model']) as app:
                # run app
                app.run()

                # test that the CLI produced the correct output
                self.assertRegexpMatches(captured.stdout.get_text(), 'mycoplasma-pneumoniae')
                self.assertEqual(captured.stderr.get_text(), '')

    def test_tool_help(self):
        with capturer.CaptureOutput(merged=False, relay=False) as captured:
            with __main__.App(argv=['tool']) as app:
                # run app
                app.run()

                # test that the CLI produced the correct output
                self.assertRegexpMatches(captured.stdout.get_text(), 'kb')
                self.assertRegexpMatches(captured.stdout.get_text(), 'lang')
                self.assertRegexpMatches(captured.stdout.get_text(), 'sim')
                self.assertEqual(captured.stderr.get_text(), '')

    def test_tool_wc_lang(self):
        os.remove(self.filename)

        with __main__.App(argv=['tool', 'lang', 'create-template', self.filename, '--ignore-repo-metadata']) as app:
            # run app
            app.run()

        self.assertTrue(os.path.isfile(self.filename))
