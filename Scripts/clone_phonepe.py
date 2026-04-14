import git

repo_url = "https://github.com/PhonePe/pulse.git"
destination_path = r"C:\PhonePe Final Project\Pulse"

git.Repo.clone_from(repo_url, destination_path)
print("Repository cloned successfully!")