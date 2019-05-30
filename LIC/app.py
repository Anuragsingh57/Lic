from flask import *
import mysql.connector
import random
import logging, os


from werkzeug.utils import secure_filename

app = Flask(__name__,static_folder="uploads")
app.secret_key = "guest"

file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upl', methods=['POST'])
def upload_file():
    # type: () -> object
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST':
        app.logger.info(app.config['UPLOAD_FOLDER'])
        policy_nm = str(request.form["t1"])
        ammount = str(request.form["t2"])
        img = request.files['t3']
        img1 = request.files['t4']
        img_name = secure_filename(img.filename)
        img1_name = secure_filename(img1.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        saved_path1 = os.path.join(app.config['UPLOAD_FOLDER'], img1_name)
        app.logger.info("saving {}".format(saved_path))
        app.logger.info("saving {}".format(saved_path1))
        img.save(saved_path)
        img1.save(saved_path1)
        # return send_from_directory(app.config['UPLOAD_FOLDER'], img_name, as_attachment=False)
        conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
        cursor = conn.cursor()
        cursor.execute(
            "insert into health(policy_number, amount, health_certificate, bill, status) values ('" + policy_nm + "','" + ammount + "','" + img_name + "','" + img1_name + "', ' Not Approved ')")

        conn.commit()

        flash("your data is entered")
        return render_template("healthcoverage.html")
    else:
        return "Where is the image?"


@app.route('/upl1', methods=['POST'])
def upload_file1():
    # type: () -> object
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST':
        app.logger.info(app.config['UPLOAD_FOLDER'])
        pln = str(request.form["t1"])
        policy_nm = str(request.form["t2"])
        name = str(request.form["t3"])
        img = request.files['t4']
        img_name = secure_filename(img.filename)

        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)

        app.logger.info("saving {}".format(saved_path))

        img.save(saved_path)

        # return send_from_directory(app.config['UPLOAD_FOLDER'], img_name, as_attachment=False)
        conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
        cursor = conn.cursor()
        cursor.execute(
            "insert into life(plan, policy_number, dependent_name, certificate, status) values ('" + pln + "','" + policy_nm + "','" + name + "','" + img_name + "', ' Not Approved ')")

        conn.commit()

        flash("your data is entered")
        return render_template("lifecoverage.html")
    else:
        return "Where is the image?"


@app.route('/admin', methods=["POST"])
def admin():
    user = str(request.form["s1"])
    pw = str(request.form["s2"])

    conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
    cursor = conn.cursor()

    cursor.execute("select * from admin where email='" + user + "' and password='" + pw + "'")
    if cursor.fetchone():

        flash("Log-in successfully")

        return render_template("adminpage.html")
    else:
        flash('uid or password wrong')
        return render_template("index.html")


@app.route('/')
def display_deals():
    conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
    cursor = conn.cursor()

    try:

        query = "SELECT * from health"
        cursor.execute(query)

        data = cursor.fetchall()

        conn.close()

        #return data

        return render_template("request.html", data=data)

    except Exception as e:
        return (str(e))


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/edit')
def edit():
    conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
    cursor = conn.cursor()
    print(request.args.get('id'))

    try:

        query = "update health set status='Approved' where id="+request.args.get('id')
        cursor.execute(query)
        conn.commit()



        query1 = "SELECT * from health"
        cursor.execute(query1)

        data = cursor.fetchall()

        conn.close()

        # return data

        return render_template("request.html", data=data)


    except Exception as e:
        return (str(e))





@app.route('/Insurance plans')
def Insurance():
    return render_template("insurance.html")


@app.route('/Contact')
def Contact():
    return render_template("contact.html")


@app.route('/ammount', methods=["POST"])
def login():
    user = str(request.form["s1"])
    pw = str(request.form["s2"])

    conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
    cursor = conn.cursor()

    cursor.execute("select * from signup where email='" + user + "' and password='" + pw + "'")
    if cursor.fetchone():
        session["usr"] = user
        flash("Log-in successfully")

        return render_template("Cdetails.html")
    else:
        flash('uid or password wrong')
        return render_template("index.html")


@app.route('/', methods=["POST"])
def signup():
    x = random.randint(2313345643, 3334490876)
    random_ref = str(x)
    nm = str(request.form["t1"])
    gn = str(request.form["f"])
    em = str(request.form["t2"])
    mb = str(request.form["t3"])
    pw = str(request.form["t4"])
    dob = str(request.form["t5"])
    pan = str(request.form["t6"])
    dd = str(request.form["t7"])
    pd = str(request.form["t8"])
    py = str(request.form["t9"])
    pa = str(request.form["t10"])
    ppa = str(request.form["t11"])
    session["usr"] = em

    conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
    cursor = conn.cursor()

    cursor.execute(
        "insert into signup(name,gender,email,mobile,password,DOB,PAN,dependent,policydate,policyyear,policyammount,preammount,policynumber) values ('" + nm + "','" + gn + "','" + em + "','" + mb + "','" + pw + "','" + dob + "','" + pan + "','" + dd + "','" + pd + "','" + py + "','" + pa + "','" + ppa + "','" + random_ref + "')")

    conn.commit()

    conn = mysql.connector.connect(host="localhost", user="root", password="", db="LIC")
    cursor = conn.cursor()
    cursor.execute("select * from signup where email='" + session["usr"] + "")

    row = cursor.fetchone()

    return render_template("show.html", x=row)


@app.route('/index')
def OK():
    return render_template("index.html")


@app.route('/health')
def health():
    return render_template("health.html")


@app.route('/life')
def life():
    return render_template("life.html")


@app.route('/option', methods=["POST"])
def option():
    a = str(request.form["s1"])
    b = str(request.form["s2"])
    if a == "Health Insurance" and b == "Coverage Offered":

        return render_template("healthcoverage.html")

    elif a == "Life Insurance" and b == "Coverage Offered":

        return render_template("lifecoverage.html")

    elif a == "Health Insurance" and b == "Payment":

        return render_template("healthdetails.html")

    elif a == "Life Insurance" and b == "Payment":

        return render_template("lifedetails.html")

    else:
        flash('uid or password wrong')


@app.route('/pay', methods=["POST"])
def pay():
    return render_template("payment.html")


@app.route('/pay1', methods=["POST"])
def pay1():
    return render_template("payment.html")


if __name__ == '__main__':
    app.run()
