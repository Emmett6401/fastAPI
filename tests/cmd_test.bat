echo off
echo.
echo ====================== curl test 결과 출력 ======================
curl -X POST -F "file=@D:\Pictures\KakaoTalk_20230505_164421070_08.jpg" http://localhost:8080/upload
echo.
echo ====================== curl test finish   ======================
echo.
echo.
echo ====================== test_api.py 실행   ======================
echo.
pytest test_api.py -vv --capture=no
echo.
echo ====================== test_api.py finish ======================

