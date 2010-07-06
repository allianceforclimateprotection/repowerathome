#!/usr/bin/python
import unittest
import logging
import random

from suds.client import Client
from suds.client import WebFault

class VanDemo(unittest.TestCase):
    
    def setUp(self):
        # Set up some logging
        logging.basicConfig(level=logging.INFO)
        logging.getLogger('suds.client').setLevel(logging.DEBUG)
        
        # Set up the client
        self.client = Client("https://secure.securevan.com/Services/V3/PersonService.asmx?WSDL")
        header = self.client.factory.create("Header")
        header.APIKey = "417B32A3-E59B-429F-BD6A-3E5D6246B945"
        header.DatabaseMode = "MyVoterFile"
        self.client.set_options(soapheaders=header)
        
        # Some variables for tests
        self.known_vanid = 325143
        self.activist_code_gun_control = 4133156
    
    def test_match_person(self):
        candidate = self.client.factory.create("Person")
        candidate.VANID = self.known_vanid
        match = self.client.service.MatchPerson(candidate, "MatchOnly")
        self.assertEqual(match.MatchResultStatus, "Matched")
    
    def test_create_person_with_email(self):
        random_email = "test.person.%s@example.org" % random.randint(1000,1000000000)
        candidate = self.client.factory.create("Person")
        candidate.Email = random_email
        match = self.client.service.MatchPerson(candidate, "MatchAndStore")
        self.assertEqual(match.MatchResultStatus, "UnmatchedStored")
    
    def test_apply_activist_code(self):
        # Get a record and check for any existing codes
        opts = self.client.factory.create("GetMethodOptions")
        opts.ReturnSections = "ActivistCode"
        person = self.client.service.GetPerson(self.known_vanid, "VANID", opts)
        if person.ActivistCodes:
            logging.info('There were already activist codes applied.')
        
        # Apply the code and refetch the person
        self.client.service.ApplyActivistCode(self.known_vanid, "VANID", self.activist_code_gun_control)
        person = self.client.service.GetPerson(self.known_vanid, "VANID", opts)
        
        # Assert that the code is applied (not necessary that it was applied)
        applied_codes = []
        if person.ActivistCodes:
            applied_codes = [[code.ActivistCodeID for code in codes] for type, codes in person.ActivistCodes][0]
        success = self.activist_code_gun_control in applied_codes
        self.assertTrue(success)
        
    def test_clear_activist_codes(self):
        self.client.service.ApplyActivistCode(self.known_vanid, "VANID", self.activist_code_gun_control)
        person = self.client.service.GetPerson(self.known_vanid, "VANID")
        person.ActivistCodes = self.client.factory.create("ArrayOfActivistCode")
        
        # Push the updated Person changes to the VAN
        match = self.client.service.MatchPerson(person, "MatchAndStore")
        self.assertEqual(match.MatchResultStatus, "Matched")
        
        # Fetch the person again to verify the activist codes are cleared
        opts = self.client.factory.create("GetMethodOptions")
        opts.ReturnSections = "ActivistCode"
        person = self.client.service.GetPerson(self.known_vanid, "VANID", opts)
        self.assertEqual(len(person.ActivistCodes), 0)
    

if __name__ == '__main__':
    unittest.main()



"""
Service Def for reference
-------------------------

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