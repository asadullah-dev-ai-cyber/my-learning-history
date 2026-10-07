from datetime import datetime

def format_joined_date(created_at_str: str) -> str:
    """Formats ISO date string (e.g. 2025-09-12T...) to 'September 12, 2025'."""
    if not created_at_str:
        return "N/A"
    try:
        dt = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%B %d, %Y")
    except ValueError:
        return created_at_str

def calculate_developer_score(total_stars: int, total_forks: int, public_repos: int, language_count: int) -> dict:
    if public_repos == 0:
        return {"activity_score": 0, "quality_score": 0, "diversity_score": 0, "overall_tier": "Novice Explorer"}

    avg_stars = total_stars / public_repos
    quality_score = min(100, int((avg_stars * 15) + (total_forks * 5)))
    diversity_score = min(100, language_count * 20)
    activity_score = min(100, int((public_repos * 10) + (total_stars * 5) + (total_forks * 8)))

    overall_avg = (quality_score + diversity_score + activity_score) / 3
    if overall_avg >= 80: tier = "Elite Architect 🚀"
    elif overall_avg >= 50: tier = "Senior Contributor ⚡"
    elif overall_avg >= 20: tier = "Active Developer 💻"
    else: tier = "Emerging Builder 🌱"

    return {
        "activity_score": activity_score,
        "quality_score": quality_score,
        "diversity_score": diversity_score,
        "overall_tier": tier
    }

def analyze_repositories(repos: list, profile: dict = None) -> dict:
    joined_date = "N/A"
    if profile and "created_at" in profile:
        joined_date = format_joined_date(profile["created_at"])

    if not repos or isinstance(repos, dict):
        return {
            "total_stars": 0,
            "total_forks": 0,
            "most_starred": "N/A",
            "languages": {},
            "top_repos": [],
            "joined_date": joined_date,
            "scores": calculate_developer_score(0, 0, 0, 0)
        }

    total_stars = 0
    total_forks = 0
    most_starred_repo = "N/A"
    max_stars = -1
    languages = {}
    processed_repos = []

    for repo in repos:
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        size_kb = repo.get("size", 0)

        total_stars += stars
        total_forks += forks

        if stars > max_stars:
            max_stars = stars
            most_starred_repo = repo.get("name", "N/A")

        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

        processed_repos.append({
            "name": repo.get("name"),
            "description": repo.get("description") or "No description provided.",
            "language": lang or "Other",
            "stars": stars,
            "forks": forks,
            "size_kb": f"{size_kb:,} KB",
            "html_url": repo.get("html_url")
        })

    # Sort repos by stars (descending) and pick top 6
    top_repos = sorted(processed_repos, key=lambda x: x["stars"], reverse=True)[:6]

    public_repos = profile.get("public_repos", len(repos)) if profile else len(repos)
    scores = calculate_developer_score(total_stars, total_forks, public_repos, len(languages))

    return {
        "total_stars": total_stars,
        "total_forks": total_forks,
        "most_starred": most_starred_repo,
        "languages": languages,
        "top_repos": top_repos,
        "joined_date": joined_date,
        "scores": scores
    }