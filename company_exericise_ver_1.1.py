import csv  # module used to read the csv file
import itertools # module used for readers
import heapq # module used for reducing the complexity while sorting on the company_share_price
import os # module jused to exit from the program if data in csv file is inappropriate while validating

class Stock(object):
    """ Abstract class for building company share price for different companies for specific month and year"""
    def __init__(self, data,index):
        self.year = data[0]
        self.month = data[1]
        self.price = data[index]
        
#check if the given file exists or not
try:
    
    """ *********************readers to calculate num_rows and num_cols in csv file******************************** """
    # Mention the file location of the csv file
    # Read the file in 2 different readers (one can be used to create a list of data and the other to find the number of columns in the file)
    datafile = open('company_data_exercise.csv', 'r')
    reader1, reader2 = itertools.tee(csv.reader(datafile))
    ## Find number of columns in csv file
    num_cols = len(next(reader1))
    data = list(reader2)
            
    ## Find number of rows in csv file
    num_rows = (sum(1 for row in data)) -1
    
    """ *********************validations to check year, month and prices in csv file******************************** """
    ## 'quit_value' is a variable to keep a track of the position where data in csv file is uneacceptable
    quit_value = 0
    for row_value in range(num_rows):
        ## Check if the values in 'YEAR' column of csv file are not blank. Once all values are filled, the program continues
        if not data[row_value][0]:
            print "Value of YEAR for row "+str(row_value+1)+" is empty. Please enter a value before proceeding"
            quit_value = 1
        ## Check if the values in 'MONTH' column of csv file are not blank. Once all values are filled, the program continues
        if not data[row_value][1]:
            print "Value of MONTH for row "+str(row_value+1)+" is empty. Please enter a value before proceeding"
            quit_value = 1
        ## Check if the company SHARE column values ('share_cols') are not blank and are digits.  Once all values are filled, the program continues 
        for share_cols in range(2,num_cols):
            if not str(data[row_value+1][share_cols]):
                data[row_value][share_cols]=0
                            
                
            if not str(data[row_value+1][share_cols]).isdigit():
                print "Value of COMPANY SHARE for row "+str(row_value+2)+" is not a number. Please enter a value before proceeding"
                quit_value = 1
    ## program quits when 'quit_value' is 1            
    if quit_value == 1 :
        os._exit(0)             
       
    """ *********************programming logic for the problem starts here******************************** """
    ## company data starts from 'column_index' 2
    company_index = 2
    
    ## Resetting the read position of the file object ('datafile') to it's begginning.
    datafile.seek(0)
    
    ## outer loop to iterate over all the company share prices, column-wise
    while(company_index < num_cols):
         ## 'temp_reader' is used to read rows for EACH company
         temp_reader = csv.reader(datafile)         
         ## 'company_record' is a list object which is getting prices for paticular company1, company2...company1 each time
         company_record = [] 
         ## "Stock" OBJECT is created for EACH row of the current 'company_index'
         row_records = [Stock(row,company_index) for row in temp_reader]
         ## loop for EACH row of the STOCK onject for current 'company_index' (excluding the first header row)
         for row in row_records[1:]:
            ## 'dict_company_stock' is a dictionary with key values : 'year','month','price'
            dict_company_stock = {}
            dict_company_stock['year'],dict_company_stock['month'],dict_company_stock['price']  = row.year, row.month, int(row.price)
            ## 'company_record' is a list of 'dict_company_stock' for particular company
            company_record.append(dict_company_stock)  
          ## 'highest_share' is used to calculate highest share 'price' using HEAPQ for each company with its respective 'year' and 'month'
         highest_share = heapq.nlargest(1, company_record, key=lambda s: s['price'])
         ## prints the 'highest_share' for each company
         print "Highest Share Price record for company " +str(company_index-1)+ ' is ' +str(highest_share)
       
         ## Resetting the read position of the file object ('datafile') to it's begginning.
         datafile.seek(0)
         company_index=company_index+1
    
except IOError:
    print 'No such  csv data file found'

