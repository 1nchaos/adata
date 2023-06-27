import adata

# class MyTestCase(unittest.TestCase):
#
#     def stock_lifting_last_month(self):
#         df = adata.sentiment.stock_lifting_last_month()
#         print(df)
#         self.assertEqual(True, len(df) > 1)


if __name__ == '__main__':
    df = adata.sentiment.stock_lifting_last_month()
    print(df)
