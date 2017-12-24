cd working-bikes
git pull

pipenv install

pipenv run python manage.py migrate
pipenv run python manage.py collectstatic --noinput

touch configuration/wsgi.py

ENVIRONMENT=production
LOCAL_USERNAME=`whoami`
REVISION=`git log -n 1 --pretty=format:"%H"`

curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$WORKING_BIKES_ROLLBAR_ACCESS_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \
  -F local_username=$LOCAL_USERNAME

cd -
