from enum import Enum


class PublicRegionCode(str, Enum):
    ASIA_NORTHEAST_1 = "asia-northeast-1"
    ASIA_NORTHEAST_2 = "asia-northeast-2"
    ASIA_SOUTH_1 = "asia-south-1"
    AUSTRALIA_EAST_1 = "australia-east-1"
    EUROPE_CENTRAL_1 = "europe-central-1"
    ME_WEST_1 = "me-west-1"
    US_EAST_1 = "us-east-1"
    US_EAST_2 = "us-east-2"
    US_EAST_3 = "us-east-3"
    US_MIDWEST_1 = "us-midwest-1"
    US_MIDWEST_2 = "us-midwest-2"
    US_SOUTH_1 = "us-south-1"
    US_SOUTH_2 = "us-south-2"
    US_SOUTH_3 = "us-south-3"
    US_WEST_1 = "us-west-1"
    US_WEST_2 = "us-west-2"
    US_WEST_3 = "us-west-3"

    def __str__(self) -> str:
        return str(self.value)
