#go to home and setup git
cd $HOME
git config --global user.email "user-email@email.com"
git config --global user.name "user-name"

#clone the repository in the buildApk folder
git clone --quiet --branch=master  https://user-name:$GITHUB_API_KEY@github.com/user-name/nebula-cmd  master > /dev/null

cd master
pyinstaller -F nebulactl.py

#add, commit and push files
git add -f .
git remote rm origin
git remote add origin https://user-name:$GITHUB_API_KEY@github.com/user-name/nebula-cmd.git
git add -f .
git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed - nebulactl.py run and pushed"
git push -fq origin master > /dev/null
echo -e "Done"
