from app import db, ma

# ---------------------------------------------------------
# 1. User Model
# ---------------------------------------------------------
class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}

    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    
    trails = db.relationship('Trail', backref='owner', lazy=True)

# ---------------------------------------------------------
# 2. Trail Model
# ---------------------------------------------------------
class Trail(db.Model):
    __tablename__ = 'Trails'
    __table_args__ = {'schema': 'CW2'}

    TrailId = db.Column(db.Integer, primary_key=True)
    OwnerId = db.Column(db.Integer, db.ForeignKey('CW2.Users.userID'), nullable=False)
    TrailName = db.Column(db.String(200), nullable=False)
    Length = db.Column(db.Numeric(10, 2), nullable=False) 
    ElevationGain = db.Column(db.Numeric(10, 2), nullable=False)
    EstimatedTime = db.Column(db.Numeric(5, 2), nullable=True)
    RouteType = db.Column(db.String(50), nullable=False)
    Difficulty = db.Column(db.String(50), nullable=False)
    trailDescription = db.Column(db.String(200), nullable=True)

    # Relationship to LocationPoint
    locations = db.relationship('LocationPoint', backref='trail', lazy=True, cascade="all, delete-orphan")

# ---------------------------------------------------------
# 3. LocationPoint Model
# ---------------------------------------------------------
class LocationPoint(db.Model):
    __tablename__ = 'LocationPoints'
    __table_args__ = {'schema': 'CW2'}

    PointId = db.Column(db.Integer, primary_key=True)
    TrailId = db.Column(db.Integer, db.ForeignKey('CW2.Trails.TrailId'), nullable=False)
    Latitude = db.Column(db.Numeric(9, 6), nullable=False)
    Longitude = db.Column(db.Numeric(9, 6), nullable=False)
    PointOrder = db.Column(db.Integer, nullable=False)

# ---------------------------------------------------------
# Serialization Schemas (The Missing Piece)
# ---------------------------------------------------------

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session
        include_fk = True # Include Foreign Keys like TrailId in the JSON

class TrailSchema(ma.SQLAlchemyAutoSchema):
    locations = ma.Nested(LocationSchema, many=True) # Nests points inside the trail
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session
        include_fk = True # Include OwnerId in the JSON

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

# Instances for use in routes
user_schema = UserSchema()
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)