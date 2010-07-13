import csv

from ...www import local_settings

class VanImporter(object):
    """Imports data exported from VAN"""
    
    def __init__(self, input_file):
        self.input_file = input_file
        self.main()
        
    def main(self):
        reader = csv.DictReader(open(self.input_file))
        for row in reader:
            print row

if __name__ == "__main__":
    VanImporter(input_file="2.csv")