from flask import Flask, render_template, request, redirect, url_for
from github_api import get_user_profile, get_user_repos
from analyzer import analyze_repositories

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# THIS ROUTE WAS MISSING & CAUSING THE 404
@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form.get('username', '').strip()
    if not username:
        return render_template('index.html', error="Please enter a valid GitHub username.")
    # Redirects to /dashboard/amirhussainnaweed
    return redirect(url_for('dashboard', username=username))


@app.route('/dashboard/<username>')
def dashboard(username):
    profile = get_user_profile(username)

    if "error" in profile or not profile:
        return render_template('index.html', error="GitHub user not found.")

    repos = get_user_repos(username)
    analytics = analyze_repositories(repos, profile)

    return render_template('dashboard.html', user_profile=profile, analytics=analytics)


if __name__ == '__main__':
    app.run(debug=True)