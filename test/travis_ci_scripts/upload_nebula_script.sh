#go to home and setup git
cd $HOME
git config --global user.email $USER_EMAIL
git config --global user.name $USER_NAME

MESSAGE=$(git log -1 HEAD --pretty=format:%s)

if [[ "$MESSAGE" == *"Travis build"* ]] || [[ "$MESSAGE" != *"RUN_UPLOAD"* ]]; then
    echo "already pushed"
else
    #clone the repository in the buildApk folder
    git clone --quiet --branch=$TRAVIS_BRANCH  https://$USER_NAME:$GITHUB_API_KEY@github.com/$USER_NAME/nebula-cmd  master > /dev/null
    cd master
    pyinstaller -F nebulactl.py
    #add, commit and push files
    git add -f .
    git remote rm origin
    git remote add origin https://$USER_NAME:$GITHUB_API_KEY@github.com/$USER_NAME/nebula-cmd.git > /dev/null 2>&1
    git add -f .
    git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed - nebulactl.py run and pushed"
    git push --quiet --set-upstream origin $TRAVIS_BRANCH
    echo -e "Done"
fi
