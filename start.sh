python3 ./weibo_hot_list_serach.py

year=`date +%Y `
month=`date +%m `
day=`date +%d `
hour=`date +%H`
now=$year-$month-$day-$hour


git config --global user.email "ouweijie123@outlook.com"
git config --global user.name "actioner"

git add .
git commit -m "$now"
