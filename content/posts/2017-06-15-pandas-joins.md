---
slug: pandas-joins
date: "2017-06-15T00:00:00Z"
description: Joins (merge) in pandas
tags:
- pandas
- join
- merge
title: Joins (merge) in pandas
---
Dabbling in pandas recently! Here are the four kinds of merges in pandas, and how you should think of it.

![pandas-joins](/images/joins.svg)

For a left join, the keys in the dataframe returned will be the same as the keys in the left dataframe. A key in the left dataframe will be used to index the right dataframe, and then the data is combined. `NaN`s are returned where the data cannot be found in the right dataframe. The key order is that of the left dataframe.

For a right join, it's conceptually the same as a left join, except that all the lefts are now right.

For an outer join, the keys in the dataframe returned will be the union of the keys of the left and right dataframes. `NaN`s are set where the data cannot be found. Keys in the output dataframe are sorted lexicographically.

For an inner join, only keys that exist in both the left and right dataframes will appear in the output dataframe. Key order of the left dataframe is preserved. This is the default joining method.

# Relationship between data in the dataframes and number of NaNs in the resulting dataframes

![pandas-nans](/images/nans.svg)
