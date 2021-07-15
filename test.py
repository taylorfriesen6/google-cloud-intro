import unittest
from unittest.mock import patch, MagicMock, PropertyMock
import asyncio

import main

class MyTests(unittest.TestCase):

    def test_get_tag_stats_empty(self):
        async def f():
            with patch("main.db") as mock_db, patch("main.logger"):
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
            with patch("main.db") as mock_db, patch("main.logger"):
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

    def test_increment_count_new(self):
        async def f():
            with patch("main.db") as mock_db, patch("main.logger"):
                doc = MagicMock()
                doc.exists = False
                doc_ref = MagicMock
                doc_ref.get = MagicMock(return_value = doc)
                doc_ref.set = MagicMock()
                collection = MagicMock()
                collection.document = MagicMock(return_value = doc_ref)
                mock_db.collection = MagicMock(return_value = collection)

                tag = main.Tag()
                tag.name = "foo"
                tag.value = 2

                await main.increment_count(tag)

                mock_db.collection.assert_called_with(u'tags')
                collection.document.assert_called_with("foo")
                doc_ref.get.assert_called_with()
                doc_ref.set.assert_called_with({u'sum':2})
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f())

    def test_increment_count_present(self):
        async def f():
            with patch("main.db") as mock_db, patch("main.logger"):
                doc = MagicMock()
                doc.exists = True
                doc.to_dict = MagicMock(return_value = {u'sum':5})
                doc_ref = MagicMock
                doc_ref.get = MagicMock(return_value = doc)
                doc_ref.set = MagicMock()
                collection = MagicMock()
                collection.document = MagicMock(return_value = doc_ref)
                mock_db.collection = MagicMock(return_value = collection)

                tag = main.Tag()
                tag.name = "foo"
                tag.value = 2

                await main.increment_count(tag)

                mock_db.collection.assert_called_with(u'tags')
                collection.document.assert_called_with("foo")
                doc_ref.get.assert_called_with()
                doc_ref.set.assert_called_with({u'sum':7})
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f())

            


unittest.main()