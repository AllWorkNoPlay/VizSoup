import json
import unittest

from trade_signal import TradeSignal

class TradeSignalTests(unittest.TestCase):
    def test_serialization(self):
        signal = TradeSignal("buy", ["price", "quantity"])
        signal.price = 100
        signal.quantity = 10

        expected_json = '{\n    "price": 100,\n    "quantity": 10,\n    "type": "buy"\n}'

        self.assertEqual(signal.toJSON(), expected_json.strip())

    def test_list_serialization(self):
        signals = [
            TradeSignal("buy", ["price", "quantity"]),
            TradeSignal("sell", ["price", "quantity"])
        ]

        signals[0].price = 100
        signals[0].quantity = 10
        signals[1].price = 200
        signals[1].quantity = 5

        expected_json = '[\n    {\n        "price": 100,\n        "quantity": 10,\n        "type": "buy"\n    },\n    {\n        "price": 200,\n        "quantity": 5,\n        "type": "sell"\n    }\n]'

        self.assertEqual(json.dumps(signals, default=lambda o: o.__dict__, sort_keys=True, indent=4), expected_json.strip())

    # we don't want to include empty properties in the JSON
    def test_empty_property(self):
        signal = TradeSignal("buy", ["", "quantity"])
        signal.quantity = 10

        expected_json = '{\n    "quantity": 10,\n    "type": "buy"\n}'

        self.assertEqual(signal.toJSON(), expected_json.strip())




if __name__ == '__main__':
    unittest.main()