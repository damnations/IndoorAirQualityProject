@xset s off
@xset -dpms
@xset s noblank

unclutter &
@chromium-browser --window-size=320,240 --kiosk --incognito --noerrdialogs --disable-infobars file:/home/akhrs/IndoorAirQualityProject/Html/Display.html