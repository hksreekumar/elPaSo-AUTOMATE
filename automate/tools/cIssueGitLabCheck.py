# Copyright (c) 2023. Authors listed in AUTHORS.md
#
# This file is part of elPaSo-AUTOMATE.
#
# elPaSo-AUTOMATE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# elPaSo-AUTOMATE is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with elPaSo-AUTOMATE (COPYING.txt). If not, see
# <https://www.gnu.org/licenses/>. 

## AUTOMATE Automated Testing Framework for elPaSo
## The current file is a part of AUTOMATE code package
##
## Authors: Harikrishnan Sreekumar, Christopher Blech
## Property of : Institut f�r Akustik, TU Braunschweig, Germany

# Project imports
import gitlab
import git
import os

# Class for GitlabIssue Reporting
# Author: Harikrishnan Sreekumar
# Date: 28.07.2021

class cIssueGitLab:
    # Constructor
    # Author: Harikrishnan Sreekumar
    # Date: 28.07.2021
    def __init__(self, _remote_repos, _pid, _local_repodir):
        # private token or personal token authentication
        self.gl = gitlab.Gitlab(_remote_repos, private_token=os.environ['CI_JOB_TOKEN_AUTOMATE_ISSUE'])
        if (os.environ['CI_JOB_TOKEN_AUTOMATE_ISSUE'] != ''):
            print('> cIssueGitLab: Key used from CI_JOB_TOKEN_AUTOMATE_ISSUE')
        # Get project
        self.project = self.gl.projects.get(_pid, lazy=True) # _pid is the project ID
        # Commit id 
        repo = git.Repo(_local_repodir)
        sha = repo.head.object.hexsha
        self.commits = self.project.commits.get(sha)
        self.commit_id = self.commits.short_id
        self.commit_idlong = self.commits.id
        print('----- CoID: ' + str(self.commits.id))
        print('---- EMAIL: ' + str(self.commits.author_email))
        # Get assignee (Person who did the last commit)
        self.gl.auth()
        self.current_user = self.gl.users.list(username=self.commits.author_email.split('@')[0])
        self.current_user_id = self.current_user[0].id
        
        print('----- USER: ' + str(self.current_user))
        print('------- ID: ' + str(self.current_user_id))

        self.title = "[DEFAULT] Error in issue creation"
        self.description = "[DEFAULT] If you see this error, there was an issue while error creation"
        self.assignee = self.current_user[0].id
        self.issuebenchmarklist = []

if __name__ == '__main__':
    instance = cIssueGitLab('https://git.rz.tu-bs.de/', 2892, '/home/sreekumar/software/repos/NEW_elPaSo-Core/')
