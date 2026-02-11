from flask import request, abort, current_app
from extensions import db
from models import Trail, LocationPoint, User, trail_schema
from auth import verify_credentials

def read_all():
    """
    Responds to a request for /api/trails
    with the complete list of trails
    """
    trails = Trail.query.all()
    # We use trails_schema from models, but we need to import it. 
    # If it's not in the import list above, add: from models import trails_schema
    from models import trails_schema 
    return trails_schema.dump(trails)

def create(body):
    """
    Creates a new trail in the database.
    Expects 'body' to be the JSON from the request.
    """
    # 1. Get credentials from headers
    email = request.headers.get('X-Email')
    password = request.headers.get('X-Password')

    if not email or not password:
        abort(401, "Authentication credentials missing")

    # 2. Verify credentials
    if not verify_credentials(email, password):
        abort(401, "Invalid credentials or authentication failed")

    # 3. Use the application context to safely query the database
    with current_app.app_context():
        # Find the user
        user = User.query.filter_by(email=email).one_or_none()
        if user is None:
            abort(404, f"User {email} not found in local database")

        # 4. Create the Trail object
        locations_data = body.pop('locations', [])
        
        new_trail = Trail(
            TrailName=body.get('TrailName'),
            Length=body.get('Length'),
            ElevationGain=body.get('ElevationGain'),
            EstimatedTime=body.get('EstimatedTime'),
            RouteType=body.get('RouteType'),
            Difficulty=body.get('Difficulty'),
            trailDescription=body.get('trailDescription'),
            OwnerId=user.userID
        )

        # 5. Add Location Points
        for point in locations_data:
            new_point = LocationPoint(
                Latitude=point.get('Latitude'),
                Longitude=point.get('Longitude'),
                PointOrder=point.get('PointOrder')
            )
            new_trail.locations.append(new_point)

        # 6. Save to Database
        db.session.add(new_trail)
        db.session.commit()

        # Serialize the result before leaving the context
        result = trail_schema.dump(new_trail)

    return result, 201