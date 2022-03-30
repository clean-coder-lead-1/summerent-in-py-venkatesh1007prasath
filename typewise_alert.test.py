#!/usr/bin/env python3
import io
import unittest.mock
import unittest
import typewise_alert


class TypeWiseTest(unittest.TestCase):
    def test_infers_breach_as_per_limits(self):
        self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
        self.assertTrue(typewise_alert.infer_breach(60, 50, 100) == 'NORMAL')
        self.assertTrue(typewise_alert.infer_breach(120, 50, 100) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.infer_breach(0, -5, 25) == 'NORMAL')

    def test_classify_temperature_breach_as_per_cooling_type(self):
        self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 20) == 'NORMAL')
        self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', -1) == 'TOO_LOW')
        self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 40) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 30) == 'NORMAL')
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', -1) == 'TOO_LOW')
        self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 50) == 'TOO_HIGH')
        self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 20) == 'NORMAL')
        self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', -1) == 'TOO_LOW')
        self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 45) == 'TOO_HIGH')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_send_to_controller(self, mock_stdout):
        typewise_alert.send_to_controller('TOO_LOW')
        self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_LOW")  # test1 of send_to_controller
        typewise_alert.send_to_controller('TOO_HIGH')
        self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_HIGH")  # test2 of send_to_controller
        typewise_alert.send_to_controller('NORMAL')
        self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, NORMAL")  # test3 of send_to_controller

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_send_to_email(self, mock_stdout):
        typewise_alert.send_to_email('TOO_LOW')
        self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too low'])    # test1 of send_to_email
        typewise_alert.send_to_email('TOO_HIGH')
        self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too high'])    # test2 of send_to_email

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_check_and_alert(self, mock_stdout):
        # ========================= PASSIVE_COOLING======================================
        typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "PASSIVE_COOLING"}, 25)
        self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, NORMAL")   # test of check_and_alert to PASSIVE

        # typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "PASSIVE_COOLING"}, -5)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_LOW")   # test of check_and_alert to PASSIVE
        #
        # typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "PASSIVE_COOLING"}, 50)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_HIGH")   # test of check_and_alert to PASSIVE
        #
        # typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "PASSIVE_COOLING"}, 25)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "NORMAL")   # test of check_and_alert to PASSIVE
        #
        # typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "PASSIVE_COOLING"}, -5)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too low'])   # test of check_and_alert to PASSIVE

        typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "PASSIVE_COOLING"}, 50)
        self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too high'])   # test of check_and_alert to PASSIVE

        # ========================= MED_ACTIVE_COOLING======================================
        typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "MED_ACTIVE_COOLING"}, 25)
        self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, NORMAL")   # test of check_and_alert to MID_ACTIVE

        # typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "MED_ACTIVE_COOLING"}, -5)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_LOW")   # test of check_and_alert to MID_ACTIVE
        #
        # typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "MED_ACTIVE_COOLING"}, 50)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_HIGH")   # test of check_and_alert to MID_ACTIVE
        #
        # typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "MED_ACTIVE_COOLING"}, 25)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "NORMAL")   # test of check_and_alert to MID_ACTIVE
        #
        # typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "MED_ACTIVE_COOLING"}, -5)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too low'])   # test of check_and_alert to MID_ACTIVE

        typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "MED_ACTIVE_COOLING"}, 50)
        self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too high'])   # test of check_and_alert to MID_ACTIVE

        # ========================= HI_ACTIVE_COOLING======================================
        typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "HI_ACTIVE_COOLING"}, 25)
        self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, NORMAL")   # test of check_and_alert to HI_ACTIVE

        # typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "HI_ACTIVE_COOLING"}, -5)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_LOW")   # test of check_and_alert to HI_ACTIVE
        #
        # typewise_alert.check_and_alert('TO_CONTROLLER', {"cooling_type": "HI_ACTIVE_COOLING"}, 50)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "65261, TOO_HIGH")   # test of check_and_alert to HI_ACTIVE
        #
        # typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "HI_ACTIVE_COOLING"}, 25)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-2], "NORMAL")   # test of check_and_alert to HI_ACTIVE
        #
        # typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "HI_ACTIVE_COOLING"}, -5)
        # self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too low'])   # test of check_and_alert to HI_ACTIVE

        typewise_alert.check_and_alert('TO_EMAIL', {"cooling_type": "HI_ACTIVE_COOLING"}, 50)
        self.assertEqual(mock_stdout.getvalue().split("\n")[-3:-1], ['To: a.b@c.com', 'Hi, the temperature is too high'])   # test of check_and_alert to HI_ACTIVE


if __name__ == '__main__':
    unittest.main()
