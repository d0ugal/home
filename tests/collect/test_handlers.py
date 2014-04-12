from sys import version_info
from unittest.mock import Mock, patch, ANY
from unittest import skipIf

from tests.base import BaseTestCase

from rfxcom.protocol import Status

from home.collect import logging_handler
from home.collect.handlers import (BaseHandler, LoggingHandler,
                                   RecordingHander, load_handlers)
from home.exceptions import HandlerConfigError


def mock_packet(extra=None):

    p = Mock()
    p.raw = bytearray(b'\x11\x5A\x01\x00\x2E\xB2\x03\x00\x00')
    p.data = {
        'id': 'test',
        'packet_type': 33,
        'sub_type': 1,
    }

    if extra is not None:
        p.data.update(extra)

    return p


class HandlerLoadingTestCase(BaseTestCase):

    def test_load_handlers_empty(self):

        result = load_handlers({})

        self.assertEqual(result, {})

    def test_load_handlers_duplicate(self):

        with self.assertRaises(HandlerConfigError):
            load_handlers({
                'rfxcom.protocol.Status': 'home.collect.logging_handler',
                Status: 'home.collect.logging_handler',
            })

    def test_load_handlers_bad_path(self):

        with self.assertRaises(ImportError):
            load_handlers({
                'rfxcom.protocol..Status': 'home.collect.logging_handler'
            })

    def test_load_handlers_wildcard(self):

        result = load_handlers({
            '*': 'home.collect.logging_handler',
        })

        self.assertEqual(result, {
            '*': logging_handler
        })

    def test_load_handlers_all_objects(self):

        h = lambda x: x

        result = load_handlers({
            Status: h,
        })

        self.assertEqual(result, {
            Status: h
        })


class BaseHandlerTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()
        self.packet = mock_packet()
        self.handler = BaseHandler()

    def test_logger(self):

        self.assertEqual(self.handler.log.name, 'home.collect.BaseHandler')

    def test_format_packet(self):

        formatted = self.handler.format_packet(self.packet.raw)
        expected = '0x11 0x5a 0x01 0x00 0x2e 0xb2 0x03 0x00 0x00'

        self.assertEqual(formatted, expected)


class LoggingHandlerTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()
        self.packet = mock_packet()
        self.handler = LoggingHandler()
        self.log_name = 'home.collect.LoggingHandler'

    def test_logger(self):

        self.assertEqual(self.handler.log.name, self.log_name)

    @skipIf(version_info < (3, 4), "Python 3.4 required.")
    def test_packet_logged(self):

        with self.assertLogs(self.log_name, level='INFO') as cm:

            self.handler(self.packet)

            self.assertEqual(cm.output, [
                'WARNING:home.collect.LoggingHandler:Ignoring packet: 0x11 '
                '0x5a 0x01 0x00 0x2e 0xb2 0x03 0x00 0x00'
            ])


class RecordingHanderTestCase(BaseTestCase):

    def setUp(self):

        super().setUp()
        self.packet = mock_packet({
            'current_watts': 650,
            'total_watts': 100000
        })
        self.handler = RecordingHander({
            'electricity': 'current_watts',
        })
        self.log_name = 'home.collect.RecordingHander'

    def test_logger(self):

        n = self.handler.log.name
        self.assertEqual(n, 'home.collect.RecordingHander')

    @patch('home.ts.models.DataPoint.record')
    def test_record(self, mock_record):

        self.handler(self.packet)

        mock_record.assert_called_once_with(ANY, ANY, 650)

    @skipIf(version_info < (3, 4), "Python 3.4 required.")
    @patch('home.ts.models.DataPoint.record')
    def test_record_missing(self, mock_record):

        self.handler = RecordingHander({
            'electricity': 'not_a_correct_attribute',
        })

        with self.assertLogs(self.log_name, level='ERROR') as cm:
            self.handler(self.packet)
            self.assertEqual(cm.output, [
                "ERROR:home.collect.RecordingHander:Failed to find "
                "not_a_correct_attribute in packet. Key list: ['current_watts'"
                ", 'id', 'packet_type', 'sub_type', 'total_watts']"
            ])

        assert not mock_record.called, 'method should not have been called'
