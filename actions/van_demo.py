from suds.sax.element import Element
from suds.client import Client
from suds.client import WebFault
import logging

# Set up some logging
logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)

# Set up the client
client = Client("https://secure.securevan.com/Services/V3/PersonService.asmx?WSDL")
header = client.factory.create("Header")
header.APIKey = "417B32A3-E59B-429F-BD6A-3E5D6246B945X"
header.DatabaseMode = "MyVoterFile"
client.set_options(soapheaders=header)

try:
    result = client.service.HelloAuthWorld("hello world...")
    print result
except WebFault, e:
    print e

# Service Def for reference
"""
Methods (6):
   ApplyActivistCode(xs:string PersonID, xs:string PersonIDType, xs:string ActivistCodeID, )
   GetPerson(xs:string PersonID, xs:string PersonIDType, GetMethodOptions options, )
   HelloAuthWorld(xs:string msg, )
   HelloWorld(xs:string msg, )
   ListPeople(ListPeopleCriteria criteria, ListMethodOptions options, )
   MatchPerson(Person candidate, xs:string instruction, xs:string options, )
Types (65):
   ActivistCode
   Address
   ArrayOfActivistCode
   ArrayOfAddress
   ArrayOfCanvassResult
   ArrayOfChoice1
   ArrayOfCommittee
   ArrayOfCustomField
   ArrayOfCustomFieldGroup
   ArrayOfDistrict
   ArrayOfElectionRecord
   ArrayOfEmail
   ArrayOfEventSignup
   ArrayOfNote
   ArrayOfOrganizationRole
   ArrayOfPerson
   ArrayOfPhone
   ArrayOfString
   ArrayOfString1
   ArrayOfSurveyQuestionResponse
   ArrayOfUser
   ArrayOfVolunteerActivity
   BaseCasework
   BasePagedList
   CanvassResult
   Case
   CaseSubject
   Committee
   CustomField
   CustomFieldGroup
   CustomFieldType
   CustomID
   CustomProperty
   DatabaseMode
   District
   ElectionRecord
   Email
   Event
   EventSignup
   FaultHeader
   GeoLevelC
   GetMethodOptions
   Header
   Issue
   IssueSubject
   IssueTopic
   ListMethodOptions
   ListPeopleCriteria
   ListPeoplePayload
   MatchPersonResult
   MatchResult
   Note
   Organization
   OrganizationRole
   Person
   PersonIDType
   Phone
   StagingLocation
   Status
   Story
   SurveyQuestion
   SurveyQuestionResponse
   User
   VolunteerActivity
   VolunteerStatus
"""