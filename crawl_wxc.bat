@echo off
rem ------------------------------------------------------------
rem 1. 设定工作目录（请改成你自己的路径）
set WORK_DIR=d:\Workspace\wxc_crawler
rem ------------------------------------------------------------
rem 2. 设定 virtualenv 的名字（与 venv 创建时一致）
set VENV_NAME=venv
rem ------------------------------------------------------------
rem 3. 要执行的命令（Python 脚本、pip install 等）
set "CMD=git pull && pip install -r requirements.txt && python crawl.py --category znjy && python crawl.py --category tzlc  && echo 任务完成"
rem ------------------------------------------------------------
rem 4. 日志文件（可选）
set LOG_FILE=%WORK_DIR%\run_%date:~-4%%date:~4,2%%date:~7,2%.log

rem ------------------------------------------------------------
rem 进入工作目录
pushd "%WORK_DIR%" || (
    echo [ERROR] Cannot change to %WORK_DIR%
    exit /b 1
)

rem ------------------------------------------------------------
rem 激活 virtualenv
call "%WORK_DIR%\%VENV_NAME%\Scripts\activate.bat" || (
    echo [ERROR] Cannot activate virtualenv %VENV_NAME%
    popd
    exit /b 1
)

rem ------------------------------------------------------------
rem 执行命令并把输出写入日志（如果你想看到即时输出，可以去掉 `> "%LOG_FILE%" 2>&1`）
echo Running: %CMD% >> "%LOG_FILE%"
%CMD% >> "%LOG_FILE%" 2>&1

rem ------------------------------------------------------------
rem 退出 virtualenv 并返回原目录
deactivate || (
    echo [WARN] deactivate failed (maybe not needed)
)

popd

echo Finished at %time% >> "%LOG_FILE%"
exit /b 0