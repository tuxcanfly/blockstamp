#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import unittest
import archiveis
logging.basicConfig(level=logging.DEBUG)


class CaptureTest(unittest.TestCase):

    def test_capture(self):
        archive_url_1 = archiveis.capture("http://www.example.com/")
        self.assertTrue(archive_url_1.startswith("http://archive.is/"))


if __name__ == '__main__':
    unittest.main()
