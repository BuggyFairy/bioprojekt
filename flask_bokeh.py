from flask import Flask, render_template
from bokeh.plotting import figure, output_notebook, show
from bokeh import embed

app = Flask(__name__)

@app.route('/')
def bla():
	return '<h1>Bokeh example Scheiße</h1><a href=/plot>Go to plot page</a>'

def make_my_plot(col):
    # this col_from_web has been added to the example and should be updated by the col attribute coming in through /plot/<col>
    col_from_web ="green"
    # prepare some data
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    y = x

    # create a new plot
    p = figure()

    # add some renderers
    p.line(x, x, legend="y=x")
    #p.circle(x, x, legend="y=x", fill_color="white", size=8)
    #p.line(x, y0, legend="y=x^2", line_width=3)
    #p.line(x, y1, legend="y=10^x", line_color=col)
    #p.circle(x, y1, legend="y=10^x", fill_color=col, line_color=col, size=6)
    #p.line(x, y2, legend="y=10^x^2", line_color="orange", line_dash="4 4")

    # show the results
    return p

@app.route('/plot/')
@app.route('/plot/<color>')
def hello(color='red'):
    plot = make_my_plot(color)
    script, div = embed.components(plot)
    return render_template(
        'bokeh.html',
        script=script,
        div=div
        )


if __name__ == '__main__':
	app.run(debug=True)
