import unittest
from unittest.mock import patch, MagicMock, PropertyMock
import asyncio

import main

class MyTests(unittest.TestCase):

    def test_get_tag_stats_empty(self):
        async def f():
            with patch("main.db") as mock_db:
                docs = iter([])
                collection = MagicMock()
                collection.stream = MagicMock(return_value = docs)
                mock_db.collection = MagicMock(return_value = collection)

                result = await main.get_tag_stats()

                mock_db.collection.assert_called_with(u'tags')
                collection.stream.assert_called_with()
                
                self.assertEqual(result, {})
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f())

    def test_get_tag_stats(self):
        async def f():
            with patch("main.db") as mock_db:
                doc1 = MagicMock()
                doc1.id = "foo"
                doc1.to_dict = MagicMock(return_value = {u'sum':5})
                doc2 = MagicMock()
                doc2.id = "bar"
                doc2.to_dict = MagicMock(return_value = {u'sum':2})
                docs = iter([doc1, doc2])
                collection = MagicMock()
                collection.stream = MagicMock(return_value = docs)
                mock_db.collection = MagicMock(return_value = collection)

                result = await main.get_tag_stats()

                mock_db.collection.assert_called_with(u'tags')
                collection.stream.assert_called_with()
                doc1.to_dict.assert_called_with()
                doc2.to_dict.assert_called_with()

                self.assertEqual(result, {"foo":5, "bar":2})
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f())


unittest.main()