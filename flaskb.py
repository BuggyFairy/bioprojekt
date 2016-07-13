from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import INLINE
from flask import Flask, request, render_template
from dinopy import FastaReader
app=Flask(__name__)



@app.route('/')
def simpleLine():
    fig=figure(title="DN-fucking-A")
    fig.line([1,2,3,4],[2,4,6,8])
    global script
    global div
    script,div=components(fig, INLINE)
    return render_template('simpleline.html', div=div, script=script)
    show(fig)

@app.route("/loadfasta", methods=['POST'])
def load_data(): 
    fasta_text = ''
    file_name = request.form['datei']
    fasta_file = FastaReader(file_name)
    for lines in fasta_file.lines():
        fasta_text = fasta_text + lines.decode("utf-8") + '\n'
    print (fasta_text)
    global script
    global div
    return render_template('simpleline.html', fasta_file=fasta_text, div=div, script=script)

#@app.route('/', methods=['GET'])
#def my_form_post():
#
#    text = request.form['text']
#    processed_text = text.upper()
#    return processed_text

if __name__ == "__main__":
    app.run(debug=True)
