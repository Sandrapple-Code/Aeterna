from pydantic import BaseModel
from typing import List

class CareerMatch(BaseModel):
    title: str
    fit_reason: str
    industry_demand: str
    learning_curve: str

class CareerDiscoveryOutput(BaseModel):
    detailed_analysis: str
    recommended_career: str
    top_matches: List[CareerMatch]

class ResumeInsights(BaseModel):
    detailed_analysis: str
    match_score: float
    skill_gaps_identified: List[str]
    optimized_bullets_suggested: List[str]

class StructuredProfile(BaseModel):
    skills: List[str]
    education: List[str]
    experience: List[str]
    projects: List[str]

class RoadmapPhase(BaseModel):
    phase_number: int
    title: str
    duration: str
    objectives: List[str]

class CareerRoadmap(BaseModel):
    detailed_analysis: str
    estimated_timeline: str
    phases: List[RoadmapPhase]
    career_readiness_score: float

class OpportunityList(BaseModel):
    detailed_analysis: str
    internships: List[str]
    jobs: List[str]
    hackathons: List[str]
    fellowships: List[str]
    recommended_companies: List[str]
