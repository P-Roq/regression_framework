# Issues / problems

## Feature Selection

    - What initial features to include for this stage of the analysis when `initial_x_vars_fs` is empty. The idea is that the program should identify features and target variables by default in case the user does not intent to manually define features and targets. This is a desirable program features because in the event that the data set has many initial variables, it may be cumbersome to manually choose them manually. 

    - Regarding the univariate (select k best) algorithm

        - Warning pops up when using constant arrays.
    
        - 'chi2' criterion giving error during runtime.


## Converting the jupyter notebook into a PDF document

    - [still giving problems, needs revision] `nbconvert` (the app that converts the 'output.ipynb' file into a PDF documents) is connected to a browser, whose purpose it to use JavaScript code to process and render the HTML output of the notebooks. Because of that, when the cache of the browser is not cleared, `nbconvert` can sometimes convert older versions of the ipynb file instead of the current. The solution this problem is to clear the browser's cache. A better alternative would be to skip the Jupyter notebook as a means to export the PDF file and use a package such as `Reportlab`.

