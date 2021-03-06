#!/usr/bin/env bash
#go to home and setup git
cd $HOME
git config --global user.email $USER_EMAIL
git config --global user.name $USER_NAME

#clone the repository in the buildApk folder
git clone --quiet --branch=$TRAVIS_BRANCH  https://$USER_NAME:$GITHUB_API_KEY@github.com/nebula-orchestrator/nebula-cmd master > /dev/null 2>&1

cd master
pyinstaller -F `pwd`/nebulactl.py

MESSAGE=$(git log -1 HEAD --pretty=format:%s)

#add, commit and push files
git remote rm origin
git remote add origin https://$USER_NAME:$GITHUB_API_KEY@github.com/nebula-orchestrator/nebula-cmd.git > /dev/null 2>&1
git add dist/nebulactl
git commit -m '[skip travis] build $TRAVIS_BUILD_NUMBER pushed - nebulactl.py run and pushed'
git push --quiet --set-upstream origin $TRAVIS_BRANCH
echo -e "upload run and pushed"
