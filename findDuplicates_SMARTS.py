# Script goal: to isolate unique records in the SMARTS data and generate
# a csv that only contains one of each application.
# please note: this runs with WDID instead of APP_ID becuase there are 121
# records with no APP_ID.
import csv
import os, sys
#import smarts
import pdb

# path to file
in_file = 'smarts_011422_needgc.csv'

# naming outputs
out_count = in_file.replace('.csv', '_application_counts.csv')
out_duplcounts = in_file.replace('.csv', '_duplicate_counts.csv')
out_uniques = in_file.replace('.csv', '_unique_applications.csv')
out_duplicates = in_file.replace('.csv', '_duplicate_applications')


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
    print('total records in original csv = ' + str(sum(application_counts.values()))) #sanity check = 33200
    # delivering sums to terminal
    a = sum(1 for i in application_counts.values() if i>=2)
    print('duplicated IDs = ' + str(a))
    print('total number of IDs = ' + str(len(application_counts)))

# creating CSVs of the dictionaries built previously
# csv with WDIDs and how many times they occur in the data set
with open(out_count, 'w+') as counts:
    writer = csv.writer(counts)
    writer.writerow(['application_id', 'occurences'])
    for app_id, count in application_counts.items():
        writer.writerow([app_id, count])
# csv with WDIDs and how many times they are duplicated in the data set
with open(out_duplcounts, 'w+') as dupl:
    writer = csv.writer(dupl)
    writer.writerow(['application_id', 'occurences'])
    for app_id, count in application_counts.items():
        if count > 1:
            writer.writerow([app_id, count])

# csv containing all records removed from the original data
# application id duplicates - 1 that stays in the original to
# have only one of each project in the output
unique_rows = set()
with open(in_file) as infile:
    csv_inf = csv.reader(infile)
    next(csv_inf)

    with open(out_duplicates, 'w+') as dupl:

        with open(out_uniques, 'w+') as uniques:
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

            print('number of records in final output = ' + str(len(unique_rows)))
            print('NOTE: number of records in final output should be equal to unique IDs')

#county_check_latlon('unique_applications.csv')
