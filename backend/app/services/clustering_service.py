"""
Geographic clustering service for risk zone detection
"""
import math
from typing import List, Dict
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.report import LocationModel
from app.models.risk_zone import RiskZoneInDB


class ClusteringService:
    """
    Service for geographic clustering and risk zone calculation
    """
    
    # Clustering parameters (in kilometers)
    CLUSTER_RADIUS_KM = 0.5  # 500 meters
    
    # Risk level thresholds
    HIGH_RISK_THRESHOLD = 5  # 5+ potholes
    MEDIUM_RISK_THRESHOLD = 3  # 3-4 potholes
    
    def calculate_distance(self, loc1: LocationModel, loc2: LocationModel) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula
        
        Args:
            loc1: First location
            loc2: Second location
            
        Returns:
            float: Distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371.0
        
        # Convert to radians
        lat1 = math.radians(loc1.latitude)
        lon1 = math.radians(loc1.longitude)
        lat2 = math.radians(loc2.latitude)
        lon2 = math.radians(loc2.longitude)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def determine_risk_level(self, pothole_count: int) -> str:
        """Determine risk level based on pothole count"""
        if pothole_count >= self.HIGH_RISK_THRESHOLD:
            return "high"
        elif pothole_count >= self.MEDIUM_RISK_THRESHOLD:
            return "medium"
        else:
            return "low"
    
    def calculate_center(self, locations: List[LocationModel]) -> LocationModel:
        """Calculate geographic center of multiple locations"""
        if not locations:
            return LocationModel(latitude=0, longitude=0)
        
        avg_lat = sum(loc.latitude for loc in locations) / len(locations)
        avg_lon = sum(loc.longitude for loc in locations) / len(locations)
        
        return LocationModel(latitude=avg_lat, longitude=avg_lon)
    
    async def recalculate_risk_zones(self, db: AsyncIOMotorDatabase) -> List[Dict]:
        """
        Recalculate all risk zones based on verified pothole reports
        
        Args:
            db: Database instance
            
        Returns:
            List of created/updated risk zones
        """
        # Get all verified pothole reports
        reports_cursor = db.pothole_reports.find({"status": "verified"})
        reports = await reports_cursor.to_list(length=None)
        
        if not reports:
            return []
        
        # Clear existing risk zones
        await db.risk_zones.delete_many({})
        
        # Group reports into clusters
        clusters: List[List[Dict]] = []
        unassigned = reports.copy()
        
        while unassigned:
            # Start new cluster with first unassigned report
            current_report = unassigned.pop(0)
            cluster = [current_report]
            
            # Find all reports within cluster radius
            i = 0
            while i < len(unassigned):
                report = unassigned[i]
                
                # Check distance to any report in current cluster
                in_cluster = False
                for cluster_report in cluster:
                    loc1 = LocationModel(**cluster_report["location"])
                    loc2 = LocationModel(**report["location"])
                    
                    if self.calculate_distance(loc1, loc2) <= self.CLUSTER_RADIUS_KM:
                        in_cluster = True
                        break
                
                if in_cluster:
                    cluster.append(report)
                    unassigned.pop(i)
                else:
                    i += 1
            
            clusters.append(cluster)
        
        # Create risk zones for each cluster
        created_zones = []
        for cluster in clusters:
            # Calculate center location
            locations = [LocationModel(**r["location"]) for r in cluster]
            center = self.calculate_center(locations)
            
            # Determine risk level
            pothole_count = len(cluster)
            risk_level = self.determine_risk_level(pothole_count)
            
            # Create risk zone
            zone = RiskZoneInDB(
                center_location=center,
                pothole_count=pothole_count,
                risk_level=risk_level,
                report_ids=[r["_id"] for r in cluster],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Insert into database
            result = await db.risk_zones.insert_one(zone.dict(by_alias=True, exclude={"id"}))
            zone.id = result.inserted_id
            
            created_zones.append(zone.dict(by_alias=True))
        
        return created_zones


# Global clustering service instance
clustering_service = ClusteringService()
