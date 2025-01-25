from flask import Flask
from flask import request
from flask import redirect
#import hashlib

app = Flask(__name__)


@app.route("/")
def home():
    html = ""
    opt = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open("publics.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    title = lines[-2]
    description = lines[-1]
    opt += f"<div class='post-card'> <h2>{title}</h2> <p>{description}</p> <a href='http://127.0.0.1:5000/pad/{title}'>前往</a> </div>"
    return html.replace("<out/>", opt)


@app.route("/signup")
def signup():
    html = ""
    with open("sign_up.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html


@app.route("/signup_finish", methods=["POST"])
def signup_finish():
    html = ""
    with open("signup_finish.html", "r", encoding="utf-8") as f:
        html = f.read()
    username = request.form.get("username")
    email = request.form.get("email")
    psw1 = request.form.get("psw1")
    psw2 = request.form.get("psw2")
    if psw1 != psw2:
        return html.replace("<out/>", "請確認密碼一致")
    try:
        with open(f"users/{username}.txt", "r", encoding="utf-8") as f:
            pass
        return html.replace("<out/>", "已有此username，請更改")
    except:
        with open(f"users/{username}.txt", "a", encoding="utf-8") as f:
            f.write(email + "\n")
            f.write(psw1)
        # 尚未hash
        return html.replace("<out/>", "註冊完畢，請在創建新的pad時登入")


@app.route("/create")
def create():
    html = ""
    with open("create.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html


@app.route("/create_finish", methods=["POST"])
def create_finish():
    title = request.form.get("title")
    description = request.form.get("description")
    public = request.form.get("public")
    username = request.form.get("username")
    psw = request.form.get("psw")
    try:
        html = ""
        with open(f"pads/{title}.txt", "r", encoding="utf-8") as f:
            pass
        with open("signup_finish.html", "r", encoding="utf-8") as f:
            html = f.read()
        return html.replace("<out/>", "此標題已有人使用，請更改標題。")
    except:
        if public == "yes":
            with open("publics.txt", "a", encoding="utf-8") as f:
                f.write("\n" + title + "\n")
                f.write(description)
            with open(f"pads/{title}.txt", "a", encoding="utf-8") as f:
                f.write(description)
        elif public == "no":
            with open(f"pads/{title}.txt", "a", encoding="utf-8") as f:
                f.write(description)
        else:
            html = ""
            with open("create.html", "r", encoding="utf-8") as f:
                html = f.read()
            return html.replace("<out/>", "請正確輸入是否公開(yes/no)")
        # 登入暫不做
        return redirect(f"http://127.0.0.1:5000/pad/{title}")  # 到時候改成真正網址


@app.route("/publicpads")
def publicpads():
    html = ""
    opt = ""
    with open("publics.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    for i in range(len(lines)):
        if i % 2 == 0:
            pass
        else:
            title = lines[i]
            description = lines[i + 1]
            opt += f"<div class='post-card'> <h2>{title}</h2> <p>{description}</p> <a href='http://127.0.0.1:5000/pad/{title}'>前往</a> </div>"
    with open("publicpads.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html.replace("<out/>", opt)


@app.route("/pad/<string:filename>")
def pad(filename):
    try:
        opt = ""
        html = ""
        with open(f"pads/{filename}.txt", "r", encoding="utf-8") as f:
            opt = f.read()
        return opt
    except:
        html = ""
        with open("signup_finish.html", "r", encoding="utf-8") as f:
            html = f.read()
        return html.replace("<out/>", "無此頁面")


@app.route("/about")
def about():
    html = ""
    with open("about.html", "r", encoding="utf-8") as f:
        html = f.read()
        return html


app.run(debug=True, host="0.0.0.0", port='7000')
