import streamlit

# Draw a title and some text to the app:
'''
# This is the document title

This is some _markdown_.
'''

import pandas as pd

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df
