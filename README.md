## EI_ST4 Groupe 2

The code is divided in 
1. A package from which we call every function implemented
2. A folder data where we get and put data we've collected
3. A dash_app folder where we define two interactive Dash apps
4. A main.py file where we execute our code __We never execute our code somewhere else__

For many visualizations we use a (wonderful) package called plotly that must be installed before `pip install plotly`.
For clustering and PCA we use scikit-learn `pip install scikit-learn`.
For interactive dash apps we use the package dash `pip install dash`
Other packages are more common : matplotlib, pandas, numpy, json, datetime