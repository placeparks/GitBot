import streamlit as st
from github import Github

def authenticate_user(username, password):
    try:
        g = Github(username, password)
        return g
    except Exception as e:
        st.error(f"Failed to authenticate: {str(e)}")
        return None


def get_repository_info(github_user, repo_url):
    # Parse repository owner and name from URL
    parts = repo_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1].replace('.git', '')  # Remove .git if present

    try:
        # Get repository details
        repo = github_user.get_repo(f'{owner}/{repo_name}')
        # Get latest commits
        commits = repo.get_commits()[:5]
        latest_commits = [
            {
                'date': commit.commit.author.date.strftime('%Y-%m-%d %H:%M:%S'),
                'message': commit.commit.message
            }
            for commit in commits
        ]
        # Get README content
        readme_content = repo.get_readme().decoded_content.decode("utf-8")
        return {
            'name': repo.name,
            'description': repo.description,
            'language': repo.language,
            'clone_url': repo.clone_url,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'watchers': repo.watchers_count,
            'size': repo.size,
            'latest_commits': latest_commits,
            'readme': readme_content
        }
    except Exception as e:
        st.error(f"Error fetching repository details: {str(e)}")
        return None


def main():
    st.title("GitHub Repository Information")

    # Authentication
    st.subheader("GitHub Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    auth_button = st.button("Authenticate")

    if auth_button and username and password:
        github_user = authenticate_user(username, password)
        if github_user:
            st.success("Authentication successful")

            # Repository input
            repo_url = st.text_input("Enter the GitHub repository URL")

            if st.button("Get Repository Info"):
                if repo_url:
                    repository_info = get_repository_info(github_user, repo_url)
                    if repository_info:
                        st.subheader("Repository Info")
                        st.write(f"Name: {repository_info['name']}")
                        st.write(f"Description: {repository_info['description']}")
                        st.write(f"Language: {repository_info['language']}")
                        st.write(f"Clone URL: {repository_info['clone_url']}")
                        st.write(f"Stars: {repository_info['stars']}, Forks: {repository_info['forks']}, Watchers: {repository_info['watchers']}, Size: {repository_info['size']} KB")

                        st.subheader("Latest Commits")
                        for commit in repository_info['latest_commits']:
                            st.write(f"- {commit['date']}: {commit['message']}")

                        st.subheader("README")
                        st.write(repository_info["readme"])
                    else:
                        st.error("Failed to fetch repository details")
                else:
                    st.warning("Please enter a repository URL")
        else:
            st.error("Failed to authenticate")


if __name__ == "__main__":
    main()