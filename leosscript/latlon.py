#BOTH OGR AND OSGEO.OGR DO THE SAME THING. USE WHAT YOUR PREFERENCE IS
#import osgeo.ogr
#from modulefinder import ModuleFinder
import ogr
# USER-CONFIGURABLES

#IN_FILE = "./test.csv"

__author__ = "Walter Mobley"
__date__ = '2017-05-05'
__email__ = "Walter.Mobley@water.ca.gov"
__license__ = "GPLv3"
__maintainer__ = "Atmospheric Modeling and Support Section at CARB"
__status__ = "Production"
__version__ = "1.1.0"

# CONSTANTS USED TO DEFINE COUNTIES' LAT/LON 
GAI_SHP = "./input/coabdis_gai_oc1_oc2_latlon_20140924/coabdis_gai_oc1_oc2_latlon_20140924.shp"
#FIELD_NAME = "GAI" #"CO_NAME"

# AUTO-MAGIC ABBREVIATIONS USED LATER IN THE SCRIPT TO PULL FROM ESRI SHAPEFILE
#drv = osgeo.ogr.GetDriverByName('ESRI Shapefile')
drv = ogr.GetDriverByName('ESRI Shapefile')
ds_in = drv.Open(GAI_SHP)
lyr_in = ds_in.GetLayer(0)
#idx_reg = lyr_in.GetLayerDefn().GetFieldIndex(FIELD_NAME)

 
#def main():
#    print(check(-117.3755, 33.9806,'GAI'))

def usage():
    print('\nThis program provides CoABDis information for a given-\n')
    print('latitude and longitude pair.\n\n')
    print('Mandatory Flags:\n')
    print('-i  = path to input file\n')
    print('-o  = path to output file\n')
    print('-v = version of SMOKE\n\n')


def check(lon, lat,FIELD_NAME='GAI'):
    # FINDS OUT WHICH COUNTY THE LAT/LON POINT IS IN 
    '''Uses:
      
       FIELD_NAME can be: 'CO'     : for county code
                          'AB'     : for air basin
                          'DIS'    : for district
                          'COABDIS': for coabdis (e.g. 30_SC_SC)
                          'GAI'    : for GAI (e.g. 06060, where the first two digits are always 06 for California)
                          'CO_NAME': for county name
       Example Possible output:
       CO=30, AB=SC, DIS=SC,COABDIS=30_SC_SC, GAI=06060, CO_NAME=Orange
    '''
    idx_reg = lyr_in.GetLayerDefn().GetFieldIndex(FIELD_NAME)
    point = ogr.Geometry(ogr.wkbPoint)
    point.SetPoint_2D(0, lon, lat)
    lyr_in.SetSpatialFilter(point)
    for feat_in in lyr_in:
        ply = feat_in.GetGeometryRef()
        if ply.Contains(point):
            return feat_in.GetFieldAsString(idx_reg)
    # IF LAT/LON POINT IS NOT IN ANY OF THE COUNTIES PRINT "NOT FOUND' 
    return "NOT FOUND"

if __name__ == '__main__':
    main()

