# Find duplicates
import csv
import os, sys
#print('Python: {}'.format(sys.version))
import pdb
#import pandas as pd


# path to file
in_file = 'smarts_data1221.csv'

# dictionary
application_counts = {}
app_id_to_row = {}

# creating the dictionary
with open(in_file) as infile:
    csv_inf = csv.reader(infile)
    next(csv_inf)
    for line in csv_inf:
        app_id = str(line[2])
        if not app_id:
            print(line)

        if app_id in app_id_to_row and tuple(line) != app_id_to_row[app_id]:
            print('Mismatch:')
            print(app_id)
        else:
            app_id_to_row[app_id] = tuple(line)

        application_counts[app_id] = application_counts.get(app_id, 0) + 1
    print('total = ' + str(sum(application_counts.values()))) #sanity check = 33200



# trying to find sums
    a = sum(1 for i in application_counts.values() if i>=2)
    print('duplicates = ' + str(a))

    print('unique IDs =', str(len(application_counts)))

#if application_duplicates.values()>1:
#        total = sum(application_duplicates.values())
#        print(total)

# csv with application ids and how many times they occur in the data set
with open('application_counts.csv', 'w+') as counts:
    writer = csv.writer(counts)
    writer.writerow(['application_id', 'occurences'])
    for app_id, count in application_counts.items():
        #if application_counts[app_id]>1:
            writer.writerow([app_id, count])

with open('application_duplicates.csv', 'w+') as dupl:
    writer = csv.writer(dupl)
    writer.writerow(['application_id', 'occurences'])
    for app_id, count in application_counts.items():
        if count > 1:
            writer.writerow([app_id, count])



# csv containing all records removed from the original data
# application id duplicates - 1 that stays in the original to
# have only one of each project in the surrogate
unique_rows = set()
with open(in_file) as infile:
    csv_inf = csv.reader(infile)
    next(csv_inf)

    with open('duplicate_applications.csv', 'w+') as dupl:

        with open('unique_applications.csv', 'w+') as uniques:
            writer_uniques = csv.writer(uniques)
            writer_uniques.writerow(['Column1','APP_ID','WDID','STATUS','NOI_PROCESSED_DATE','NOT_EFFECTIVE_DATE','REGION','COUNTY','SITE_NAME','SITE_ADDRESS','SITE_ADDRESS_2','SITE_CITY','SITE_STATE','SITE_ZIP','SITE_LATITUDE','SITE_LONGITUDE','SITE_COUNTY','SITE_TOTAL_SIZE','SITE_TOTAL_SIZE_UNIT','SITE_TOTAL_DISTURBED_ACREAGE','TOTAL_DISTURBED_ACREAGE_UNIT','PERCENT_TOTAL_DISTURBED','IMPERVIOUSNESS_BEFORE','IMPERVIOUSNESS_AFTER','MILE_POST_MARKER','CONSTRUCTION_COMMENCEMENT_DATE','COMPLETE_GRADING_DATE','COMPLETE_PROJECT_DATE','TYPE_OF_CONSTRUCTION','Year_construction_complete','year column','terminated?'])
            writer_dupl = csv.writer(dupl)
            writer_dupl.writerow(['Column1','APP_ID','WDID','STATUS','NOI_PROCESSED_DATE','NOT_EFFECTIVE_DATE','REGION','COUNTY','SITE_NAME','SITE_ADDRESS','SITE_ADDRESS_2','SITE_CITY','SITE_STATE','SITE_ZIP','SITE_LATITUDE','SITE_LONGITUDE','SITE_COUNTY','SITE_TOTAL_SIZE','SITE_TOTAL_SIZE_UNIT','SITE_TOTAL_DISTURBED_ACREAGE','TOTAL_DISTURBED_ACREAGE_UNIT','PERCENT_TOTAL_DISTURBED','IMPERVIOUSNESS_BEFORE','IMPERVIOUSNESS_AFTER','MILE_POST_MARKER','CONSTRUCTION_COMMENCEMENT_DATE','COMPLETE_GRADING_DATE','COMPLETE_PROJECT_DATE','TYPE_OF_CONSTRUCTION','Year_construction_complete','year column','terminated?'])
            for line in csv_inf:
                as_tuple = tuple(line)
                if as_tuple not in unique_rows:
                    writer_uniques.writerow(line)
                    unique_rows.add(as_tuple)
                else:
                    writer_dupl.writerow(line)

            print(len(unique_rows))
#test2

        #    if not app_id in uniques[1]:
        #        writer.writerow(line)
        #    else:
        #        pass
            #unique_rows = csv_pd.APP_ID.unique()
            #if unique_rows == TRUE:
            #    writer.writerow(unique_rows)
