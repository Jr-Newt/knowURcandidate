from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class District(BaseModel):
    id: int
    name: str


class Constituency(BaseModel):
    id: int
    name: str
    district_id: int


class Candidate(BaseModel):
    id: int
    name: str
    constituency_id: int
    party: Optional[str] = None
    education: Optional[str] = None
    criminal_cases: int = 0
    serious_cases: int = 0
    assets: int = 0
    liabilities: int = 0
    profession: Optional[str] = None
    age: Optional[int] = None
    affidavit_link: Optional[str] = None
    education_score: float = 0.0
    criminal_score: float = 1.0
    asset_score: float = 0.0
    experience_score: float = 0.0
    # Joined fields (optional, populated in some queries)
    constituency_name: Optional[str] = None
    district_name: Optional[str] = None


class CandidateNews(BaseModel):
    id: int
    candidate_id: int
    title: str
    source: Optional[str] = None
    published_date: Optional[date] = None
    url: str
    summary: Optional[str] = None


class RankWeights(BaseModel):
    education: float = Field(default=0.25, ge=0.0, le=1.0)
    criminal: float = Field(default=0.25, ge=0.0, le=1.0)
    experience: float = Field(default=0.25, ge=0.0, le=1.0)
    assets: float = Field(default=0.25, ge=0.0, le=1.0)


class RankRequest(BaseModel):
    weights: RankWeights
    district: Optional[str] = None
    constituency: Optional[str] = None


class ScoreBreakdown(BaseModel):
    education: float
    criminal: float
    experience: float
    assets: float


class RankedCandidate(BaseModel):
    id: int
    name: str
    party: Optional[str] = None
    constituency_name: Optional[str] = None
    district_name: Optional[str] = None
    total_score: float
    breakdown: ScoreBreakdown
    education: Optional[str] = None
    criminal_cases: int = 0
    serious_cases: int = 0
    assets: int = 0
    liabilities: int = 0
    profession: Optional[str] = None
    age: Optional[int] = None
