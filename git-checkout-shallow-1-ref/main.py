from git import Blob as GitBlob
from git import Repo
from git import Remote

repo = Repo.init("/tmp/openshift-origin")
remote = Remote.add(repo, "origin", "https://github.com/openshift/origin")
repo.remotes.append(remote)
repo.remote().fetch("7b7d4ef2acfb10117f21af59d5b99da177b19d3d", depth=1)
repo.git.checkout("FETCH_HEAD")



