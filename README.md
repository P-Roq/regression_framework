# Project: A Linear Regression Framework Based On Modular Programming
  

## Details

1. The overall purpose of the application:

    - This application pre-configures a linear regression workflow which aims at streamlining several statistical analysis processes, from exploratory data analysis up to predictive quality comparison between estimated models. To achieve this, a control script is set with a pre-defined number of hyperparameters that instructs the program to produce a customized and comprehensive statistical analysis report that can be exported into a PDF document. The main goal of the application is to allow the user to pick any data set and conduct a quick, scalable and customizable analysis that permits to easily visualize, modify and compare data, integrate support machine learning algorithms for feature selection and data randomization, produce multiple regressions and comprehensive batteries of error hypothesis testing, without having to always write the base code from the ground up, while resorting to a simplified, user friendly, set of commands. 


2. How the application can be used to address specific needs or objectives:

    - A problem arises when a researcher wants to try several approaches to the various stages of the analysis before it settles into a final configuration that wishes to interpret and explain -- e.g. changing the variables to be analyzed; determining how many experimental regressions to perform; omit or ignore one or more sections of the analysis, but has no way simple way to quickly produce or reproduce a modified version of the current analysis. This program allows the researcher to perform several exploratory and statistical tasks, by ony changing or omitting control arguments in a single dedicated control script without having to constantly change the core structure of the framework. The framework includes machine learning algorithms that allow for enhancement and automatization of certain aspects of the analysis, such has features selection and model validation techniques.
      

3. The main features and functions of the application:

    - Produce a full or partial linear regression analysis workflow in a Jupyter Notebook.
        - Choose what sections (stages or sub-sections of the analysis) to be performed.
        - Store multiple reports by either storing the control script or by exporting the report into a PDF document.
        - Automatically store a processed data set into a CSV file by setting its name in the control script.

    - It allows to change a number of arguments at several stages of the data pipeline that modify aspects of:
        - Exploratory data analysis / data visualization.
        - Data processing, transformation and splitting.
        - Regression analysis and sub-component analysis.

    - The control script is a module identified by the initial expression 'ctrl', e.g. 'ctrl_template.py'.  


4. The target audience the application is designed for:

    - The app is targeted to students/researchers/practitioners within the econometrics, data analysis, data science fields. 


5. The value the application provides to users:

    - By having a pre-configured data workflow, researchers can spend more time efficiently exploring a set of essential tools in data analysis and linear regression methodology, without having to constantly re-writing necessary code. 


6. Any potential benefits or advantages to using the application:

    - The benefits of this program are directly related with the use of a modular approach to the structure/framework of the analysis. Some of the benefits:
        - volume of code to be written decreases substantially
        - multiple libraries loaded without the need to specify them or to explicitly use their specific classes, functions, methods, etc
        - the ctrl script uses simplified syntax that is easier to use for users not familiarized with programming languages, instead of using   
        - code reuse:
            - extend sections of the analysis, e.g. multiple regressions
            - make multiple analysis of the same data set
            - use any data set
        - better code organization
            - easier feature implementation 
        - easier troubleshooting
        - time efficiency


7. The cost associated with using the application:

    - The major disadvantage of this app is the loss of flexibility:
        - It follows a pre-configured workflow which doesn't allow to perform an analysis or statistical tests beyond what has been built-in. (although, like aforementioned in point 6, it is easier to add new features to the program due to its organization)
    
        - Similarly, functions may have a reduced scope, e.g. in regards to the Feature Selection section, only 4 of the 11 algorithms available in the Scikit-learn library are evoked by the app.  

        - Less flexibility to customize graphs, e.g. axis scales, bin sizes (histograms), colors, etc. since these are pre-configured as well.   

        - The work flow of the analysis follows a pre-determined order. 

    - The implementation of new app features such as new statistical tests or machine learning support algorithms is more complex than the traditional approach.  



8. The usability and user experience design of the application:

    - The use of the app is supposed to be simple as the user only has to change values in a pre-configured control script and run the program via Jupyter notebook.


10. The ongoing support and maintenance services available for the application

    - There just a few customized error/warning messages built-in, but for most cases, if the control script is not well set (e.g. missing dictionary key, sub-section of the analysis activated when the parent section is deactivated, etc.), errors may arise and the user must be able to at least be able detect if there is some error in the set-up of the control script, or if there is some incompatibility between the data set, or any other error that may transpire. 
