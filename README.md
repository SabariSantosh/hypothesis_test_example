# hypothesis_test_example
A simple example on hypothesis test using ttest_ind from scipy.stats

<b>Definitions</b>:
1) A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
2) A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
3) A recession bottom is the quarter within a recession which had the lowest GDP.
4) A university town is a city which has a high percentage of university students compared to the total population of the city.

<b>Hypothesis</b>: University towns have their mean housing prices less effected by recessions. A t-test is run to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom.
The following data files are available for this assignment:
<ul>
<li>From the Zillow research data site there is housing data for the United States. In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, has median home sale prices at a fine grained level.</li>
<li>From the Wikipedia page on college towns is a list of university towns in the United States which has been copy and pasted into the file university_towns.txt.</li>
<li>From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in current dollars, in quarterly intervals, in the file gdplev.xls.</li>
</ul>
