v4l2-ctl -d /dev/video0 --set-ctrl=white_balance_automatic=0,exposure=1,contrast=30,gain_automatic=0,auto_exposure=1
python3 /home/pi/vision2020/locate_target.py