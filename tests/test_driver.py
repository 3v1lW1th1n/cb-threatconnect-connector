import unittest
import threading
import traceback
from cbopensource.driver import threatconnect
from tests.utils.threatconnect_mock_server import get_mocked_server


class TestTcDriverMockedServer(unittest.TestCase):

    def setUp(self):
        self.mock_tc_server = get_mocked_server("tests/data")
        kwargs = {"sources": "*",
                  "url": "http://localhost:7982/api",
                  "web_url": "http://localhost:7982/auth",
                  "api_key": "adfasfdsa",
                  "secret_key": "asfdsafdsa",
                  "default_org": "Carbon Black",
                  "ioc_types": "File,Address,Host"}
        tcconfig = threatconnect.ThreatConnectConfig(**kwargs)
        threatconnect.ThreatConnectDriver.initialize(tcconfig)
        self.driver = threatconnect.ThreatConnectDriver(tcconfig)
        t = threading.Thread(target=self.mock_tc_server.run, args=('127.0.0.1', 7982), kwargs={"debug": False})
        t.daemon = True
        t.start()

    def test_driver_against_mock(self):
        reports = threatconnect.ThreatConnectDriver.generate_reports(self.driver)
        self.assertTrue(reports, "Didn't get any reports!")


class TestTcConfig(unittest.TestCase):
    def test_tc_config(self):
        kwargs = {"sources": "Carbon Black",
                  "url": "https://api.sandbox.threatconnect.com/api",
                  "web_url": "https://api.sandbox.threatconnect.com/auth",
                  "api_key": "adfasfdsa",
                  "secret_key": "asfdsafdsa",
                  "default_org": "Carbon Black",
                  "ioc_types": "file"}
        tcconfig = threatconnect.ThreatConnectConfig(**kwargs)

    def test_tc_config_all_types_if_none(self):
        kwargs = {"sources": "Carbon Black",
                  "url": "https://api.sandbox.threatconnect.com/api",
                  "web_url": "https://api.sandbox.threatconnect.com/auth",
                  "api_key": "adfasfdsa",
                  "secret_key": "asfdsafdsa",
                  "default_org": "Carbon Black"}
        tcconfig = threatconnect.ThreatConnectConfig(**kwargs)

    def test_tc_config_bad_ioc_min(self):
        kwargs = {"sources": "Carbon Black",
                  "url": "https://api.sandbox.threatconnect.com/api",
                  "web_url": "https://api.sandbox.threatconnect.com/auth",
                  "api_key": "adfasfdsa",
                  "secret_key": "asfdsafdsa",
                  "default_org": "Carbon Black",
                  "ioc_min_rating": 6}
        with self.assertRaises(ValueError):
            tcconfig = threatconnect.ThreatConnectConfig(**kwargs)

        kwargs["ioc_min_rating"] = -1
        with self.assertRaises(ValueError):
            tcconfig = threatconnect.ThreatConnectConfig(**kwargs)

        kwargs["ioc_min_rating"] = "text"
        with self.assertRaises(ValueError):
            tcconfig = threatconnect.ThreatConnectConfig(**kwargs)

    def test_tc_config_bad_configs(self):
        kwargs = {"sources": "Carbon Black",
                  "url": "https://api.sandbox.threatconnect.com/api",
                  "web_url": "https://api.sandbox.threatconnect.com/auth",
                  "api_key": "adfasfdsa",
                  "secret_key": "asfdsafdsa",
                  "default_org": "Carbon Black"}
        toremove = ["url", "web_url", "api_key", "secret_key"]
        for remove in toremove:
            with self.assertRaises(ValueError):
                mykwargs = kwargs.copy()
                del mykwargs[remove]
                tcconfig = threatconnect.ThreatConnectConfig(**mykwargs)


if __name__ == "__main__":
    unittest.main()
