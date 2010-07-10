from django.core.management.base import NoArgsCommand
from records.models import Record, Activity
from rah.models import Profile

class Command(NoArgsCommand):
    help = "Updates rows in the records table to reflect the current action points."

    def handle_noargs(self, **options):
        """
        After running this, you might want to run these SQL commands to recalculate the total_points in the profile.
        UPDATE `rah_profile` SET total_points = 0;
        REPLACE INTO rah_profile(`user_id`, `total_points`) SELECT `user_id`, SUM(`points`) FROM records_record WHERE void = 0 GROUP BY `user_id`;
        """
        activity = Activity.objects.get(slug="action_complete")
        records = Record.objects.filter(activity=activity, void=False)
        update_count = 0
        for record in records:
            content_object = record.content_objects.all()
            if len(content_object) <> 1:
                continue
            
            action = content_object[0].content_object
            
            if record.points <> action.points:                
                record.points = action.points
                record.save()
                update_count += 1
            
            if update_count > 0 and update_count % 10 == 0:
                print "%s..." % update_count 
        
        print "Updated %s record(s)" % update_count