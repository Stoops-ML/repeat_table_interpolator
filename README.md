# Repeated value table interpolation

This script allows table interpolation that contain repeated values.
An example of a table with repeated values is show below (taken from [example_table.png](example_table.png)), where the 
first three columns are independent variables that repeat and the last two columns are dependent variables to be 
interpolated.

![alt text](example_table.png "Sample table")

##Project goal
The aim of this project is to create an interpolation script that can interpolate tables with repeated values. Such tables
are very common in aerospace engineering where drag is detailed at repeated values of speed, height, lift values etc.
Interpolating such tables is time consuming by hand as the number of calculations increases exponentially with the number 
of columns: `sum([2**i for i in range(1, n_columns+1)])`.


##Capabilities
- script can handle any table with repeated values
- interpolate along any number of independent and dependent variables
- moving of columns to the far right of the table. This is necessary if the user wants to move a column to the position 
of the dependent variables (i.e. the far right). Controlled by the `move_columns` argument.
