from unittest import TestCase

from home.collect.handlers import BaseHandler, LoggingHandler, RecordingHander

TEST_PACKET = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00')


class BaseHandlerTestCase(TestCase):

    def setUp(self):

        self.handler = BaseHandler()

    def test_logger(self):

        self.assertEquals(self.handler.log.name, 'home.collect.BaseHandler')

    def test_format_packet(self):

        formatted = self.handler.format_packet(TEST_PACKET)
        expected = '0x11 0x5a 0x01 0x00 0x2e 0xb2 0x03 0x00 0x00'

        self.assertEquals(formatted, expected)


class LoggingHandlerTestCase(TestCase):

    def setUp(self):

        self.handler = LoggingHandler()
        self.log_name = 'home.collect.LoggingHandler'

    def test_logger(self):

        self.assertEquals(self.handler.log.name, self.log_name)

    def test_packet_logged(self):

        with self.assertLogs(self.log_name, level='INFO') as cm:

            self.handler(TEST_PACKET)

            self.assertEquals(cm.output, [])


class RecordingHanderTestCase(TestCase):

    def setUp(self):

        self.handler = RecordingHander({})

    def test_logger(self):

        n = self.handler.log.name
        self.assertEquals(n, 'home.collect.RecordingHander')
