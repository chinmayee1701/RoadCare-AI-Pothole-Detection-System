"""
MongoDB database connection and management
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from app.config import settings


class Database:
    """MongoDB database manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None
    
    async def connect_db(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            self.database = self.client[settings.MONGODB_DB_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")
            
            # Create indexes for better performance
            await self.create_indexes()
            
        except Exception as e:
            print(f"❌ Error connecting to MongoDB: {e}")
            raise
    
    async def close_db(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")
    
    async def create_indexes(self):
        """Create database indexes for better query performance"""
        try:
            # Users collection indexes
            await self.database.users.create_index("email", unique=True)
            
            # Pothole reports collection indexes
            await self.database.pothole_reports.create_index("status")
            await self.database.pothole_reports.create_index("user_id")
            await self.database.pothole_reports.create_index([("location.latitude", 1), ("location.longitude", 1)])
            
            # Image verification collection indexes
            await self.database.image_verification.create_index("report_id", unique=True)
            
            # Risk zones collection indexes
            await self.database.risk_zones.create_index([("center_location.latitude", 1), ("center_location.longitude", 1)])
            
            # Repair actions collection indexes
            await self.database.repair_actions.create_index("zone_id")
            await self.database.repair_actions.create_index("repair_status")
            
            print("✅ Database indexes created")
            
        except Exception as e:
            print(f"⚠️  Error creating indexes: {e}")


# Global database instance
db = Database()


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance for dependency injection"""
    return db.database
