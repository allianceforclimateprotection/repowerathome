import csv
import os
import time

from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User

from actions.models import Action
from events.models import Event, Guest, Survey, Commitment
from geo.models import Location


class Command(NoArgsCommand):
    help = "Designed for a one time import of van data into repowerathome.com events, guests, and commitments."

    def handle_noargs(self, **options):
        input_files = [
            os.path.join(os.path.dirname(__file__), "import_van_data_input_files/commitments1.txt"),
            os.path.join(os.path.dirname(__file__), "import_van_data_input_files/commitments2.txt"),
            os.path.join(os.path.dirname(__file__), "import_van_data_input_files/commitments3.txt"),
            os.path.join(os.path.dirname(__file__), "import_van_data_input_files/commitments4.txt"),
            os.path.join(os.path.dirname(__file__), "import_van_data_input_files/events.txt"),
            os.path.join(os.path.dirname(__file__), "import_van_data_input_files/emails.txt")
        ]
        VanImporter(input_files=input_files)

class VanImporter(object):
    """Imports data exported from VAN. input_files should be a list of file names"""

    def __init__(self, input_files=[]):
        if not input_files:
            exit("No input files provided")
        self.people = {}
        self.events = {}
        self.input_files = input_files
        self.action_map = {'replace_hvac_filter':'change-air-conditioning-heater-filters',
                           'replace_old_fridge':'replace-your-outdated-refrigerator',
                           'retire_refrigerat':'retire-second-refrigerator',
                           'seal_vents':'seal-vents-unoccupied-rooms',
                           'use_fan_in_summer':'use-ceiling-fan-summer',
                           'water_heater_120deg':'adjust-water-heater-temperature',
                           'insulate_windows':'insulate-your-windows',
                           'insulate_wtr_pipes':'insulate-water-pipes',
                           'lowflow_shower':'install-low-flow-shower-head',
                           'manual_thermostat':'save-with-manual-thermostat',
                           'program_thermostat':'programmable-thermostat',
                           'replace_bulb_cfl':'replace-your-incandescent-light-bulbs-with-cfls',
                           'energy_audit':'have-home-energy-audit',
                           'fan_in_winter':'use-ceiling-fan-winter',
                           'inst_chm_guard':'install-chimney-draft-guard',
                           'inst_sink_aerator':'install-low-flow-sink-aerator',
                           'insulate_water_htr':'insulate-water-heater',
                           'caulk_windows':'caulk-around-your-windows',
                           'close_firedamper':'keep-fireplace-damper-closed',
                           'cold_wash_cycle':'wash-clothes-cold-water',
                           'computer_to_sleep':'set-your-computer-sleep-automatically',
                           'dial_dwn_thermostat':'dial-down-thermostat',
                           'elim_always_on_light':'sensors-timers-for-lights'}
        self.answer_map = {'Completed': 'D', 'Already': 'D', 'Committed': 'C'}
        self.main()

    def main(self):
        print "Parsing input files..."
        # Loop through each commitment input file
        for f in self.input_files:
            reader = csv.DictReader(open(f, 'rU'), dialect='excel-tab')
            for row in reader:
                cid = row['My Campaign ID']
                try:
                    self.people[cid].update(row)
                except KeyError, e:
                    self.people[cid] = row
        """
        # How many cid's don't have events
        print "My Campaign ID, FirstName, LastName, Email"
        for k, v in self.people.iteritems():
            if 'House Party Code' not in v.keys():
                print "%s, %s, %s, %s" % (v['My Campaign ID'], v['FirstName'], v['LastName'], v['LastName'])

        # How many peeps don't have commitments
        print "My Campaign ID,House Party Code,House Party Date,Host"
        for k, v in self.people.iteritems():
            if 'LastName' not in v.keys():
                # print v
                print "%s, %s, %s, %s" % (v['My Campaign ID'], v['House Party Code'], v['House Party Date'], v['Host'])
        """

        # Prune a few incomplete records
        print "Pruning %s records..." % len(self.people.keys()),
        prune_keys = []
        for k, v in self.people.iteritems():
            if len(v.keys()) <> 40:
                prune_keys.append(k)
        for k in prune_keys:
            del self.people[k]
        print "%s record(s) pruned" % len(prune_keys)

        # Loop through the people and make a set of events
        for k, v in self.people.iteritems():
            self.events[v['House Party Code']] = {'House Party Date': v['House Party Date'], 'event_location': v['event_location'] }

        # Create the events in the Database
        print "Creating events...",
        event_counter = 0
        brenna = User.objects.get(pk=8)
        for k, v in self.events.iteritems():
            self.events[k] = Event.objects.create(
                creator=brenna,
                when=time.strftime("%Y-%m-%d", time.strptime(v['House Party Date'], "%m/%d/%y")),
                start="20:00:00",
                duration=90,
                details="Pilot energy meeting",
                location=Location.objects.get(zipcode=v['event_location'])
            )
            event_counter += 1
        print "%s event records created!" % event_counter

        # Create Guest records
        print "Creating guest records...",
        guest_counter = 0
        for k, v in self.people.iteritems():
            # Try to get the location from the guest zip
            try:
                location = Location.objects.get(zipcode=v['mZip5'])
            except:
                location = None

            # If that didn't work, use the zip from their event.
            if location == None:
                try:
                    location = Location.objects.get(zipcode=v['event_location'])
                except:
                    location = None

            try:
                self.people[k]['guest_obj'] = Guest.objects.create(
                    event = self.events[v['House Party Code']],
                    first_name = v['FirstName'],
                    last_name = v['LastName'],
                    email = v['Email'] if v['Email'] else "",
                    location = location,
                    rsvp_status = 'A',
                    notify_on_rsvp = 0,
                    is_host = 1 if v['Host'] else 0
                )
                guest_counter += 1
            except:
                print self.people[k]
        print "%s guest records created!" % guest_counter

        # Create an event survey
        print "Creating survey"
        survey = Survey.objects.get_or_create(
            name = "Pilot Commitment Card",
            form_name = "PilotEnergyMeetingCommitmentCard",
            template_name = "events/_pilot_commitment_card.html",
            is_active = True
        )[0]

        # Loop through people and create commitments for them
        print "Creating commitments...",
        commitment_counter = 0
        for k, v in self.people.iteritems():
            # go through actions and create commitment rows 
            for commitment_name, action_slug in self.action_map.iteritems():
                if commitment_name in v.keys() and v[commitment_name] <> '' and v[commitment_name] <> None and v[commitment_name] <> 'Decommitted':
                    Commitment.objects.create(
                        guest = v['guest_obj'],
                        survey = survey,
                        question = commitment_name,
                        answer = self.answer_map[v[commitment_name]],
                        action = Action.objects.get(slug=action_slug)
                    )
                    commitment_counter += 1

        print "%s commitment records created!" % commitment_counter


