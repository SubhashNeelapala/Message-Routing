# Build and run solution
pip3 install --user -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate --run-syncdb
python3 manage.py runserver 0.0.0.0:8000 &>/dev/null &
SERVER_PID=$!
# Setup test environment
cd .questiontest
pip3 install --user -r requirements.txt
sleep 5
py.test --suppress-tests-failed-exit-code --junitxml=results.xml
kill $SERVER_PID
sleep 1
python3 score.py
