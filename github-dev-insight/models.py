from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class UserProfile:
    username: str
    name: str
    bio: str
    public_repos: int
    followers: int
    following: int
    avatar_url: str

@dataclass
class RepoAnalytics:
    total_stars: int
    total_forks: int
    most_starred: str
    languages: Dict[str, int]