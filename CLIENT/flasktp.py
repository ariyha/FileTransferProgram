from flask import Flask, redirect, url_for, request,render_template
import clientidea

app = Flask(__name__)
 
host = 'localhost'

@app.route('/download',methods=['GET','POST'])
def download_file():

    if request.method=='POST':
        if(request.form['fname']== ''):
            return "<html><body> <h1>INVALID DATA</h1></body></html>"

        else:
            name  = request.form['fname']

            print(name)
            
            k = clientidea.ftp_client_download(name,host=host)

            if k=='FILE_SEND_UNSUCCESFUL':
                return "<html><body> <h1>There was an error in file</h1></body></html>"
            return render_template('success.html',data=name)
    if request.method=='GET':
        return render_template('rand.html',data=clientidea.get_files(host=host))
    

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('rand2.html', fpath='')

    if request.method == 'POST':
        if request.form['fileInput']=='':
            return "<html><body> <h1>INVALID DATA</h1></body></html>"
        else:
            filepath = request.form['fileInput']
        
        
        clientidea.client_upload(filepath)
        return render_template('rand2.html', fpath=filepath)


@app.route("/",methods=['GET','POST'])
def choose():
    if request.method=='POST':
        print(1)
        print(request.form['service'])
        if request.form['service']=='download':
            return redirect(url_for('download_file'))
        else:
            return redirect(url_for('upload_file'))
    
    if request.method=='GET':
        return render_template('choose.html')

if __name__ == '__main__':
    app.run(debug=True,host='localhost')