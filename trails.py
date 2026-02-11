from flask import request, abort, current_app
from extensions import db
from models import Trail, LocationPoint, User, trail_schema, trails_schema
from auth import verify_credentials

def read_all():
    """Responds to a request for /api/trails with the complete list of trails"""
    trails = Trail.query.all()
    return trails_schema.dump(trails)

def create(body):
    """Creates a new trail in the database."""
    email = request.headers.get('X-Email')
    password = request.headers.get('X-Password')

    if not email or not password:
        abort(401, "Authentication credentials missing")

    if not verify_credentials(email, password):
        abort(401, "Invalid credentials or authentication failed")

    with current_app.app_context():
        user = User.query.filter_by(email=email).one_or_none()
        if user is None:
            abort(404, f"User {email} not found in local database")

        # Extract locations before creating the Trail object
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

        for point in locations_data:
            new_point = LocationPoint(
                Latitude=point.get('Latitude'),
                Longitude=point.get('Longitude'),
                PointOrder=point.get('PointOrder')
            )
            new_trail.locations.append(new_point)

        db.session.add(new_trail)
        db.session.commit()
        result = trail_schema.dump(new_trail)

    return result, 201

def delete(TrailId):
    """Deletes a specific trail."""
    email = request.headers.get('X-Email')
    password = request.headers.get('X-Password')

    if not email or not password:
        abort(401, "Authentication credentials missing")

    if not verify_credentials(email, password):
        abort(401, "Invalid credentials")

    with current_app.app_context():
        trail = Trail.query.filter_by(TrailId=TrailId).one_or_none()
        if trail is None:
            abort(404, f"Trail {TrailId} not found")

        user = User.query.filter_by(email=email).one_or_none()
        
        # Ownership check is required by assignment brief
        if not user or trail.OwnerId != user.userID:
            abort(403, "Forbidden: You are not the owner of this trail")

        db.session.delete(trail)
        db.session.commit()

    return "", 204

# FIX: Moved this back to the left margin so it is a standalone function
def update(TrailId, body):
    """Updates an existing trail's information."""
    email = request.headers.get('X-Email')
    password = request.headers.get('X-Password')

    if not email or not password:
        abort(401, "Authentication credentials missing")

    if not verify_credentials(email, password):
        abort(401, "Invalid credentials")

    with current_app.app_context():
        trail = Trail.query.filter_by(TrailId=TrailId).one_or_none()
        if trail is None:
            abort(404, f"Trail {TrailId} not found")

        user = User.query.filter_by(email=email).one_or_none()
        
        # Verify ownership before allowing modifications
        if not user or trail.OwnerId != user.userID:
            abort(403, "Forbidden: You are not the owner of this trail")

        # Safely remove locations from body if present to avoid model mismatch
        body.pop('locations', None)

        # Update core fields
        trail.TrailName = body.get('TrailName', trail.TrailName)
        trail.Length = body.get('Length', trail.Length)
        trail.ElevationGain = body.get('ElevationGain', trail.ElevationGain)
        trail.EstimatedTime = body.get('EstimatedTime', trail.EstimatedTime)
        trail.RouteType = body.get('RouteType', trail.RouteType)
        trail.Difficulty = body.get('Difficulty', trail.Difficulty)
        trail.trailDescription = body.get('trailDescription', trail.trailDescription)

        db.session.commit()
        return trail_schema.dump(trail), 200