# Import base schemas first to avoid circular imports
from app.schemas.region import RegionBase, RegionCreate, RegionUpdate, RegionResponse
from app.schemas.court import CourtBase, CourtCreate, CourtUpdate, CourtResponse
from app.schemas.availability import (
    AvailabilityBase,
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityResponse,
    AvailabilityQuery,
)

# Then import schemas with relationships
from app.schemas.region import RegionWithCourts
from app.schemas.court import CourtWithRegion, CourtWithAvailability
from app.schemas.availability import AvailabilityWithCourt

# Rebuild models to resolve forward references
RegionWithCourts.model_rebuild()
CourtWithRegion.model_rebuild()
CourtWithAvailability.model_rebuild()
AvailabilityWithCourt.model_rebuild()

__all__ = [
    # Region
    "RegionBase",
    "RegionCreate",
    "RegionUpdate",
    "RegionResponse",
    "RegionWithCourts",
    # Court
    "CourtBase",
    "CourtCreate",
    "CourtUpdate",
    "CourtResponse",
    "CourtWithRegion",
    "CourtWithAvailability",
    # Availability
    "AvailabilityBase",
    "AvailabilityCreate",
    "AvailabilityUpdate",
    "AvailabilityResponse",
    "AvailabilityWithCourt",
    "AvailabilityQuery",
]
