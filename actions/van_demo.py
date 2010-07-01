from suds.client import Client
from suds.client import WebFault
import logging

# Set up some logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

# Set up the client
client = Client("https://secure.securevan.com/Services/V3/PersonService.asmx?WSDL")
header = client.factory.create("Header")
header.APIKey = "417B32A3-E59B-429F-BD6A-3E5D6246B945"
header.DatabaseMode = "MyVoterFile"
client.set_options(soapheaders=header)

msg = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <Header xmlns="https://api.securevan.com/Services/V3/">
      <APIKey>417B32A3-E59B-429F-BD6A-3E5D6246B945</APIKey>
      <DatabaseMode>MyVoterFile</DatabaseMode>
    </Header>
  </soap:Header>
  <soap:Body>
    <ApplyActivistCode xmlns="https://api.securevan.com/Services/V3/">
      <PersonID>325143</PersonID>
      <PersonIDType>VANID</PersonIDType>
      <ActivistCodeID>4134268</ActivistCodeID>
    </ApplyActivistCode>
  </soap:Body>
</soap:Envelope>
"""

try:
    # result = client.service.HelloAuthWorld("hello world...")
    
    # Get the participant 
    candidate = client.factory.create("Person")
    candidate.Email = "jimmysmith@gmail.com"
    match = client.service.MatchPerson(candidate, "MatchOnly")
    print match
    
    # Apply a code (Gun owner: 4133156)
    result = client.service.ApplyActivistCode(match.PersonID, match.PersonIDType, "4133156")
    print result
    
    # print client.service.ApplyActivistCode(__inject={'msg':msg})
    sections = client.factory.create("GetMethodOptions")
    sections.ReturnSections = "SurveyQuestionResponse"
    print client.service.GetPerson(match.PersonID, match.PersonIDType, sections)
    
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