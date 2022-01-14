#Run with: python smarts_check_latlon.py <path to input file>
#          python smarts_check_latlon.py input/unique_applications.csv
import csv
import latlon
import sys

def county_check_latlon(in_fname, out_fname1 = 'output/records_pass_latlon_qa.csv', \
                        out_fname2 = 'output/records_fail_latlon_qa.csv'):

    fname= 'unique_applications.csv' #reading input file name to opeN
    print(fname) #outputs input file name to screen
    fin=open(fname,'r')
    reader = csv.reader(fin) #handle to open file with csv reader
    index=0   # index to count number of records with problems in the input file
    header = next(reader)
    #Handles for output files
    #of1 = open('output/records_pass_latlon_qa.csv','wt')
    of1 = open(out_fname1, 'wt')
    #of2 = open('output/records_fail_latlon_qa.csv','wt')
    of2 = open(out_fname2, 'wt')
    csv_good_writer = csv.writer(of1)
    csv_bad_writer = csv.writer(of2)
    csv_good_writer.writerow(header)
    csv_bad_writer.writerow(header)
    #--------------------------------
    reader = csv.reader(fin) #handle to open file with csv reader
    for line in reader:
        try: #checks to make sure latitude value read, is a numerical
            lat=float(line[14])
        except:
            print('!!!!! check lat=%s is not numerical %s' % (line[14],line)) #screen output (not numerical latitude value)
        try: #checks to make sure longitude value read, is a numerical
            lon=float(line[15])
        except:
            print('!!!!! check lon=%s is not numerical %s' % (line[15],line)) #screen output (not numerical longitude value)
        cty=str(line[16]).upper() #converts county field read from input file to uppercase for comparison
        co_name=latlon.check(lon,lat,'CO_NAME') #Uses latitude and longitude to obtain county. It stores into variable: co_name
        co_name=co_name.upper()   #converts co_name data to uppercase
        if cty != co_name: #If there is not a match it means the county read and county calculated do not match. Record should be checked.
            index+=1
            #print('%s,!!!!! check lat=%s lon=%s is in %s not in %s  ,%s' % (index,lat,lon,co_name,cty,line))
            csv_bad_writer.writerow(line) # writes record that needs to be checked
        else:
            csv_good_writer.writerow(line) # writes good record
    print('Completed checking. Found %s rows that need further latitude, longitude revision.' % (index))

if __name__ == '__main__':
    main()
