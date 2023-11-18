from app import app
from flask_cors import CORS


if __name__ == '__main__': # 현재 파일이 직접 실행될 때만 코드 블록을 실행하도록 하는 조건문
    print(app.config)
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})

    app.run(debug=True)
    # Flask에서는 app 객체를 보통 __init__.py 파일에서 생성하고 초기화합니다. 



# 서버 실행 :  D:\dsc_project> python .\run.py
# 리액트 실행 : D:\dsc_project\my-react-app> npm start