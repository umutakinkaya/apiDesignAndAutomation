from app.init import create_app, db
from app.models import Site, Building, Level

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Initialize the database"""
    with app.app_context():
        try:
            db.drop_all()  # Önce mevcut tabloları temizle
            db.create_all()  # Yeni tabloları oluştur
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")

@app.cli.command("seed-db")
def seed_db():
    """Seed the database with test data"""
    with app.app_context():
        try:
            # Önce tabloların var olduğundan emin ol
            db.create_all()
            
            # Test verisi oluştur
            site = Site(
                name="Test Hospital Campus",
                address="123 Medical Center Dr",
                city="Boston", 
                country="USA",
                description="Test hospital campus"
            )
            db.session.add(site)
            db.session.commit()
            
            building = Building(
                name="Main Hospital Building",
                code="MHB",
                address="123 Medical Center Dr, Building A",
                floors=10,
                site_id=site.id
            )
            db.session.add(building)
            db.session.commit()
            
            level = Level(
                name="Ground Floor",
                level_number=0,
                description="Main entrance and reception",
                map_data="base64_encoded_data_here",
                building_id=building.id
            )
            db.session.add(level)
            db.session.commit()
            
            print("✅ Test data seeded successfully!")
            print(f"   Site ID: {site.id}")
            print(f"   Building ID: {building.id}")
            print(f"   Level ID: {level.id}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding database: {e}")



# Manuel olarak çalıştırmak için fonksiyonlar
def init_database():
    """Initialize database manually"""
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            print("✅ Database tables created successfully!")
            return True
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            return False

def seed_database():
    """Seed database manually"""
    with app.app_context():
        try:
            # Check if tables exist, if not create them
            db.create_all()
            
            # Check if data already exists
            if Site.query.count() > 0:
                print("ℹ️  Database already has data, skipping seed.")
                return True
            
            print("🌱 Seeding database with test data...")
            
            # Create test data
            site = Site(
                name="Test Hospital Campus",
                address="123 Medical Center Dr",
                city="Boston", 
                country="USA",
                description="Test hospital campus"
            )
            db.session.add(site)
            db.session.commit()
            
            building = Building(
                name="Main Hospital Building",
                code="MHB",
                address="123 Medical Center Dr, Building A",
                floors=10,
                site_id=site.id
            )
            db.session.add(building)
            db.session.commit()
            
            level = Level(
                name="Ground Floor",
                level_number=0,
                description="Main entrance and reception",
                map_data="base64_encoded_data_here",
                building_id=building.id
            )
            db.session.add(level)
            db.session.commit()
            
            print("✅ Test data seeded successfully!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error seeding database: {e}")
            return False

if __name__ == '__main__':
    # Eğer command line argümanları varsa
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "init-db":
            init_database()
        elif sys.argv[1] == "seed-db":
            seed_database()
        elif sys.argv[1] == "run":
            # Sadece API'yi başlat
            with app.app_context():
                db.create_all()
            app.run(debug=True, host='0.0.0.0', port=5000)
        else:
            print("Usage: python run.py [init-db|seed-db|run]")
    else:
        # Varsayılan: hem init hem seed hem de çalıştır
        with app.app_context():
            db.create_all()
            if Site.query.count() == 0:
                print("🌱 Seeding initial data...")
                seed_database()
        
        print("🚀 Starting Pointr API...")
        app.run(debug=True, host='0.0.0.0', port=5000)