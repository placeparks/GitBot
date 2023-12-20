import streamlit as st
from app import get_repository_info
from base64 import b64decode

def display_repository_info(repo_info):
    st.write(f"**Name:** {repo_info['name']}")
    st.write(f"**Description:** {repo_info['description']}")
    st.write(f"**Language:** {repo_info['language']}")
    st.write(f"**Clone URL:** {repo_info['clone_url']}")
    st.write(f"**Stars:** {repo_info['stars']}, **Forks:** {repo_info['forks']}, **Watchers:** {repo_info['watchers']}, **Size:** {repo_info['size']}KB")
    
    st.subheader("Latest Commits:")
    for commit in repo_info["latest_commits"]:
        st.write(f"- {commit['commit']['author']['date']}: {commit['commit']['message']}")

    st.subheader("README:")
    st.text(repo_info["readme"])

def main():
    st.title('GitHub Repository Information Tool')

    github_token = st.text_input("GitHub Personal Access Token:", type="password")
    repo_url = st.text_input("Enter the GitHub repository URL:")

    if st.button('Fetch Repository Info'):
        if not github_token or not repo_url:
            st.warning('Please enter both a GitHub Personal Access Token and a repository URL.')
        else:
            with st.spinner('Fetching repository details...'):
                repo_info = get_repository_info(repo_url, github_token)
                if repo_info:
                    st.success('Repository details fetched successfully!')
                    display_repository_info(repo_info)
                else:
                    st.error('Failed to fetch repository details or invalid token.')

if __name__ == '__main__':
    main()
