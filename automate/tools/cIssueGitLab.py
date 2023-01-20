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
        # Get project
        self.project = self.gl.projects.get(_pid, lazy=True) # _pid is the project ID
        # Commit id 
        repo = git.Repo(_local_repodir)
        sha = repo.head.object.hexsha
        self.commits = self.project.commits.get(sha)
        self.commit_id = self.commits.short_id
        self.commit_idlong = self.commits.id
        # Get assignee (Person who did the last commit)
        self.gl.auth()
        self.current_user = self.gl.users.list(username=self.commits.author_email.split('@')[0])
        self.current_user_id = self.current_user[0].id

        self.title = "[DEFAULT] Error in issue creation"
        self.description = "[DEFAULT] If you see this error, there was an issue while error creation"
        self.assignee = self.current_user[0].id
        self.issuebenchmarklist = []
        
    # Set a AUTOMATE Issue | Integration
    # Author: Harikrishnan Sreekumar
    # Date: 28.07.2021
    def setAutomateIntegrationIssue(self, blist, buildcase):
        self.title = "AUTOMATE Issue | Build Type: " + buildcase + " | Integration Test | " + self.commit_id
        self.description = "This is an AUTOMATE generated issue during elPaSo CI run\n"+ \
                           "There seems to be an error while automatic tests\n"+ \
                           "                                                        \n"+ \
                           "                                                        \n"+ \
                           "Issue: Some integration test(s) did not pass\n"+ \
                           "                                                        \n"+ \
                           "Benchmarks: " + blist + "\n"+ \
                           "                                                        \n"+ \
                           "Assigned to: " + self.current_user[0].username + "\n"+ \
                           "                                                        \n"+ \
                           "Commit ID:   " + self.commit_id + " | Long: " + self.commit_idlong + "\n"+ \
                           "                                                        \n"+ \
                           "                                                        \n"+ \
                           "Please resolve the error and close the issue. In case of problems, seek help of main developers."
        self.assignee = self.current_user_id

    # Set a AUTOMATE Issue | Performance
    # Author: Harikrishnan Sreekumar
    # Date: 28.07.2021
    def setAutomatePerformanceIssue(self, blist, buildcase):
        self.title = "AUTOMATE Issue | Build Type: " + buildcase + " | Performance Test | " + self.commit_id
        self.description = "This is an AUTOMATE generated issue during elPaSo CI run\n"+ \
                           "There seems to be an error while automatic tests\n"+ \
                           "                                                        \n"+ \
                           "                                                        \n"+ \
                           "Issue: Some performance test(s) did not pass\n"+ \
                           "                                                        \n"+ \
                           "Benchmarks: " + blist + "\n"+ \
                           "                                                        \n"+ \
                           "Assigned to: " + self.current_user.username + "\n"+ \
                           "                                                        \n"+ \
                           "Commit ID:   " + self.commit_id + " | Long: " + self.commit_idlong + "\n"+ \
                           "                                                        \n"+ \
                           "                                                        \n"+ \
                           "Please resolve the error and close the issue. In case of problems, seek help of main developers."
        self.assignee = self.current_user_id
        
    # Report an issue
    # Author: Harikrishnan Sreekumar
    # Date: 28.07.2021
    def reportGitlabIssue(self):
        issue = self.project.issues.create({'title': self.title,'description': self.description,'assignee_ids':[self.assignee]})
        print("> Issue created : ", self.title)
        print("> Issue assignee: ", self.assignee)
        
    # Add a benchmark to issue list
    # Author: Harikrishnan Sreekumar
    # Date: 28.07.2021
    def addBenchmarkToIssueList(self, benchmark):
        self.issuebenchmarklist.append(benchmark)
        
    # Get BenchmarkList in string form
    # Author: Harikrishnan Sreekumar
    # Date: 28.07.2021
    def getBenchmarkListAsString(self):
        bstring = ''
        for benchmark in self.issuebenchmarklist:
            bstring = bstring + benchmark + ', '
        return bstring
