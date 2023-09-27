from app import app

if __name__ == '__main__':
    print(app.config)
    app.run(debug=True)



# 실행 : dsc_project> python .\run.py