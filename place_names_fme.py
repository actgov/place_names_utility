import fme
import fmeobjects

"""
This script is called on from within FME using the Python Caller function
https://www.safe.com/transformers/python-caller/

The purpose of this script is to concatenate multiple people fields into a single description field. 
html formatting i added to improve display when a feature is returned using the place names geocortex site. 
http://app.actmapi.act.gov.au/actmapi/index.html?viewer=pn

"""

# Template Function interface:
# When using this function, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
def processFeature(feature):
    
    commemorated_location = str(feature.getAttribute('C_LOC_NAME'))
    category              = str(feature.getAttribute('CATEGORY_NAME'))
    title                 = str(feature.getAttribute('TITLE'))         # has nulls
    given_names           = str(feature.getAttribute('GIVEN_NAMES'))
    surname               = str(feature.getAttribute('PEOPLE_NAMES'))
    alias                 = str(feature.getAttribute('OTHER_NAME'))    # has <missing>
    qualification         = str(feature.getAttribute('QUALIFICATION')) # has nulls
    gender                = str(feature.getAttribute('GENDER'))        # has nulls
    birth_year            = str(feature.getAttribute('BIRTH_YEAR'))    # has nulls
    death_year            = str(feature.getAttribute('DEATH_YEAR'))    # has nulls
    biography             = feature.getAttribute('BIOGRAPHY')          # has nulls
    
    # strip 'SIR ' '(SIR) ' from other names.
    alias = alias.replace('SIR ','').replace('(SIR) ','')
    
    # ignore switches for description compilation
    ignore_alias = False
    ignore_title = False
    ignore_qualification = False
    ignore_gender = False
    has_birth_year = True
    has_death_year = True
    ignore_biography = False
    
    # ignore null values
    # do not display OTHER_NAME (ALIAS) is OTHER_NAME == PEOPLE_NAMES
    if (alias == ''): ignore_alias = True
    if (title == ''): ignore_title = True
    if (qualification == ''): ignore_qualification = True
    if (gender == 'None'): ignore_gender = True
    if (birth_year == 'None'): has_birth_year = False
    if (death_year == 'None'): has_death_year = False
    if (biography == 'None'): ignore_biography = True
    
    # Build description for popup in geocortex
    description = ''
    description += 'Feature Name: ' + commemorated_location + '<br>'
    description += 'Commemorated Name: ' + surname + '<br>'
    description += 'Given Names: ' + given_names + '<br>'
    if (ignore_title == False): description += 'Title: ' + title + '<br>'
    if (ignore_qualification == False): description += 'Qualification: ' + qualification + '<br>'
    if (has_birth_year == True): description += 'Birth Year: ' + birth_year + '<br>'
    if (has_death_year == True): description += 'Death Year: ' + death_year + '<br>'
    # Clean gender for description
    if (ignore_gender == False):
        if (gender == 'M'):
            gender = 'Male'
        elif (gender == 'F'):
            gender = 'Female'
        description += 'Gender: ' + gender + '<br>'
    if (ignore_biography == False): description += 'Biography: ' + biography
    
    # Output to DESCRIPTION field for use in front end.
    feature.setAttribute('DESCRIPTION', description)
    
# Template Class Interface:
# When using this class, make sure its name is set as the value of
# the 'Class or Function to Process Features' transformer parameter
class FeatureProcessor(object):
    def __init__(self):
        pass
    def input(self,feature):
        processFeature(feature)
        self.pyoutput(feature)
    def close(self):
        pass
