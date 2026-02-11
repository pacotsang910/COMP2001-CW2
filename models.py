from app import db, ma

# ---------------------------------------------------------
# 1. User Model (Matches existing CW1 table)
# ---------------------------------------------------------
class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'} 

    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False) # The roles held in the app

    trails = db.relationship('Trail', backref='owner', lazy=True)

# ---------------------------------------------------------
# 2. Trail Model (The Parent Entity)
# ---------------------------------------------------------
class Trail(db.Model):
    __tablename__ = 'Trails'
    __table_args__ = {'schema': 'CW2'}

    trailID = db.Column(db.Integer, primary_key=True)
    trailName = db.Column(db.String(100), nullable=False)
    trailDescription = db.Column(db.String(200))
    ownerID = db.Column(db.Integer, db.ForeignKey('CW2.Users.userID'), nullable=False)

    # Relationship: One trail consists of many location points
    locations = db.relationship('LocationPoint', backref='trail', lazy=True, cascade="all, delete-orphan")

# ---------------------------------------------------------
# 3. LocationPoint Model (The Child Entity)
# ---------------------------------------------------------
class LocationPoint(db.Model):
    __tablename__ = 'LocationPoints'
    __table_args__ = {'schema': 'CW2'}

    pointID = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    orderNumber = db.Column(db.Integer, nullable=False) 
    trailID = db.Column(db.Integer, db.ForeignKey('CW2.Trails.trailID'), nullable=False)

# ---------------------------------------------------------
# Serialization Schemas 
# ---------------------------------------------------------

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True 
        sqla_session = db.session 

class TrailSchema(ma.SQLAlchemyAutoSchema):
    locations = ma.Nested(LocationSchema, many=True) 
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

# Instances for use in our routes 
user_schema = UserSchema()
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)