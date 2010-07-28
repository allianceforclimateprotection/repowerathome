import csv
from events.models import Event

# from ..www import local_settings
# Note: Brenna's VAN ID is 100221441

class VanImporter(object):
    """Imports data exported from VAN. input_files should be a list of file names"""
    
    def __init__(self, input_files=[], event_files=[]):
        if not input_files:
            exit("No input files provided")
        self.people = {}
        self.events = {}
        self.input_files = input_files
        self.event_files = event_files
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
        
        self.main()
            
    def main(self):
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
        print "Pruning %s records..." % len(self.people.keys())
        prune_keys = []
        for k, v in self.people.iteritems():
            if len(v.keys()) <> 40:
                prune_keys.append(k)
        for k in prune_keys:
            del self.people[k]
        print "pruned %s record(s)" % len(prune_keys)
        
        # Loop through the people and make a set of events
        for k, v in self.people.iteritems():
            self.events[v['House Party Code']] = v['House Party Date']
        
        print "There are %s event(s)" % len(self.events.keys())
        
if __name__ == "__main__":
    input_files = [
        "commitments1.txt", 
        "commitments2.txt", 
        "commitments3.txt", 
        "commitments4.txt", 
        "events.txt", 
        "emails.txt"
    ]
    VanImporter(input_files=input_files, event_files=['events.txt'])