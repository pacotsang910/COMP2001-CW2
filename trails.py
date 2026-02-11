from flask import request, abort, current_app
from extensions import db
from models import Trail, LocationPoint, User, trail_schema, trails_schema
from auth import verify_credentials

def read_all():
    """
    Responds to a request for /api/trails
    with the complete list of trails
    """
    trails = Trail.query.all()
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

def delete(TrailId):
    """
    Deletes a specific trail.
    Requires X-Email and X-Password for owner verification.
    """
    email = request.headers.get('X-Email')
    password = request.headers.get('X-Password')

    if not email or not password:
        abort(401, "Authentication credentials missing")

    # 1. Verify credentials with University API
    if not verify_credentials(email, password):
        abort(401, "Invalid credentials")

    with current_app.app_context():
        # 2. Find the trail in the database
        trail = Trail.query.filter_by(TrailId=TrailId).one_or_none()
        if trail is None:
            abort(404, f"Trail {TrailId} not found")

        # 3. Find the user trying to delete it
        user = User.query.filter_by(email=email).one_or_none()
        
        # 4. Check Ownership: Only the owner can delete
        if not user or trail.OwnerId != user.userID:
            abort(403, "Forbidden: You are not the owner of this trail")

        # 5. Delete and Commit
        db.session.delete(trail)
        db.session.commit()

    return "", 204