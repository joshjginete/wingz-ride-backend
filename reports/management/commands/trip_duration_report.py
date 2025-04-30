from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Report of trips longer than 1 hour grouped by driver and month'

    def handle(self, *args, **kwargs):
        self.stdout.write("Running trip duration report...")

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    DATE_TRUNC('month', pickup.created_at) AS month,
                    rr.driver_id,
                    COUNT(*) AS trip_count
                FROM rides_rideevents pickup
                JOIN rides_rideevents dropoff ON pickup.ride_id = dropoff.ride_id
                JOIN rides_rides rr ON pickup.ride_id = rr.id
                WHERE pickup.description = 'Status changed to pickup'
                    AND dropoff.description = 'Status changed to dropoff'
                    AND dropoff.created_at > pickup.created_at
                    AND EXTRACT(EPOCH FROM (dropoff.created_at - pickup.created_at)) > 3600
                GROUP BY month, rr.driver_id
                ORDER BY month, rr.driver_id
            """)

            rows = cursor.fetchall()

        if not rows:
            self.stdout.write("No trips longer than 1 hour found.")
        else:
            for row in rows:
                month, driver_id, count = row
                self.stdout.write(f"{month.strftime('%Y-%m')} - Driver {driver_id}: {count} trips")
